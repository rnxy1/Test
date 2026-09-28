"""Study-wide lists that grow patient by patient (no AI).
  python3 ledger.py specialist <existing.csv|-> <patient_dir> <out.csv>
  python3 ledger.py icu        <existing.csv|-> <patient_dir> <out.csv>
The existing CSV is the current Google Sheet exported from Drive. Rows are keyed by (patient, field);
columns the team fills in (Status / Answer) are never overwritten.
"""
import sys, os, csv, json, datetime
SPEC_COLS = ['ID', 'Patient', 'Register no', 'Field', 'Field name', 'Why', 'Proposed value', 'Evidence (page: quote)', 'Drive links', 'Origin', 'Status', 'Specialist answer', 'Date added']
ICU_COLS = ['ID', 'Patient', 'Register no', 'ICU admission', 'Field', 'Field name', 'What is missing', 'Why missing', 'Reviewer note', 'Decided by', 'Date', 'Status', 'ICU answer']
TEAM_COLS = {'Status', 'Specialist answer', 'ICU answer'}
kind, existing, pdir, out = sys.argv[1:5]
cols = SPEC_COLS if kind == 'specialist' else ICU_COLS
rows = []
if existing != '-' and os.path.exists(existing):
    with open(existing, encoding='utf-8-sig') as fh: rows = list(csv.DictReader(fh))
key = lambda r: (r.get('Patient', ''), r.get('Field', ''))
idx = {key(r): r for r in rows}
today = datetime.date.today().strftime('%d/%m/%Y')
meta = json.load(open(os.path.join(pdir, 'meta.json')))
decisions = json.load(open(os.path.join(pdir, 'decisions.json'))) if os.path.exists(os.path.join(pdir, 'decisions.json')) else {}
review = json.load(open(os.path.join(pdir, 'review_fields.json')))          # written by build_review.py
new = []
for f in review:
    d = decisions.get(f['id'], {})
    if kind == 'specialist' and (f['route'] == 'PURPLE' or d.get('a') == 'escalate'):
        new.append({'Patient': meta['folder'], 'Register no': meta.get('register_no', ''), 'Field': f['id'], 'Field name': f['name'],
                    'Why': 'escalated by reviewer' + (f": {d.get('n')}" if d.get('n') else '') if d.get('a') == 'escalate' else 'clinical-interpretation field',
                    'Proposed value': f['value'], 'Evidence (page: quote)': ' | '.join(f"{e['src']}: “{e['quote']}”" for e in f['ev']),
                    'Drive links': ' '.join(e.get('drive') or '' for e in f['ev'] if e.get('drive')),
                    'Origin': 'escalated' if d.get('a') == 'escalate' else 'auto (🟣)', 'Status': 'open', 'Specialist answer': '', 'Date added': today})
    if kind == 'icu' and d.get('a') == 'ask_icu':
        new.append({'Patient': meta['folder'], 'Register no': meta.get('register_no', ''), 'ICU admission': meta.get('register_admission', ''),
                    'Field': f['id'], 'Field name': f['name'], 'What is missing': f['name'],
                    'Why missing': 'page type not photographed' if f['readerStatus'] == 'CANNOT_ASSESS' else 'searched by the team, not found',
                    'Reviewer note': d.get('n', ''), 'Decided by': d.get('i', ''), 'Date': d.get('d', today), 'Status': 'open', 'ICU answer': ''})
added = 0
for r in new:
    k = key(r)
    if k in idx:
        for c in cols:
            if c not in TEAM_COLS and c != 'ID' and r.get(c): idx[k][c] = r[c]
    else:
        rows.append(r); idx[k] = r; added += 1
for i, r in enumerate(rows, 1): r['ID'] = r.get('ID') or str(i)
with open(out, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows)
print(f'{kind}: {len(rows)} rows ({added} new) -> {out}')
