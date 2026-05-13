# 1. Workflow Name

Bow Retrieval / Verification Workflow

---

# 2. Purpose

Verify whether a query bow image matches an existing registered bow using embeddings and similarity search, and return ownership + traceability information.

---

# 3. Trigger

A user submits a bow image for verification through the UI or API.

---

# 4. Preconditions

- User is authenticated
- Query image is provided
- Embedding model is available
- Vector database is operational
- Metadata service is reachable

---

# 5. Actors/Services Involved

- UI
- Orchestrator Service
- Preprocessing Service
- Model Service
- Retrieval Service
- Metadata Service
- Vector Database
- PostgreSQL Database

---

# 6. Inputs

- Query bow image
- Optional search parameters:
  - top_k
  - similarity threshold

---

# 7. Outputs

- Match decision:
  - Registered Match
  - Possible Match
  - No Match
- Similarity scores
- Top-k matched bow IDs
- Ownership information
- Contract / traceability data

---

# 8. Main Workflow Steps

## Step 1 — Query Submission

User uploads bow image via UI.

---

## Step 2 — Request Validation

Orchestrator validates image and request parameters.

---

## Step 3 — Image Preprocessing

Image is sent to preprocessing service:
- resize
- normalize
- validate quality
- optional background removal

Invalid images are rejected early.

---

## Step 4 — Embedding Generation

Processed image is sent to model service.

Model service:
- runs inference
- generates embedding vector

---

## Step 5 — Similarity Search

Embedding is sent to retrieval service.

Retrieval service:
- queries vector database
- retrieves top-k nearest embeddings
- computes similarity scores

---

## Step 6 — Match Decision

System applies threshold logic:

- If similarity ≥ registered threshold → Registered Match
- If similarity ≥ possible match threshold → Possible Match
- Else → No Match

---

## Step 7 — Metadata Enrichment

If matches exist:
- fetch ownership data
- fetch contract details
- fetch registration history

---

## Step 8 — Response Generation

Orchestrator aggregates:
- match results
- similarity scores
- metadata information

Returns final response.

---

# 9. Alternative Flows

## No Matches Found

System returns "No Match" with empty metadata.

---

## Multiple Close Matches

System returns top-k ranked candidates with "Possible Match".

---

## Service Failure

Workflow fails and returns partial or error response.

---

# 10. Data Produced

- Query embeddings
- Similarity scores
- Match decision
- Retrieved bow IDs
- Ownership and contract data
- Query logs