---
title: GrainTrace
emoji: 🎻
colorFrom: yellow
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---

# GrainTrace — Streamlit UI

A Streamlit prototype of the GrainTrace UI: enrol a bow, identify an unknown
bow against the database, and browse the registered bows. The backend is
**mocked in-memory** (random embeddings, cosine matching) so the app runs
end-to-end without the model service — swap `lib/mock_backend.py` for real
HTTP calls when the model is ready.

## Run locally

```bash
# from inside graintrace_ui/
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app opens at `http://localhost:8501`.

## Screens

1. **Home** — three cards linking to the main flows + quick database stats.
2. **📝 Enrol Bow** — three steps: passport details → photo upload with the
   "good photo" preflight check → review and confirm.
3. **🔍 Identify Bow** — upload one or more query photos → preflight →
   top-3 ranked candidates with confidence scores and side-by-side compare.
   A fallback "register as new" button hands off to Enrol.
4. **📚 Browse Database** — filterable table of every bow, plus a detail view
   with passport, photos, and a preview of the bow's embedding vector.

## Project layout

```
graintrace_ui/
├── streamlit_app.py        # Home + navigation
├── pages/
│   ├── 1_Enrol_Bow.py
│   ├── 2_Identify_Bow.py
│   └── 3_Browse_Database.py
├── lib/
│   ├── mock_backend.py     # in-memory "database" + mock model
│   ├── photo_check.py      # "good photo" preflight
│   └── style.py            # palette, CSS, shared header helpers
├── assets/bows/            # drop BOW-001.jpg etc. here
├── .streamlit/config.toml  # theme matching the GrainTrace deck
└── requirements.txt
```

## Replacing the mock backend

Each function in `lib/mock_backend.py` defines a stable contract:

- `list_bows()` → list of `BowPassport`
- `get_bow(bow_id)` → one `BowPassport` or `None`
- `enroll_bow(passport_fields, photos)` → `bow_id`
- `query_bow(image_bytes_list, top_k)` → list of `MatchResult`
- `compute_embedding(image_bytes)` → 256-d float list
- `aggregate_embeddings(embs)` → 256-d float list (mean pool)

To plug in the real backend later: rewrite each function as an HTTP call
against the FastAPI service, keep the same return shapes, and the pages won't
need any changes.

## Photo-rejection criteria (v2 spec)

`lib/photo_check.py` enforces the team's final criteria:

- Resolution ≥ 10 MP (recommended ≥ 12 MP)
- Sharp focus on head — no motion blur
- Head fully visible and centred
- No heavy glare covering the wood grain

ID information is checked at the form level (`Maker` field required).
