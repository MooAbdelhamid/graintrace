# GrainTrace — Local Setup and Run Guide

This guide explains how to install the required dependencies and run GrainTrace locally on Windows.

## 1. Prerequisites

Install:

- Python 3.11
- Git
- Docker Desktop
- PostgreSQL with pgAdmin
- The required trained model files

Clone the repository:

```cmd
git clone https://github.com/MooAbdelhamid/graintrace.git
cd graintrace
```

> Some Python packages may require Administrator access. If you see `Access is denied` or `WinError 5`, close the terminal, reopen CMD or PowerShell using **Run as administrator**, and repeat the installation command.

---

## 2. Install dependencies

Install the common dependencies once:

```cmd
C:\Python311\python.exe -m pip install --upgrade pip setuptools wheel
C:\Python311\python.exe -m pip install fastapi uvicorn requests pydantic python-multipart numpy pillow opencv-python torch torchvision
```

Install the remaining service-specific dependencies:

```cmd
C:\Python311\python.exe -m pip install transparent-background ultralytics
C:\Python311\python.exe -m pip install qdrant-client
C:\Python311\python.exe -m pip install pydantic-settings psycopg2-binary
C:\Python311\python.exe -m pip install streamlit
```

If a `requirements.txt` file is available, you can install it with:

```cmd
C:\Python311\python.exe -m pip install -r requirements.txt
```

---

## 3. Add the model files

Create this folder:

```text
services\model\pipeline\model_weights\
```

From CMD:

```cmd
cd <PATH_TO_GRAINTRACE>\services\model
mkdir pipeline\model_weights
```

Copy the model files into it using these exact names:

```text
services\model\pipeline\model_weights\Dino_Final.pth
services\model\pipeline\model_weights\Resnet_Final.pth
```

---

## 4. Start Qdrant

Qdrant is a separate vector database used by the Retrieval service.

Start Docker Desktop first, then verify it is running:

```cmd
docker info
```

Create and start Qdrant:

```cmd
docker run --name graintrace-qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

For later runs, use:

```cmd
docker start graintrace-qdrant
```

---


## 5. Configure PostgreSQL

The Metadata service connects to PostgreSQL and reads the database credentials from a `.env` file.

Create this file:

```text
services\metadata\.env
```

Add your PostgreSQL / pgAdmin username and password:

```env
DB_HOST=localhost
DB_NAME=Metadata
DB_PORT=5432
DB_USER=YOUR_PGADMIN_USERNAME
DB_PASSWORD=YOUR_PGADMIN_PASSWORD
```

Replace `YOUR_PGADMIN_USERNAME` and `YOUR_PGADMIN_PASSWORD` with the username and password you use for your local PostgreSQL server in pgAdmin.

Make sure PostgreSQL is running before starting the Metadata service.

Do not upload or commit the `.env` file because it contains your database password.

---

## 6. Start the services

Open a separate terminal for each service.

### Preprocessing — port 8002

```cmd
cd <PATH_TO_GRAINTRACE>\services\preprocessing
C:\Python311\python.exe -m uvicorn main:app --port 8002
```

### Model — port 8003

```cmd
cd <PATH_TO_GRAINTRACE>\services\model
C:\Python311\python.exe -m uvicorn main:app --port 8003
```

### Retrieval — port 8004

```cmd
cd <PATH_TO_GRAINTRACE>\services\retrieval
C:\Python311\python.exe -m uvicorn main:app --port 8004
```

### Metadata — port 8005

```cmd
cd <PATH_TO_GRAINTRACE>\services\metadata
C:\Python311\python.exe -m uvicorn main:app --port 8005
```

### Orchestrator — port 8001

Start the orchestrator after the other services:

```cmd
cd <PATH_TO_GRAINTRACE>\services\orchestrator
C:\Python311\python.exe -m uvicorn main:app --port 8001
```

### Streamlit UI

```cmd
cd <PATH_TO_GRAINTRACE>\services\ui
C:\Python311\python.exe -m streamlit run GrainTrace.py
```

The Streamlit localhost page should open automatically in your browser.

---

## 7. Port summary

```text
Orchestrator    8001
Preprocessing   8002
Model           8003
Retrieval       8004
Metadata        8005
Qdrant          6333
Streamlit       8501
```

Keep these ports consistent with the service URLs used in the orchestrator.

---

## 8. Recommended startup order

```text
1. Docker Desktop
2. Qdrant
3. PostgreSQL
4. Preprocessing
5. Model
6. Retrieval
7. Metadata
8. Orchestrator
9. Streamlit UI
```

---

## 9. Common installation commands

If a dependency is missing, install it using:

```cmd
C:\Python311\python.exe -m pip install PACKAGE_NAME
```

Examples:

```cmd
C:\Python311\python.exe -m pip install python-multipart
C:\Python311\python.exe -m pip install opencv-python
C:\Python311\python.exe -m pip install pydantic-settings
C:\Python311\python.exe -m pip install psycopg2-binary
C:\Python311\python.exe -m pip install transparent-background
C:\Python311\python.exe -m pip install ultralytics
C:\Python311\python.exe -m pip install qdrant-client
```
