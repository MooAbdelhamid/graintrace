# 1. Purpose

Responsible for coordinating workflows between internal services and managing the end-to-end registration and retrieval pipelines.

---

# 2. Responsibilities

- Receive external client requests
- Coordinate service communication
- Manage registration workflows
- Manage retrieval workflows
- Route requests between services
- Aggregate service responses
- Generate shared bow IDs
- Handle workflow-level validation
- Format final system responses

---

# 3. Inputs

- User requests
- Bow images
- Embedding results
- Retrieval results
- Metadata information
- Workflow parameters

---

# 4. Outputs

- Final registration responses
- Final retrieval responses
- Workflow status information
- Generated bow IDs
- Aggregated system results

---

# 5. Internal Components

- API Layer
- Workflow Controller
- Registration Pipeline Manager
- Retrieval Pipeline Manager
- Service Clients
- Request Validator
- Response Aggregator
- ID Generator
- Error Handler
- Response Formatter

---

# 6. External Dependencies

- Preprocessing Service
- Model Service
- Retrieval Service
- Metadata Service
- Shared Schema Package

---

# 7. APIs/Interfaces

- POST /register
- POST /verify
- POST /batch-verify
- GET /health

---

# 8. Data Models

- RegistrationRequest
- VerificationRequest
- RegistrationResponse
- VerificationResult

---

# 9. Processing Flow

- Receive external request
- Validate request structure
- Route image to preprocessing service
- Send processed image to model service
- Send embedding to retrieval service
- Retrieve metadata information
- Aggregate service responses
- Apply workflow decision logic
- Format final response
- Return results