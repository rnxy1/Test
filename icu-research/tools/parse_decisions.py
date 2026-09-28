"""Turn the text from “Copy for Claude” into decisions.json (no AI).
  python3 parse_decisions.py <pasted.txt> <patient_dir>
Free-text notes are kept verbatim; Claude reads them afterwards and turns each into a value (logged in the audit file).
"""
import sys, re, json, os
ACT = {'ACCEPT': 'accept', 'CORRECT': 'correct', 'SEARCHED — NOT DOCUMENTED': 'searched_no', 'MISSING — ASK ICU': 'ask_icu',
       '→ SPECIALIST': 'escalate', 'NOT APPLICABLE': 'na'}
txt, pdir = open(sys.argv[1], encoding='utf-8').read(), sys.argv[2]
head = txt.strip().splitlines()[0]
who = (re.search(r'reviewer (\S+)', head) or [None, ''])[1]
date = (re.search(r'(\d{2}/\d{2}/\d{4})', head) or [None, ''])[1]
out, pending = {}, []
for line in txt.splitlines()[1:]:
    m = re.match(r'\s*([A-L]\d{2}):\s*(.*)$', line)
    if not m:
        if line.startswith('NO DECISION YET'): pending = re.findall(r'[A-L]\d{2}', line)
        continue
    fid, rest = m[1], m[2]; d = {'i': who, 'd': date}
    for part in [p.strip() for p in rest.split(' | ')]:
        if part.startswith('note:'): d['n'] = part[5:].strip(); continue
        if part.startswith('BLIND CHECK'):
            b = re.match(r'BLIND CHECK read "(.*)" · (\w+)', part); d['bv'], d['bm'] = (b[1], b[2] == 'match') if b else (part, False); continue
        for k, a in ACT.items():
            if part.startswith(k):
                d['a'] = a; v = part[len(k):].strip(' —→')
                if a == 'correct': d['v'] = v
                if a == 'searched_no' and v: d['coded'] = v
                break
    out[fid] = d
json.dump(out, open(os.path.join(pdir, 'decisions.json'), 'w'), ensure_ascii=False, indent=1)
print(f'{len(out)} decisions ({sum(1 for d in out.values() if d.get("n"))} with notes), {len(pending)} still pending, reviewer {who or "?"}')
