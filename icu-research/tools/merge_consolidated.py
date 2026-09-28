"""Merge parallel consolidation parts into consolidated.json (no AI).
  python3 merge_consolidated.py <reader_dir>"""
import sys, os, json, glob
rd = sys.argv[1]; out = {'fields': {}, 'timeline': [], 'page_types_present': []}
for f in sorted(glob.glob(os.path.join(rd, 'consolidated_*.json'))):
    d = json.load(open(f))
    out['fields'].update(d.get('fields', {}))
    if d.get('timeline'): out['timeline'] = d['timeline']
    out['page_types_present'] = sorted(set(out['page_types_present']) | set(d.get('page_types_present') or []))
    out.setdefault('patient', d.get('patient')); out['reader'] = d.get('reader', 'A')
fields = [f['id'] for f in json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(rd)))), 'fields.json')))]
missing = [f for f in fields if f not in out['fields']]
json.dump(out, open(os.path.join(rd, 'consolidated.json'), 'w'), ensure_ascii=False, indent=1)
print(f"{len(out['fields'])} fields merged; missing: {missing or 'none'}")
