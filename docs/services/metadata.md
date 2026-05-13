# 1. Purpose

Responsible for managing and retrieving bow metadata, ownership records, contracts, and traceability information.

---

# 2. Responsibilities

- Store bow metadata
- Store ownership information
- Store contract records
- Manage registration history
- Retrieve traceability records
- Retrieve ownership information
- Maintain query history
- Associate metadata with bow IDs

---

# 3. Inputs

- Bow IDs
- Ownership information
- Contract information
- Registration metadata
- Metadata query parameters

---

# 4. Outputs

- Ownership records
- Contract records
- Registration history
- Traceability information
- Metadata query results

---

# 5. Internal Components

- API Layer
- TBD

---

# 6. External Dependencies

- PostgreSQL
- Data Flow Manager

---

# 7. APIs/Interfaces

- POST /metadata/register
- GET /metadata/{bow_id}
- GET /ownership/{bow_id}
- GET /contracts/{bow_id}
- GET /history/{bow_id}
- POST /query-log
- GET /health

---

# 8. Data Models

- BowMetadata
- OwnershipRecord
- ContractRecord
- RegistrationRecord
- QueryLog
- MetadataResponse

---

# 9. Processing Flow

- Receive metadata request
- Validate request data
- Retrieve or store records
- Associate records with bow ID
- Format metadata response
- Return results


