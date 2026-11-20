# AWN AI | عَون

### ذكاء يفهم طلبك، ويوصلك للحل.

AWN AI is an AI-powered customer support intelligence system designed to understand incoming customer messages, detect their scope, identify relevant categories and intents, and retrieve useful information from a structured knowledge base.

The project demonstrates an end-to-end machine learning workflow, combining data analysis, text classification, hybrid information retrieval, API development, and an interactive web interface.

---

## Project Overview

Customer support systems receive messages that may be relevant, unrelated, or unclear. AWN AI introduces an intelligent processing pipeline that evaluates incoming messages before attempting to retrieve relevant information.

### Key Features

- **Scope Detection:** Classifies messages into three categories:
  - `IN_SCOPE`
  - `OUT_OF_SCOPE`
  - `UNCLEAR_SCOPE`
- **Category & Intent Classification:** Identifies the relevant customer-service category and intent for supported messages.
- **Hybrid Information Retrieval:** Combines original-query similarity with intent-enriched similarity.
- **REST API:** Provides endpoints for health checks and customer message processing.
- **Interactive Web Interface:** Supports message submission, conversation controls, and response status indicators.
- **Source Transparency:** Returns retrieved knowledge excerpts with supporting source references.

---

## System Workflow

1. A customer submits a message through the web interface.
2. The API receives and processes the message.
3. The scope detection model determines whether the message is supported, unsupported, or unclear.
4. Supported messages proceed to category and intent classification.
5. The retrieval component searches the knowledge base using hybrid retrieval.
6. The API returns the relevant information and source references.
7. Unsupported or unclear messages receive predefined responses.

---

## Scope Detection V3

The latest scope detection model was developed using a manually authored synthetic dataset.

### Dataset Summary

| Property | Value |
|---|---:|
| Total messages | 600 |
| Scope classes | 3 |
| Messages per class | 200 |
| Writing styles | 5 |
| Message patterns | 15 |
| Dataset quality checks | 15/15 passed |

### Model Comparison

Two machine learning configurations were evaluated using five-fold `StratifiedGroupKFold`, grouped by message pattern.

| Model | Mean Fold Macro F1 |
|---|---:|
| V1: Word TF-IDF + Logistic Regression | 0.804 |
| V2: Word + Character TF-IDF + LinearSVC | **0.853** |

V2 outperformed V1 in all five validation folds and was selected as the final model.

### V2 Class Performance

| Class | F1 Score |
|---|---:|
| IN_SCOPE | 0.824 |
| OUT_OF_SCOPE | 0.905 |
| UNCLEAR_SCOPE | 0.835 |

**Evaluation Notes:**
- The reported Macro F1 is the mean of five validation-fold scores, not an out-of-fold aggregate.
- The final model was trained using all 600 dataset messages.
- LinearSVC decision margins are not probability estimates.
- The synthetic benchmark does not guarantee production performance.

---

## Information Retrieval Evaluation

The hybrid retrieval component was evaluated using 22 authored queries.

| Metric | Result |
|---|---:|
| Precision@1 | 81.82% |
| Recall@3 | 100% |
| Mean Reciprocal Rank (MRR) | 90.91% |

All 22 relevant documents appeared within the top three retrieved results.

---

## Technology Stack

| Area | Technologies |
|---|---|
| Programming Language | Python |
| Data Analysis | pandas, NumPy |
| Machine Learning | scikit-learn |
| Model Persistence | joblib |
| Backend API | FastAPI |
| ASGI Server | Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Testing | pytest |
| Development | JupyterLab |

---

## Project Structure

```text
AWN-AI/
├── data/
│   ├── raw/
│   ├── processed/
│   └── benchmark/
├── docs/
│   ├── PROJECT_STATE.md
│   ├── WORK_LOG.md
│   ├── knowledge_base.md
│   ├── annotation_guidelines.md
│   ├── benchmark_specification.md
│   └── benchmark_release_manifest.txt
├── models/
│   ├── scope_detection_v3.joblib
│   └── lumora_intent_model_v2.joblib
├── notebooks/
├── src/
│   ├── api.py
│   ├── intelligence.py
│   ├── knowledge_base.py
│   ├── pipeline.py
│   ├── predictor.py
│   ├── response_generator.py
│   ├── retriever.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
├── tests/
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.12
- pip
- Git

### 1. Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_REPOSITORY_DIRECTORY>
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 3. Activate the Environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the Application

From the project root directory:

```bash
uvicorn src.api:app --reload
```

Open your browser:

```text
http://127.0.0.1:8000
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the web interface |
| `/health` | GET | Checks API health |
| `/api/chat` | POST | Processes customer messages |

---

## Running Tests

Execute the test suite from the project root:

```bash
pytest -q
```

The previously completed test run reported **49 passing tests**.

---

## Knowledge Base

AWN AI currently uses a fictional demonstration store named **Lumora Demo Store**.

The knowledge base covers:

- Store information
- Orders
- Shipping and delivery
- Refunds and returns
- Payments
- Customer accounts
- Subscriptions
- Customer support policies

The store is used exclusively as a demonstration knowledge source.

---

## Current Limitations

- The knowledge base represents a fictional demonstration store.
- No live order-management or payment-system integration is available.
- The system cannot retrieve actual order status or execute refunds.
- The current API does not use an integrated LLM provider or configured LLM API key.
- Responses rely on retrieved knowledge and predefined scope responses.
- The current response content is in English.
- The scope detection dataset is synthetic and requires evaluation on representative real-world customer messages before production deployment.

---

## Documentation

Detailed technical documentation is available in the `docs/` directory, including:

- Project state and implementation progress.
- Development work log.
- Knowledge base documentation.
- Annotation guidelines.
- Scope Detection V3 benchmark specification.
- Benchmark release manifests.

---

## Project Status

The core classification, retrieval, API, and web interface components have been integrated.

The project is undergoing final documentation, demonstration preparation, and release preparation.

---

## Disclaimer

AWN AI is an educational and portfolio project developed to demonstrate applied machine learning, data processing, text classification, information retrieval, and API development. It is not a production-ready customer support platform.

---

**AWN AI — عَون**  
*ذكاء يفهم طلبك، ويوصلك للحل.*