# 1. Workflow Name

Bow Registration Workflow

---

# 2. Purpose

Register a new bow into the system by generating embeddings, checking for duplicates, and storing metadata and ownership information.

---

# 3. Trigger

An admin submits a new bow registration request through the UI or API.

---

# 4. Preconditions

- User is authenticated
- Bow images are provided
- Required metadata is available
- Internal services are operational

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

- Bow images
- Owner information
- Manufacturer information
- Bow reference ID

---

# 7. Outputs

- Generated bow ID
- Registration confirmation
- Duplicate detection result
- Stored embeddings
- Stored metadata records

---

# 8. Main Workflow Steps

## Step 1 — Request Submission

Admin uploads bow images and metadata through the UI.

---

## Step 2 — Request Validation

Orchestrator validates request structure and required fields.

---

## Step 3 — Image Preprocessing

Images are sent to the preprocessing service for:
- resizing
- normalization
- quality validation
- optional background removal

Invalid images are rejected.

---

## Step 4 — Embedding Generation

Processed images are sent to the model service.

The model service:
- performs inference
- generates embedding vectors

---

## Step 5 — Duplicate Detection

Generated embeddings are sent to the retrieval service.

The retrieval service:
- performs vector similarity search
- retrieves nearest matches
- applies duplicate thresholds

---

## Step 6 — Registration Decision

If no duplicate exceeds the similarity threshold:
- registration continues

Otherwise:
- registration is flagged for manual review or rejected

---

## Step 7 — Data Persistence

System stores:
- embeddings in Qdrant
- metadata in PostgreSQL
- ownership records
- contracts
- registration history

---

## Step 8 — Response Generation

Orchestrator aggregates responses and returns:
- registration status
- generated bow ID
- duplicate detection results

---

# 9. Alternative Flows

## Duplicate Match Detected

Request is rejected before inference.

---

## Invalid Image Quality

Request is rejected before inference.

---

## Metadata Validation Failure

Registration request is rejected.

---

# 10. Data Produced

- Embedding vectors
- Bow registration ID
- Ownership records
- Query logs
- Registration history
