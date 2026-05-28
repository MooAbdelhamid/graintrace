# Bow photos for the demo

Drop your bow photos here using the naming convention:

```
BOW-001.jpg          # primary photo of bow 001
BOW-001_front.jpg    # any extra views, optional
BOW-001_side.jpg
BOW-002.jpg
BOW-003.jpg
...
```

Anything starting with `BOW-001` (any case, any extension `.jpg`/`.jpeg`/`.png`)
will be picked up automatically and shown in the Browse and Identify screens
for that bow. Multiple files per bow are supported.

If a bow has no matching files, the app falls back to a generated placeholder
silhouette so the UI is never empty.

Seeded demo bows (so you know which IDs to use):
- BOW-001 — François Xavier Tourte
- BOW-002 — Eugène Sartory
- BOW-003 — Dominique Peccatte
- BOW-004 — James Tubbs
- BOW-005 — Albert Nürnberger

When the team's real backend is wired up, photos move to proper storage and
this folder becomes irrelevant.
