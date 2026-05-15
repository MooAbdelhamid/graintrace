# GrainTrace – Wood Grain Identification Protocol (Head Region Focus)

## Version
0.1 – Data Collection Specification (Focused on Wood Grain ROI)

---

# 1. Objective

GrainTrace aims to identify and match musical bows by analyzing stable wood grain patterns, primarily in the head.

The system does NOT rely on full-object recognition, but instead on:
- localized texture signatures
- micro-grain structure consistency
- varnish + wear pattern fingerprints

---

# 2. Region of Interest (ROI) Definition

- bow head

---

# 3. Image Capture Requirements

## 3.1 Required Image Set per Bow

### A. Primary ROI Views
- head wood (left side)
- head wood (right side)

### B. Macro Texture Capture
- Extreme close-up grain image (1–2 samples)


## 3.2 Capture Constraints

- Fixed camera orientation (shaft vertical alignment)
- Consistent framing across all bows
- No motion blur
- Uniform background (matte neutral preferred)

## 3.3 Capture Specifications

- Minimum: 1600 × 1200 px
- Recommended: 3000 × 2000 px or higher

---

# 4. Lighting Requirements

## Preferred Setup
- Diffused source preferred
- Emphasis on surface texture visibility

## Avoid
- Flat frontal lighting
- Harsh shadows

---

# 5. Variations

- Different distances
- Different angles

---

# 6. Data Structure (Per Bow)

## 6.1 Structure 1

- head_left
- head_right
- macro_grain_closeup

## 6.1 Structure 2

- head_left
- head_right

---

# 7. Labeling Scheme

Each image must include:

- bow_id
- view_side (left/right/context)

---

# 8. Quality Control Rules

Reject capture if:
- blur is present
- grain structure is not visible
- lighting flattens texture
- shaft alignment is inconsistent

---

# 9. Data Modeling Implication

This dataset is optimized for:
- texture-based embedding learning
- contrastive learning (same bow vs different bow)
- multi-instance aggregation per bow **TBD**