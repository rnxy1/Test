"""Search the WhatsApp transcript for a patient's name variants / chart numbers (no AI)."""
import re, sys, json
sys.path.insert(0, __import__('os').path.dirname(__file__))
from arabic import norm
path, out, *terms = sys.argv[1:]
strong = [norm(t) for t in terms if not t.startswith('~')]
weak = [norm(t[1:]) for t in terms if t.startswith('~')]
msgs, cur = [], None
hdr = re.compile(r'^‎?\[(\d\d/\d\d/\d{4}), ([^\]]+)\] ([^:]+): (.*)$')
for line in open(path, encoding='utf-8'):
    m = hdr.match(line.rstrip('\n'))
    if m:
        cur = {'i': len(msgs), 'date': m[1], 'time': m[2], 'sender': m[3].strip(), 'text': m[4]}
        msgs.append(cur)
    elif cur:
        cur['text'] += '\n' + line.rstrip('\n')
for m in msgs:
    m['attach'] = re.findall(r'<attached: ([^>]+)>', m['text'])
hits = []
for m in msgs:
    n = norm(m['text'])
    s = [t for t in strong if t in n]
    w = [t for t in weak if re.search(r'(^|\s)' + re.escape(t) + r'(\s|$)', n)]
    if s or w:
        hits.append((m['i'], 'strong' if s else 'weak', s + w))
windows = []
for i, kind, matched in hits:
    lo, hi = max(0, i - 6), min(len(msgs), i + 7)
    windows.append({'hit_msg': i, 'strength': kind, 'matched': matched,
                    'messages': msgs[lo:hi]})
json.dump({'terms': terms, 'n_messages': len(msgs), 'hits': windows}, open(out, 'w'), ensure_ascii=False, indent=1)
for w in windows:
    m = msgs[w['hit_msg']]
    print(w['strength'], w['hit_msg'], m['date'], m['time'], m['sender'], '|', m['text'][:160].replace('\n', ' / '), '| attach:', m['attach'])
