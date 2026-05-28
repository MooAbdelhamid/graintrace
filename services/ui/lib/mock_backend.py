"""In-memory mock backend that mimics the real GrainTrace API contract.

When the real backend exists, swap each function for an HTTP call but keep the
same signatures and return shapes — the UI doesn't need to change.
"""
from __future__ import annotations

import hashlib
import io
import os
import random
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import streamlit as st
from PIL import Image, ImageDraw, ImageFilter

EMBED_DIM = 256
TOP_K_DEFAULT = 3

# Where to look for real bow images. Drop JPEGs here named BOW-001.jpg,
# BOW-002.jpg etc., and they'll show up in the Browse + Identify screens.
ASSETS_DIR = Path(__file__).parent.parent / "assets" / "bows"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class BowPassport:
    bow_id: str
    maker: str
    year: str | None
    school: str | None
    owner: str | None
    notes: str
    registered_at: str
    photos: list[bytes] = field(default_factory=list)
    embedding: list[float] = field(default_factory=list)
    model_version: str = "mock-v0.1"


# ---------------------------------------------------------------------------
# Image loading — real assets if present, generated placeholder otherwise
# ---------------------------------------------------------------------------


def _load_bow_photos(bow_id: str) -> list[bytes]:
    """Look in assets/bows/ for files named {bow_id}*.jpg / .jpeg / .png.

    Examples that all match BOW-001:
        BOW-001.jpg
        BOW-001_front.jpg
        BOW-001-2.png
    """
    if not ASSETS_DIR.exists():
        return []
    matches = []
    for ext in ("jpg", "jpeg", "png"):
        matches.extend(sorted(ASSETS_DIR.glob(f"{bow_id}*.{ext}")))
        matches.extend(sorted(ASSETS_DIR.glob(f"{bow_id}*.{ext.upper()}")))
    return [p.read_bytes() for p in matches]


def _placeholder_bow(seed: int) -> bytes:
    """Draw a simple stylised bow-head silhouette so the demo isn't empty."""
    rng = random.Random(seed)
    w, h = 1200, 400
    bg = (245, 240, 234)  # cream
    wood = (
        180 + rng.randint(-40, 20),
        110 + rng.randint(-30, 30),
        60 + rng.randint(-20, 30),
    )
    img = Image.new("RGB", (w, h), bg)
    d = ImageDraw.Draw(img)
    # bow head — rounded triangle
    head_poly = [(60, 200), (40, 320), (200, 320), (260, 220), (260, 180),
                 (240, 160), (180, 140), (110, 150)]
    d.polygon(head_poly, fill=wood)
    # stick
    d.polygon([(220, 195), (1180, 240), (1180, 260), (220, 215)], fill=wood)
    # white tip
    d.polygon([(40, 320), (45, 340), (200, 340), (200, 320)], fill=(245, 240, 230))
    img = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Session-state store (acts as our "database" for the demo)
# ---------------------------------------------------------------------------


def _store() -> dict[str, BowPassport]:
    if "bow_db" not in st.session_state:
        st.session_state["bow_db"] = {}
        _seed_demo_data()
    return st.session_state["bow_db"]


def _seed_demo_data():
    """Plant ~5 fake bows so the Browse / Identify screens aren't empty."""
    samples = [
        ("BOW-001", "François Xavier Tourte", "1810", "French",
         "Berliner Philharmoniker",
         "Reference master bow, ex-Joachim collection (demo entry)."),
        ("BOW-002", "Eugène Sartory", "1925", "French",
         "Private collector",
         "Silver-mounted; minor frog wear noted (demo entry)."),
        ("BOW-003", "Dominique Peccatte", "1855", "French",
         "Bow maker workshop",
         "Round stick, gold-mounted, fine condition (demo entry)."),
        ("BOW-004", "James Tubbs", "1880", "English",
         "Hochschule für Musik",
         "Octagonal stick, ebony frog (demo entry)."),
        ("BOW-005", "Albert Nürnberger", "1910", "German",
         "Anonymous",
         "Workshop bow, light wear (demo entry)."),
    ]
    rng = np.random.default_rng(42)
    for i, (bow_id, maker, year, school, owner, notes) in enumerate(samples):
        emb = rng.standard_normal(EMBED_DIM)
        emb = emb / np.linalg.norm(emb)

        # Use real photos from assets/bows/ if available, else placeholder
        photos = _load_bow_photos(bow_id)
        if not photos:
            photos = [_placeholder_bow(seed=i * 7 + 1)]

        st.session_state["bow_db"][bow_id] = BowPassport(
            bow_id=bow_id, maker=maker, year=year, school=school,
            owner=owner, notes=notes,
            registered_at=datetime.now().isoformat(timespec="seconds"),
            photos=photos, embedding=emb.tolist(),
        )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def list_bows() -> list[BowPassport]:
    return sorted(_store().values(), key=lambda b: b.bow_id)


def get_bow(bow_id: str) -> BowPassport | None:
    return _store().get(bow_id)


def next_bow_id() -> str:
    db = _store()
    n = len(db) + 1
    while f"BOW-{n:03d}" in db:
        n += 1
    return f"BOW-{n:03d}"


def compute_embedding(image_bytes: bytes) -> list[float]:
    """Stub: deterministic 'embedding' derived from the image hash.

    Same image → same vector. Different images → different vectors.
    Real backend will replace this with a model call.
    """
    h = hashlib.sha256(image_bytes).digest()
    seed = int.from_bytes(h[:8], "big") % (2**31 - 1)
    rng = np.random.default_rng(seed)
    v = rng.standard_normal(EMBED_DIM)
    v = v / np.linalg.norm(v)
    return v.tolist()


def aggregate_embeddings(embs: list[list[float]]) -> list[float]:
    """Mean-pool multiple per-photo embeddings into a single bow embedding."""
    arr = np.array(embs)
    m = arr.mean(axis=0)
    m = m / (np.linalg.norm(m) + 1e-9)
    return m.tolist()


def enroll_bow(passport_fields: dict[str, Any], photos: list[bytes]) -> str:
    """Compute embedding, store, return bow_id."""
    embs = [compute_embedding(p) for p in photos]
    agg = aggregate_embeddings(embs)
    bow_id = passport_fields.get("bow_id") or next_bow_id()
    bp = BowPassport(
        bow_id=bow_id,
        maker=passport_fields.get("maker", "Unknown"),
        year=passport_fields.get("year"),
        school=passport_fields.get("school"),
        owner=passport_fields.get("owner"),
        notes=passport_fields.get("notes", ""),
        registered_at=datetime.now().isoformat(timespec="seconds"),
        photos=photos,
        embedding=agg,
    )
    _store()[bow_id] = bp
    return bow_id


@dataclass
class MatchResult:
    bow_id: str
    score: float            # cosine similarity, 0..1
    confidence: str         # 'high' | 'medium' | 'low'
    passport: BowPassport


def query_bow(image_bytes_list: list[bytes], top_k: int = TOP_K_DEFAULT) -> list[MatchResult]:
    """Return ranked matches for one or more query photos."""
    q_embs = [compute_embedding(b) for b in image_bytes_list]
    q = np.array(aggregate_embeddings(q_embs))

    results: list[MatchResult] = []
    for bp in list_bows():
        v = np.array(bp.embedding)
        sim = float(np.dot(q, v))           # both unit-norm → cosine
        sim = (sim + 1) / 2                  # map -1..1 → 0..1 for UI
        sim = min(1.0, sim + random.uniform(-0.02, 0.02))
        if sim >= 0.85:
            confidence = "high"
        elif sim >= 0.65:
            confidence = "medium"
        else:
            confidence = "low"
        results.append(MatchResult(bow_id=bp.bow_id, score=sim,
                                   confidence=confidence, passport=bp))
    results.sort(key=lambda r: -r.score)
    return results[:top_k]
