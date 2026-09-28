"""Cut the A–L sections out of the authoritative form PDF (no AI).
  python3 form_sections.py <form.pdf> <out_dir>"""
import sys, os, json, pymupdf
pdf, out = sys.argv[1:3]; os.makedirs(out, exist_ok=True)
doc = pymupdf.open(pdf)
heads = {'A': 'A. Patient Identification', 'B': 'B. Type of Emergency', 'C': 'C. Admission Details', 'D': 'D. Condition at ICU',
         'E': 'E. Neurological Status', 'F': 'F. Past Medical', 'G': 'G. Drug History', 'H': 'H. Blood Products', 'I': 'I. ICU Complications',
         'J': 'J. Final Outcome', 'K': 'K. If Patient Died', 'L': 'L. APACHE II'}
pos = {}
for pno, page in enumerate(doc):
    for k, h in heads.items():
        r = page.search_for(h)
        if r and k not in pos: pos[k] = (pno, r[0].y0)
order = sorted(pos.items(), key=lambda kv: kv[1]); res = {}
for i, (k, (pno, y0)) in enumerate(order):
    page = doc[pno]; nxt = next((y for kk, (p, y) in order[i + 1:] if p == pno), None)
    clip = pymupdf.Rect(20, max(0, y0 - 6), page.rect.width - 20, (nxt - 4) if nxt else page.rect.height - 30)
    fn = f'form_{k}.png'; page.get_pixmap(clip=clip, dpi=130).save(os.path.join(out, fn)); res[k] = fn
json.dump(res, open(os.path.join(out, 'form_sections.json'), 'w')); print(res)
