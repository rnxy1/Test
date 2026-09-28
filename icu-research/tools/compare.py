"""Compare Reader A vs Reader B, run checks, route every field (no AI).
usage: python3 compare.py <patient_dir> <folder_name> <A_dir> <B_dir>
"""
import sys, os, re, json, glob
sys.path.insert(0, os.path.dirname(__file__))
from arabic import norm

pdir, folder_name, adir, bdir = sys.argv[1:5]
proj = os.path.dirname(os.path.dirname(os.path.abspath(pdir)))
FIELDS = json.load(open(os.path.join(proj, 'fields.json')))
A = json.load(open(os.path.join(adir, 'consolidated.json')))
B = json.load(open(os.path.join(bdir, 'consolidated.json')))
pages = {r: {os.path.basename(f)[:-5]: json.load(open(f)) for f in glob.glob(os.path.join(d, 'pages', '*.json'))}
         for r, d in (('A', adir), ('B', bdir))}
WINDOW = ((15, 7, 2026), (15, 8, 2026))

# ---------- normalization ----------
def n_date(v):
    m = re.search(r'(\d{1,2})\s*[/\-.]\s*(\d{1,2})(?:\s*[/\-.]\s*(\d{2,4}))?', str(v))
    if not m: return None
    d, mo, y = int(m[1]), int(m[2]), m[3]
    y = (int(y) + 2000 if y and len(y) == 2 else int(y)) if y else None
    return (d, mo, y)
def n_time(v):
    m = re.search(r'(\d{1,2})[:.](\d{2})\s*(am|pm|ص|م)?', str(v).lower())
    if not m: return None
    h, mi = int(m[1]), int(m[2])
    if m[3] in ('pm', 'م') and h < 12: h += 12
    if m[3] in ('am', 'ص') and h == 12: h = 0
    return f'{h:02d}:{mi:02d}'
def nums(v): return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', str(v))]
def meas(v):
    """measurement numbers only: drop (...) annotations, source IDs, real dates and clock times"""
    s = re.sub(r'\([^)]*\)', ' ', str(v))
    s = re.sub(r'\b(?:P|R|WA)\d{2}\b', ' ', s)
    s = re.sub(r'\b(\d{1,2})\s*[/.-]\s*(\d{1,2})(?:\s*[/.-]\s*\d{2,4})?\b',
               lambda m: ' ' if int(m[1]) <= 31 and 1 <= int(m[2]) <= 12 else m[0], s)
    s = re.sub(r'\d{1,2}:\d{2}(\s*[ap]m)?', ' ', s, flags=re.I)
    return [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s)]
def n_text(v): return re.sub(r'[^\w\s/]', '', norm(str(v))).strip()
def n_multi(v): return frozenset(t.strip() for t in re.split(r'[,;/+]| and ', n_text(v)) if t.strip())

def opts_in(field, v):
    txt = ' ' + re.sub(r'[^\w\s]', ' ', str(v).lower()) + ' '
    return frozenset(o for o in field['options'] if re.search(r'(?<![\w])' + re.escape(re.sub(r'[^\w\s]', ' ', o.lower())).replace('\\ ', r'\s+') + r'(?![\w])', txt))

def normalize(field, v):
    t = field['type']
    if v is None: return None
    if str(v).upper().startswith('CONFLICT'): return ('conflict', n_text(v))
    if t == 'date': return n_date(v)
    if t == 'time': return n_time(v)
    if t == 'datetime': return (n_date(v), n_time(v))
    if t == 'number': return tuple(nums(v)[:1]) or n_text(v)
    if t == 'apache': return frozenset(meas(v))
    if t in ('option', 'multi'):
        found = opts_in(field, v)
        if found: return found if t == 'multi' else (found if len(found) > 1 else next(iter(found)))
        return n_multi(v) if t == 'multi' else n_text(v)
    return n_text(v)

def same(field, a, b):
    if isinstance(a, tuple) and a[:1] == ('conflict',) or isinstance(b, tuple) and b[:1] == ('conflict',):
        return a == b
    if field['type'] == 'date' and a and b:           # year may be missing on one side
        return a[:2] == b[:2] and (a[2] is None or b[2] is None or a[2] == b[2])
    if field['type'] == 'text' and field['id'] == 'A01' and a and b:
        return a in b or b in a
    return a == b

# ---------- evidence helpers ----------
def items(r): return (r or {}).get('items') or []
def has_evidence(r): return any(i.get('source') and i.get('quote') for i in items(r))
def uncertain(r): return '[?]' in json.dumps(r, ensure_ascii=False) or 'illegible' in str((r or {}).get('value', '')).lower()
def wa_only(r): return bool(items(r)) and all(str(i.get('source', '')).startswith('WA') for i in items(r))
def page_type(src):
    for rd in ('A', 'B'):
        p = pages[rd].get(src)
        if p: return p.get('page_type', '')
    return ''

# ---------- per-field compare ----------
rows, get = [], lambda d, fid: (d.get('fields') or {}).get(fid) or {'status': 'MISSING'}
for f in FIELDS:
    ra, rb = get(A, f['id']), get(B, f['id'])
    sa, sb = ra.get('status'), rb.get('status')
    va, vb = ra.get('value'), rb.get('value')
    na, nb = (normalize(f, va) if sa == 'FOUND' else None), (normalize(f, vb) if sb == 'FOUND' else None)
    if sa == sb == 'FOUND':
        cls = 'AGREE' if same(f, na, nb) else 'DISAGREE'
    elif 'FOUND' in (sa, sb):
        cls = 'ONE_FOUND'
    elif sa == sb == 'NOT_APPLICABLE':
        cls = 'AGREE_NA'
    elif 'NOT_APPLICABLE' in (sa, sb):
        cls = 'DISAGREE'
    elif 'CANNOT_ASSESS' in (sa, sb):
        cls = 'CANNOT_ASSESS'
    else:
        cls = 'BOTH_NOT_FOUND'
    rows.append(dict(field=f, A=ra, B=rb, cls=cls, checks=[], flags=[]))
R = {r['field']['id']: r for r in rows}

# ---------- checks (plausibility / consistency / eligibility / identity) ----------
def chk(fid, ok, msg):
    R[fid]['checks'].append(('PASS' if ok else 'FAIL', msg))
def agreed(fid): return R[fid]['cls'] == 'AGREE'
def val(fid): return R[fid]['A'].get('value') if R[fid]['A'].get('status') == 'FOUND' else R[fid]['B'].get('value')

fn = norm(folder_name)
for rd in 'AB':
    r = R['A01'][rd]
    if r.get('status') == 'FOUND':
        chk('A01', fn in norm(str(r.get('value'))) or norm(str(r.get('value'))) in fn, f'Reader {rd} name vs folder name "{folder_name}"')
reg_names = [norm(i.get('quote', '')) for rd in 'AB' for i in items(R['A01'][rd]) if str(i.get('source', '')).startswith('R')]
if reg_names:
    chk('A01', any(fn.split()[0] in q for q in reg_names), 'name matches ICU register row')
if R['A02']['cls'] in ('AGREE', 'DISAGREE', 'ONE_FOUND'):
    for rd in 'AB':
        n = nums(R['A02'][rd].get('value')) if R['A02'][rd].get('status') == 'FOUND' else []
        if n: chk('A02', 0 <= n[0] <= 120, f'Reader {rd} age {n[0]} within 0–120')
def in_window(d):
    if not d or d[2] is None and False: return None
    y = d[2] or 2026
    return WINDOW[0][::-1] <= (y, d[1], d[0]) <= WINDOW[1][::-1]
for rd in 'AB':
    r = R['C01'][rd]
    if r.get('status') == 'FOUND':
        d = n_date(r.get('value'))
        chk('C01', bool(d) and in_window(d), f'Reader {rd} ICU admission {r.get("value")} inside 15/07–15/08/2026 (eligibility)')
        regd = [n_date(i.get('clinical_datetime') or i.get('quote')) for i in items(r) if str(i.get('source', '')).startswith('R') and n_date(i.get('clinical_datetime') or i.get('quote'))]
        if regd and d:
            chk('C01', all(x[:2] == d[:2] for x in regd), f'Reader {rd} admission date matches register entry')
if R['C01']['cls'] in ('BOTH_NOT_FOUND', 'CANNOT_ASSESS'):
    chk('C01', False, 'eligibility cannot be confirmed: no ICU admission date found')
for rd in 'AB':
    c, j = R['C01'][rd], R['J02'][rd]
    if c.get('status') == j.get('status') == 'FOUND':
        dc, dj = n_date(c['value']), n_date(j['value'])
        if dc and dj:
            chk('J02', (dj[2] or 2026, dj[1], dj[0]) >= (dc[2] or 2026, dc[1], dc[0]), f'Reader {rd} outcome date after admission')
jv = n_text(val('J01') or '')
if R['J01']['cls'] == 'AGREE':
    death = 'death' in jv
    for k in ('K01', 'K02', 'K03', 'K04'):
        if death:
            chk(k, R[k]['cls'] != 'AGREE_NA', 'death documented → section K applies')
        else:
            chk(k, R[k]['cls'] in ('AGREE_NA', 'BOTH_NOT_FOUND'), 'non-death outcome → section K should be N/A')
if 'yes' in n_text(val('D03') or '') and R['E02']['cls'] in ('AGREE', 'DISAGREE', 'ONE_FOUND'):
    chk('E02', 't' in n_text(val('E02') or ''), 'ventilated at admission → GCS V should be T')
if 'yes' in n_text(val('D01') or ''):
    srcs = [i.get('source') for rd in 'AB' for i in items(R['D02'][rd])]
    chk('D02', any('drug' in page_type(s).lower() for s in srcs), 'named vasopressor appears on a drug/medication chart page')
RANGES = {'L01': (25, 45), 'L03': (0, 300), 'L04': (0, 80), 'L06': (6.5, 8.0), 'L07': (100, 200), 'L08': (1, 10), 'L10': (5, 75), 'L11': (0, 200)}
for fid, (lo, hi) in RANGES.items():
    for rd in 'AB':
        r = R[fid][rd]
        if r.get('status') == 'FOUND':
            bad = [x for x in meas(r.get('value')) if not lo <= x <= hi]
            chk(fid, not bad, f'Reader {rd} values within {lo}–{hi}' + (f' (check: {bad[:4]})' if bad else ''))

# ---------- routing (§7) ----------
for r in rows:
    f, cls = r['field'], r['cls']
    fl = r['flags']
    for rd in 'AB':
        x = r[rd]
        if x.get('status') == 'FOUND':
            if not has_evidence(x): fl.append(f'Reader {rd}: value without page ID + quote → rejected')
            if uncertain(x): fl.append(f'Reader {rd}: uncertain characters [?]')
            if x.get('conflict'): fl.append(f'Reader {rd}: conflicting sources')
            if wa_only(x): fl.append(f'Reader {rd}: WhatsApp-only evidence')
    failed = any(s == 'FAIL' for s, _ in r['checks'])
    if cls in ('BOTH_NOT_FOUND', 'CANNOT_ASSESS'):
        route = 'RED'
    elif f['route'] == 'SPECIALIST' and cls != 'AGREE_NA':
        route = 'PURPLE'
    elif cls == 'AGREE_NA' and not failed and R['J01']['cls'] == 'AGREE':
        route = 'GREEN'
    elif cls == 'AGREE' and f['route'] == 'AUTO_OK' and not fl and not failed:
        route = 'GREEN'
    else:
        route = 'YELLOW'
    if f['id'] in ('E04', 'E08') and route == 'GREEN': route = 'YELLOW'
    r['route'] = route

out = {'patient': folder_name, 'readers': {'A': os.path.basename(adir), 'B': os.path.basename(bdir)},
       'timeline': {'A': A.get('timeline'), 'B': B.get('timeline')},
       'page_types_present': {'A': A.get('page_types_present'), 'B': B.get('page_types_present')},
       'apache_total': 'not computed — APACHE time-window decision pending (§15.1)',
       'rows': [{**{k: v for k, v in r.items() if k != 'field'}, 'id': r['field']['id'], 'label': r['field']['label'],
                 'field_route': r['field']['route']} for r in rows]}
json.dump(out, open(os.path.join(pdir, 'comparison.json'), 'w'), ensure_ascii=False, indent=1, default=list)
from collections import Counter
print('classes:', dict(Counter(r['cls'] for r in rows)))
print('routes :', dict(Counter(r['route'] for r in rows)))
print('failed checks:', [(r['field']['id'], m) for r in rows for s, m in r['checks'] if s == 'FAIL'])
