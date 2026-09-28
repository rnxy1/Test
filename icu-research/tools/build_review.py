"""Single-reader v4 → review v4.1 HTML (no AI).
usage: python3 build_review.py <patient_dir> <reader_dir> <folder_name> <out.html>
Routing (single reader, replaces two-reader agreement):
  NOT_FOUND / CANNOT_ASSESS → 🔴 ; SPECIALIST field → 🟣 ;
  🟢 only if: AUTO_OK field, FOUND with page+quote, no [?]/conflict, not WhatsApp-only, checks pass,
     and the value is corroborated by ≥2 independent (non-duplicate) sources ; everything else → 🟡.
"""
import sys, os, re, json, io, base64, hashlib, html, datetime
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from arabic import norm

pdir, rdir, folder_name, out_path = sys.argv[1:5]
proj = os.path.dirname(os.path.dirname(os.path.abspath(pdir)))
FIELDS = json.load(open(os.path.join(proj, 'fields.json')))
TAG = '<script id="review-data" type="application/json">'
TPL = open(os.path.join(proj, 'v3', 'review_v41.html'), encoding='utf-8').read()
FORM = json.load(open(os.path.join(proj, 'v3', 'form_sections.json')))
INV = {r['id']: r for r in json.load(open(os.path.join(pdir, 'inventory.json')))}
R = json.load(open(os.path.join(rdir, 'consolidated.json')))
PAGES = {f[:-5]: json.load(open(os.path.join(rdir, 'pages', f))) for f in os.listdir(os.path.join(rdir, 'pages')) if f.endswith('.json')}
WA = json.load(open(os.path.join(pdir, 'wa_hits.json')))
WA_TXT = open(os.path.join(proj, 'shared', 'whatsapp.txt'), encoding='utf-8').read()
WINDOW = ((2026, 7, 15), (2026, 8, 15))
META = json.load(open(os.path.join(pdir, 'meta.json')))
KB_PATH = os.path.join(proj, 'shared', 'field_locations.json')

# ---------- image assets (deduplicated, WR-032) ----------
assets = {}
def add_asset(im, maxw, q=80, fmt='JPEG'):
    im = im.copy(); im.thumbnail((maxw, maxw * 4))
    buf = io.BytesIO(); im.convert('RGB').save(buf, fmt, quality=q)
    b = buf.getvalue(); k = hashlib.md5(b).hexdigest()[:12]
    assets.setdefault(k, f'data:image/{fmt.lower()};base64,' + base64.b64encode(b).decode())
    return 'asset:' + k
_pg = {}
def page_img(pid):
    if pid not in _pg: _pg[pid] = Image.open(os.path.join(pdir, INV[pid]['reading_copy'])).convert('RGB')
    return _pg[pid]
def crop_box(pid, bbox):
    try:
        x0, y0, x1, y1 = [max(0.0, min(1.0, float(v))) for v in bbox]
    except (TypeError, ValueError):
        return None
    if x1 <= x0 or y1 <= y0: return None
    im = page_img(pid); W, H = im.size
    return im.crop((int(max(0, x0 - .012) * W), int(max(0, y0 - .008) * H), int(min(1, x1 + .012) * W), int(min(1, y1 + .008) * H)))
def stacked(crops):
    crops = [c for c in crops if c is not None]
    if not crops: return None
    if len(crops) == 1: return crops[0]
    w = max(c.width for c in crops); h = sum(c.height for c in crops) + 6 * (len(crops) - 1)
    out = Image.new('RGB', (w, h), 'white'); y = 0
    for c in crops: out.paste(c, (0, y)); y += c.height + 6
    return out

# ---------- helpers ----------
def n_date(v):
    m = re.search(r'(\d{1,2})\s*[/\-.]\s*(\d{1,2})(?:\s*[/\-.]\s*(\d{2,4}))?', str(v or ''))
    if not m or int(m[2]) > 12: return None
    y = m[3]; y = (int(y) + 2000 if len(y) == 2 else int(y)) if y else 2026
    return (y, int(m[2]), int(m[1]))
def items(x): return (x or {}).get('items') or []
def quote_ok(x): return any(i.get('source') and i.get('quote') for i in items(x))
def has_q(x): return '[?]' in json.dumps(x, ensure_ascii=False)
def wa_only(x): return bool(items(x)) and all(str(i.get('source', '')).startswith('WA') for i in items(x))
def indep_sources(x):
    s = set()
    for i in items(x):
        src = str(i.get('source', ''))
        s.add((INV.get(src) or {}).get('duplicate_of') or src)
    return s
def F(fid): return R['fields'].get(fid) or {'status': 'MISSING'}
def val(fid): return F(fid).get('value') if F(fid).get('status') == 'FOUND' else None
def opts_in(field, v):
    txt = ' ' + re.sub(r'[^\w\s]', ' ', str(v or '').lower()) + ' '
    return {o for o in field['options'] if re.search(r'(?<![\w])' + r'\s+'.join(map(re.escape, re.sub(r'[^\w\s]', ' ', o.lower()).split())) + r'(?![\w])', txt)}

# ---------- checks ----------
checks = {f['id']: [] for f in FIELDS}
def chk(fid, ok, msg): checks[fid].append(('PASS' if ok else 'FAIL', msg))
if val('A01'): chk('A01', norm(folder_name).split()[0] in norm(val('A01')), f'name vs folder "{folder_name}"')
if val('A02'):
    n = re.findall(r'\d+(?:\.\d+)?', str(val('A02'))); chk('A02', bool(n) and 0 <= float(n[0]) <= 120, 'age within 0–120')
adm_dates = sorted({n_date(i.get('clinical_datetime') or i.get('quote')) for i in items(F('C01'))} - {None})
if F('C01').get('status') == 'FOUND':
    chk('C01', bool(adm_dates) and all(WINDOW[0] <= d <= WINDOW[1] for d in adm_dates),
        'every documented ICU-admission date inside 15/07–15/08/2026: ' + ', '.join(f'{d[2]:02d}/{d[1]:02d}' for d in adm_dates))
else:
    chk('C01', False, 'eligibility not confirmable: no ICU admission date found')
if val('J02') and adm_dates:
    jd = n_date(val('J02')); chk('J02', bool(jd) and jd >= adm_dates[0], 'outcome date on/after ICU admission')
death = bool(re.match(r"\s*(1\.\s*)?death\b", str(val('J01') or ''), re.I)) and 'non-death' not in str(val('J01') or '').lower()
for k in ('K01', 'K02', 'K03', 'K04'):
    if val('J01'): chk(k, (F(k).get('status') != 'NOT_APPLICABLE') if death else True, 'section K consistent with J01')
RANGES = {'L01': (25, 45), 'L03': (0, 300), 'L04': (0, 80), 'L06': (6.5, 8.0), 'L07': (100, 200), 'L08': (1, 10), 'L10': (5, 75), 'L11': (0, 200)}
for fid, (lo, hi) in RANGES.items():
    if val(fid):
        s = re.sub(r'\([^)]*\)|\b(?:P|R|WA)\d{2}\b|\d{1,2}:\d{2}', ' ', str(val(fid)))
        s = re.sub(r'\b(\d{1,2})\s*/\s*(\d{1,2})(\s*/\s*\d{2,4})?\b', lambda m: ' ' if int(m[2]) <= 12 else m[0], s)
        bad = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', s) if not lo <= float(x) <= hi]
        chk(fid, not bad, f'values within plausible range {lo}–{hi}' + (f' — check {bad[:3]}' if bad else ''))

# ---------- route ----------
LBL = {'GREEN': '🟢 Auto', 'YELLOW': '🟡 Student review', 'PURPLE': '🟣 Specialist review', 'RED': '🔴 Search required', 'NA': 'Not applicable'}
GATE = {'GREEN': 'None', 'YELLOW': 'Student review', 'PURPLE': 'Need to review by specialist', 'RED': 'Mandatory search', 'NA': 'None'}
def route(f, x):
    st = x.get('status'); why = []
    if st in ('NOT_FOUND', 'CANNOT_ASSESS', 'MISSING'): return 'RED', [st.replace('_', ' ').lower()]
    if st == 'NOT_APPLICABLE':
        trig = str(x.get('trigger') or '')
        tf = re.findall(r'\b[A-L]\d{2}\b', trig)
        return ('NA', ['form logic: ' + trig]) if (not tf or all(F(t).get('status') == 'FOUND' for t in tf)) else ('YELLOW', ['N/A trigger not FOUND'])
    if f['route'] == 'SPECIALIST': return 'PURPLE', ['clinical-interpretation field']
    if not quote_ok(x): why.append('no page ID + verbatim quote')
    if has_q(x): why.append('uncertain characters [?]')
    if x.get('conflict') or str(x.get('value', '')).upper().startswith('CONFLICT'): why.append('conflicting sources')
    if wa_only(x): why.append('WhatsApp-only evidence')
    if any(s == 'FAIL' for s, _ in checks[f['id']]): why.append('a check failed')
    if f['route'] != 'AUTO_OK': why.append('field type always reviewed by a student')
    if f['id'] in ('E04', 'E08'): why.append('written GCS total — convention pending')
    if (f['id'] in ('A07', 'C01', 'C02', 'E01', 'E02', 'E03', 'E04', 'H02') or f['id'].startswith('L')) and str(x.get('time_label') or '').lower() != 'at/near icu admission':
        why.append(f"temporal status '{x.get('time_label') or 'unresolved'}' — not locked to ICU admission")
    if not why and len(indep_sources(x)) < 2: why.append('single source only (no second independent page)')
    return ('YELLOW', why) if why else ('GREEN', [f'corroborated by {len(indep_sources(x))} independent sources'])


# ---------- sources ----------
msgs = {m['i']: m for w in WA['hits'] for m in w['messages']}
WA_MSG = {k: v['msg'] for k, v in META.get('wa', {}).items()}
WA_PHRASE = {k: v.get('phrase', '') for k, v in META.get('wa', {}).items()}
sources = {}
for pid, inv in INV.items():
    p = PAGES.get(pid, {}); im = page_img(pid)
    sources[pid] = {'kind': 'chart', 'file': inv['file'], 'type': p.get('page_type', ''), 'own': p.get('ownership', ''), 'read': p.get('readability', ''),
                    'date': p.get('document_datetime') or '', 'drive': inv.get('drive_link'), 'dup': inv.get('duplicate_of'),
                    'full': add_asset(im, 1600, 78), 'thumb': add_asset(im, 360, 70)}
used_wa = set()
for f in FIELDS:
    for i in items(F(f['id'])):
        if str(i.get('source', '')) in WA_MSG: used_wa.add(i['source'])
for w in sorted(used_wa):
    m = msgs[WA_MSG[w]]; n = WA_TXT.count(WA_PHRASE[w])
    sources[w] = {'kind': 'wa', 'sender': m['sender'], 'ts': f"{m['date']}, {m['time']}", 'text': m['text'], 'phrase': WA_PHRASE[w],
                  'uniq': 'Unique in the exported transcript' if n == 1 else f'Appears {n}× — use the timestamp', 'own': 'Confirmed',
                  'ownWhy': 'explicit patient label in the message' + (f" ({META['wa'][w]['note']})" if META['wa'][w].get('note') else ''), 'chain': 'CC-' + w}


# ---------- search guidance (how hard to search, where) ----------
# Yes/No fields where the team's convention applies: searched + not documented → coded as the "absent" value.
ABSENT = {'D01': 'No', 'D03': 'No', 'D05': 'No', 'D07': 'No', 'D11': 'No', 'F01': 'None', 'F03': 'No previous operation',
          'G02': 'No', 'H03': 'No', 'H06': 'No', 'I01': 'No', 'I05': 'No', 'I07': 'No'}
PT_MAP = [(r'admission (sheet|form|card|note|record)|icu admission', 'ADM'), (r'progress', 'PROG'), (r'nursing', 'NURS'),
          (r'drug|medication|treatment (chart|form)', 'DRUG'), (r'flow ?sheet|vital', 'FLOW'), (r'ventilator', 'VENT'), (r'\blab', 'LAB'),
          (r'\babg\b', 'ABG'), (r'radiolog', 'RAD'), (r'operation', 'OP'), (r'consult', 'CONS'), (r'death|discharge (note|summary)', 'DEATH'),
          (r'register', 'REG'), (r'referral', 'REF'), (r'dialysis', 'DIAL')]
def ptoks(t):
    t = str(t or '').lower()
    return {k for rx, k in PT_MAP if re.search(rx, t)}
# learned knowledge base: in which page types each field has been FOUND, across all patients read so far
try: KB = json.load(open(KB_PATH))
except Exception: KB = {}
KB[folder_name] = {}
for f in FIELDS:
    types = sorted({PAGES[str(i.get('source'))].get('page_type', '').split(':')[0].split('(')[0].strip()
                    for i in items(F(f['id'])) if str(i.get('source')) in PAGES})
    if F(f['id']).get('status') == 'FOUND' and types: KB[folder_name][f['id']] = types
os.makedirs(os.path.dirname(KB_PATH), exist_ok=True); json.dump(KB, open(KB_PATH, 'w'), ensure_ascii=False, indent=1)
def learned(fid):
    c = {}
    for pat, d in KB.items():
        for t in d.get(fid, []): c[t] = c.get(t, 0) + 1
    n = len(KB)
    return [f'{t} ({k} of {n} patient{"s" if n > 1 else ""})' for t, k in sorted(c.items(), key=lambda kv: -kv[1])]
def guidance(f, x):
    st = x.get('status')
    if st not in ('NOT_FOUND', 'CANNOT_ASSESS', 'MISSING'): return None
    want = set().union(*[ptoks(u) for u in f.get('usual_pages', '').split(',')]) if f.get('usual_pages') else set()
    rel = [pid for pid, p in PAGES.items() if ptoks(p.get('page_type')) & want]
    rel_poor = [pid for pid in rel if PAGES[pid].get('readability') in ('poor', 'partial')]
    unknown_blur = sorted(pid for pid, p in PAGES.items() if p.get('readability') == 'poor' and not ptoks(p.get('page_type')))
    g = {'learned': learned(f['id']), 'usual': f.get('usual_pages', ''), 'absent': ABSENT.get(f['id']), 'blurred': unknown_blur}
    if st == 'CANNOT_ASSESS' or (want and not rel):
        g.update(level='NOTPHOTO', label='📷 Not in the photos', pages=[],
                 text=f"The page type that normally holds this ({x.get('missing_page_type') or f.get('usual_pages')}) was not photographed. "
                      "Searching these photos cannot find it → re-photograph, or mark “Missing — ask ICU”.")
    elif rel_poor and len(rel_poor) == len(rel):
        g.update(level='HIGH', label='🔎 Search needed — the right page is hard to read', pages=sorted(rel_poor),
                 text='The only pages of the right type are partly unreadable. Look carefully at them before deciding.')
    elif rel:
        extra = f" Also glance at {', '.join(sorted(rel_poor))} (partly readable)." if rel_poor else ''
        g.update(level='LOW', label='✓ Quick confirm — probably truly not written', pages=sorted(rel),
                 text='The page type that normally holds this was photographed, is readable, and was searched.' + extra
                      + (f" If it is not there → “Searched — not documented → {ABSENT[f['id']]}”." if f['id'] in ABSENT else ' If it is not there → “Searched — not documented”.'))
    else:
        g.update(level='MEDIUM', label='🔎 Search the whole record', pages=sorted(PAGES),
                 text='This field has no fixed page type. Skim all pages.')
    return g

# ---------- fields ----------
SECT = {'A': 'A · Patient identification', 'B': 'B · Type of emergency', 'C': 'C · Admission details', 'D': 'D · Condition at ICU admission / major support',
        'E': 'E · Glasgow Coma Scale', 'F': 'F · Past medical & surgical history', 'G': 'G · Drug history', 'H': 'H · Blood products & anemia',
        'I': 'I · ICU complications', 'J': 'J · Final outcome', 'K': 'K · Cause of death', 'L': 'L · APACHE II (raw values)'}
TEMP = lambda t: {'at/near icu admission': 'at/near ICU admission', 'pre-icu': 'pre-ICU', 'outside admission window': 'outside admission window'}.get(str(t or '').lower(), 'time unresolved' if t else '')
sections = {k: {'id': k, 'title': v, 'form': add_asset(Image.open(os.path.join(proj, 'v3', FORM[k])), 1000, 85) if k in FORM else '', 'fields': []} for k, v in SECT.items()}
counts = {}
for f in FIELDS:
    x = F(f['id']); st = x.get('status', 'MISSING'); rt, why = route(f, x); counts[rt] = counts.get(rt, 0) + 1
    by_src = {}
    for it in items(x): by_src.setdefault(str(it.get('source', '')), []).append(it)
    ev = []
    for src, its in by_src.items():
        if src not in sources: continue
        q = ' · '.join(i.get('quote', '') for i in its if i.get('quote'))
        when = ' · '.join(dict.fromkeys(str(i['clinical_datetime']) for i in its if i.get('clinical_datetime')))
        crop = ''
        if sources[src]['kind'] == 'chart':
            c = stacked([crop_box(src, i.get('bbox')) for i in its])
            if c is not None: crop = add_asset(c, 900, 84)
        ev.append({'src': src, 'quote': q, 'when': when, 'crop': crop})
    if st == 'FOUND': value = str(x.get('value', ''))
    elif st == 'NOT_FOUND': value = 'Not found in the photographed pages'
    elif st == 'CANNOT_ASSESS': value = 'Cannot assess — page type not photographed'
    elif st == 'NOT_APPLICABLE': value = 'Not applicable — ' + str(x.get('trigger', ''))
    else: value = '—'
    sel = opts_in(f, x.get('value')) if st == 'FOUND' else set()
    un = x.get('unreadable'); un = ', '.join(map(str, un)) if isinstance(un, list) else (un or '')
    sections[f['id'][0]]['fields'].append({
        'id': f['id'], 'name': f['label'], 'options': [[o, o in sel] for o in f['options']], 'route': rt, 'readerStatus': st, 'value': value,
        'why': why, 'checks': checks[f['id']], 'ev': ev, 'searched': [str(p) for p in (x.get('searched') or [])], 'unreadable': un,
        'missing': str(x.get('missing_page_type') or ''), 'usual': f.get('usual_pages', ''), 'temporal': TEMP(x.get('time_label')),
        'conflict': bool(x.get('conflict') or str(x.get('value', '')).upper().startswith('CONFLICT')), 'comment': str(x.get('comment') or ''),
        'guide': guidance(f, x), 'absent': ABSENT.get(f['id'])})

# ---------- WhatsApp chains ----------
def chain(title, lo, hi, cur, notes):
    its = []
    for i in range(lo, hi + 1):
        m = msgs.get(i)
        if m: its.append({'time': f"{m['date']} {m['time']}", 'text': m['text'] if len(m['text']) < 180 else m['text'][:180] + '…', 'assessment': notes.get(i, ''), 'cur': i == cur})
    return {'title': title, 'rule': 'From the previous explicitly named patient to the next one; unlabeled attachments belong to the preceding named patient.', 'items': its}
chains = {}
for w, c in META.get('chains', {}).items():
    if w not in used_wa: continue
    notes = {int(k): v for k, v in c.get('notes', {}).items()}
    for lo, hi, t in c.get('range_notes', []): notes.update({i: t for i in range(lo, hi + 1)})
    chains['CC-' + w] = chain(c['title'], c['lo'], c['hi'], META['wa'][w]['msg'], notes)

poor = sorted(k for k, s in sources.items() if s.get('read') == 'poor')
missing = sorted({str(F(f['id']).get('missing_page_type')) for f in FIELDS if F(f['id']).get('status') == 'CANNOT_ASSESS'} - {'None', ''})
ok = bool(checks['C01']) and all(s == 'PASS' for s, _ in checks['C01'])
data = {
    'meta': {'patient': folder_name, 'protocol': 'v4.1', 'reader': 'Claude Opus (single reader)', 'reviewDate': datetime.date.today().strftime('%d/%m/%Y'),
             'admission': (lambda d, t: (d or 'unresolved') + (' · ' + t if t and len(t) <= 12 and 'CONFLICT' not in t.upper() else (' · time conflicting — see C02' if t else '')))(
                 None if 'CONFLICT' in str(val('C01') or '').upper() else val('C01'), str(val('C02') or '')),
             'eligibility': {'ok': ok, 'label': 'Included' if ok else 'Eligibility needs decision', 'detail': ('; '.join(m for _, m in checks['C01']))[:1].upper() + ('; '.join(m for _, m in checks['C01']))[1:]},
             'sourceCounts': {'chart': len(INV), 'wa': len(used_wa)}},
    'counts': counts, 'sections': list(sections.values()), 'sources': sources, 'chains': chains,
    'timeline': [{'when': t.get('datetime', ''), 'what': t.get('event', ''), 'src': t.get('sources') or [], 'conflict': t.get('conflict')} for t in R.get('timeline') or []],
    'pageTypes': sorted({s['type'].split(':')[0].split('(')[0].strip() for s in sources.values() if s['kind'] == 'chart' and s['type']}),
    'missingTypes': missing,
    'waReview': {**META.get('wa_review', {}), 'Used': ', '.join(sorted(used_wa)) + ' — confirmed by explicit label'},
    'notes': [{'title': 'Method (protocol v4.1)', 'text': 'Single reader (Claude Opus) reads every page and returns FOUND / NOT FOUND / CANNOT ASSESS / N/A with page ID + verbatim quote. The AI never writes “Not documented”. Scripts run the checks and routing. 🟢 needs ≥2 independent sources, a verbatim quote, passing checks and (for admission/APACHE fields) an admission-time lock.'},
              {'title': 'APACHE II', 'text': 'Total withheld — time-window decision pending (§15.1); recommended worst value in first 24 h after ICU admission.'},
              {'title': 'Photographs', 'text': f"Poor photos: {', '.join(poor) or 'none'}. Page types not photographed: {'; '.join(missing) or 'none'}."}],
    'qc': {'Chart pages': len(INV), 'WhatsApp messages used': len(used_wa), 'Routes': ' · '.join(f'{k}: {v}' for k, v in counts.items()),
           'Failed checks': '; '.join(f'{k}: {m}' for k, v in checks.items() for s, m in v if s == 'FAIL') or 'none', 'Exact duplicates': sum(1 for s in sources.values() if s.get('dup')) or 'none'},
    'assets': assets}
spec = []
for sec in sections.values():
    for fl in sec['fields']:
        if fl['route'] == 'PURPLE':
            spec.append({'patient': folder_name, 'register_no': META.get('register_no', ''), 'field': fl['id'], 'field_name': fl['name'],
                         'why': 'clinical-interpretation field', 'proposed_value': fl['value'],
                         'evidence': ' | '.join(f"{e['src']}: “{e['quote']}”" for e in fl['ev']),
                         'links': ' '.join(sources[e['src']].get('drive') or '' for e in fl['ev'] if sources[e['src']].get('kind') == 'chart'),
                         'origin': 'auto (🟣)', 'status': 'open', 'answer': '', 'date': datetime.date.today().strftime('%d/%m/%Y')})
json.dump(spec, open(os.path.join(pdir, 'ledger_specialist.json'), 'w'), ensure_ascii=False, indent=1)
data['meta']['registerNo'] = META.get('register_no', '')
json.dump([{**fl, 'ev': [{**e, 'crop': '', 'drive': sources[e['src']].get('drive')} for e in fl['ev']], 'guide': fl.get('guide')} for sec in sections.values() for fl in sec['fields']],
          open(os.path.join(pdir, 'review_fields.json'), 'w'), ensure_ascii=False, indent=1)
blob = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
page = TPL.replace('__DATA__', blob, 1).replace('<title>ICU Research Review</title>', f'<title>{html.escape(folder_name)} — ICU Research Review</title>', 1)
open(out_path, 'w', encoding='utf-8').write(page)
print(out_path, f'{len(page) / 1e6:.1f} MB', counts, 'assets', len(assets))
