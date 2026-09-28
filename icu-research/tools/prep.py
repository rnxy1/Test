"""Prepare reading copies (no AI): EXIF rotation, <=2576px long edge, SHA-256 duplicate detection, P-IDs."""
import sys, os, json, hashlib
from PIL import Image, ImageOps
pdir, ids_json = sys.argv[1], sys.argv[2]
drive_ids = json.load(open(ids_json))            # filename -> drive file id
raw, pages = os.path.join(pdir, 'raw'), os.path.join(pdir, 'pages')
os.makedirs(pages, exist_ok=True)
MAX = 2576
chart = sorted(f for f in os.listdir(raw) if f.startswith('IMG_'))
extra = sorted(f for f in os.listdir(raw) if not f.startswith('IMG_'))
inv, seen = [], {}
def add(fn, pid, kind):
    b = open(os.path.join(raw, fn), 'rb').read()
    h = hashlib.sha256(b).hexdigest()
    im = ImageOps.exif_transpose(Image.open(os.path.join(raw, fn))).convert('RGB')
    w0, h0 = im.size
    s = min(1, MAX / max(w0, h0))
    if s < 1: im = im.resize((round(w0 * s), round(h0 * s)), Image.LANCZOS)
    out = os.path.join(pages, pid + '.jpg')
    im.save(out, quality=90)
    dup = seen.get(h); seen.setdefault(h, pid)
    inv.append({'id': pid, 'file': fn, 'kind': kind, 'drive_id': drive_ids.get(fn),
                'drive_link': f"https://drive.google.com/file/d/{drive_ids.get(fn)}/view" if drive_ids.get(fn) else None,
                'sha256': h, 'duplicate_of': dup, 'orig_px': [w0, h0], 'read_px': list(im.size),
                'reading_copy': os.path.relpath(out, pdir)})
for i, fn in enumerate(chart, 1): add(fn, f'P{i:02d}', 'chart photo (patient folder)')
for i, fn in enumerate(extra, 1): add(fn, f'R{i:02d}', 'ICU register / ICU file list page (contains other patients\' rows)')
json.dump(inv, open(os.path.join(pdir, 'inventory.json'), 'w'), ensure_ascii=False, indent=1)
for r in inv: print(r['id'], r['file'], r['orig_px'], '->', r['read_px'], 'DUP of ' + r['duplicate_of'] if r['duplicate_of'] else '')
