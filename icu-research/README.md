# ICU Arbaeen research — extraction tooling (protocol v4.1)

Code and templates only. **No patient data belongs in this repository** — photos, reader outputs,
review pages, decisions and lists live in the team's Google Drive (see the protocol file there:
`00 - ICU RESEARCH AI WORKFLOW - READ ME FIRST.md`).

| File | Purpose |
|---|---|
| `fields.json` | A–L form fields: wording, options, type, routing, usual page types (`tools/make_fields.py` regenerates it) |
| `reader_protocol.md` | Instructions for the Opus reader subagents (page reading in parallel chunks, split consolidation) |
| `tools/prep.py` | EXIF rotation, ≤2576 px reading copies, SHA-256 duplicates, P/R IDs |
| `tools/wa_search.py` | WhatsApp transcript search + context windows |
| `tools/crop.py` | reader zoom helper (optional rotation) |
| `tools/merge_consolidated.py` | merges the parallel consolidation parts |
| `tools/build_review.py` | checks, routing, search guidance, learned page locations → review page |
| `tools/parse_decisions.py` | “Copy for Claude” text → `decisions.json` |
| `tools/ledger.py` | study-wide specialist / ICU-question lists (merge keeps team answers) |
| `tools/form_sections.py` | cuts sections A–L out of the form PDF |
| `tools/compare.py` | v4.0 two-reader comparison (kept for reference) |
| `templates/review_v41.html` | review page template (v3.1 design language, v4.1 workflow) |
