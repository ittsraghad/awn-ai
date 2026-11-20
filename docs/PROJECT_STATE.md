# عَون (AWN AI) — Project State

**Last Updated:** 2026-11-20  
**Project:** عَون (AWN AI) — AI Customer Support Intelligence  
**Former Name:** Lumora  
**Purpose:** Build a high-quality, reproducible AI/ML portfolio project demonstrating machine learning, intent detection, scope classification, hybrid retrieval, and a functional customer support interface.

**Brand Tagline:** ذكاء يفهم طلبك، ويوصلك للحل.

---

## 1. Current Project Status

عَون (AWN AI) is an AI-powered customer support intelligence system.

The project includes:

- Customer message classification.
- Intent detection.
- Scope detection.
- Hybrid knowledge base retrieval.
- Decision-making before returning a response.
- Security checks.
- A web-based chat interface.
- Source references for retrieved information.

The project is designed to identify the nature and scope of a customer message before retrieving relevant knowledge.

**Important product limitation:** The current system uses classification and retrieval components. It is not connected to a live store database or an external LLM response-generation service.

The project is in its final integration, documentation, and demo-preparation stage.

---

## 2. Environment

- Operating System: macOS
- Python: 3.12.7
- Project Directory: `~/Desktop/Lumora`
- Virtual Environment: `.venv`
- Main Notebook: `notebooks/01_data_exploration.ipynb`

The local directory and existing technical paths retain their original names. The approved product identity is now AWN AI.

---

## 3. Original Dataset

**Source:**

`data/raw/customer_support_tickets.csv`

Known dimensions:

- 26,872 rows.
- 5 columns: `flags`, `instruction`, `category`, `intent`, `response`.
- 11 categories.
- 27 intents.
- No missing values in the initial inspection.

---

## 4. Completed ML Components

### 4.1 Category Classification

- Model: Character TF-IDF + LinearSVC.
- Artifact: `models/lumora_model_v2.joblib`
- Predictor: `src/predictor.py`
- Tests: 6 passed.
- Previously reported test accuracy: 99.9752%.

**Evaluation limitation:** The test set was previously inspected. It must not be described as pristine or independently untouched.

### 4.2 Intent Classification

- Model: Character TF-IDF + LinearSVC.
- Artifact: `models/lumora_intent_model_v2.joblib`
- Configuration: `data/processed/selected_intent_config_v2.json`
- Implementation: `src/intelligence.py`
- Tests: 6 passed.

**Evaluation limitation:** The test set was previously inspected, and four test queries overlap with synthetic training additions. Do not claim an untouched test evaluation.

### 4.3 Knowledge Base

- 22 documented chunks.
- Main file: `docs/knowledge_base.md`.
- Covers store information, orders, shipping, refunds, payments, accounts, subscriptions, customer support, and AI guidelines.
- Some intents have partial or unsupported knowledge coverage.

**Limitations:**

- No live order lookup.
- No actual payment or refund status integration.
- No real order management system.
- No account modification or actual order placement.
- No verified human-agent handoff.

### 4.4 Hybrid Retrieval

Evaluation dataset: 22 authored queries.

| Metric | Result |
|---|---:|
| Precision@1 | 81.82% |
| Recall@3 | 100% |
| MRR | 90.91% |

- 18 of 22 queries retrieved the correct document at rank 1.
- All 22 queries retrieved the correct document within the top 3.
- Four top-1 misses had the correct document at rank 2.
- No query missed its relevant document in the top 3.

The hybrid retrieval score uses:

- 75% original query similarity.
- 25% intent-enriched query similarity.

These results represent the authored retrieval benchmark, not production traffic.

---

## 5. Scope Detection V3 — Completed

### Dataset

File:

`data/processed/scope_detection_v3.csv`

Verified properties:

- 600 manually authored synthetic messages.
- 4 columns: `message`, `writing_style`, `scope`, `pattern`.
- 3 scope classes:
  - `IN_SCOPE`
  - `OUT_OF_SCOPE`
  - `UNCLEAR_SCOPE`
- 200 messages per class.
- 15 topic patterns.
- 40 messages per pattern.
- 5 writing styles.
- 120 messages per writing style.
- 8 messages per pattern per writing style.

### Data Quality Audit

Final audit:

- 15 checks passed.
- 0 checks failed.
- Missing values: 0.
- Empty messages: 0.
- Exact duplicates: 0.
- Normalized duplicates: 0.
- Leading/trailing whitespace issues: 0.
- Saved CSV reloaded and verified identical to the original DataFrame.

**Evaluation limitation:** Full overlap comparison against frozen V1/V2 datasets was not available for all batches. Do not claim a complete V1/V2 overlap audit.

### Model Evaluation

Evaluation strategy:

- StratifiedGroupKFold.
- 5 folds.
- Grouping by `pattern`.
- 480 training messages and 120 test messages per fold.

**Model V1**
- Word TF-IDF + Logistic Regression.
- Mean Macro F1: 0.803732.
- Standard deviation: 0.108728.

**Model V2 — Selected**
- Word + Character TF-IDF + LinearSVC.
- Mean Macro F1: 0.852994.
- Standard deviation: 0.074751.
- Minimum fold Macro F1: 0.754556.
- Maximum fold Macro F1: 0.923036.

V2 achieved a higher Macro F1 in all five folds.

Class-level F1:

| Class | F1 |
|---|---:|
| IN_SCOPE | 0.823529 |
| OUT_OF_SCOPE | 0.904872 |
| UNCLEAR_SCOPE | 0.835443 |

### Final Model Artifact

- Selected model: V2.
- Trained on all 600 V3 messages after evaluation.
- Artifact: `models/scope_detection_v3.joblib`
- File existence verified.
- Reload verification passed.
- Predictions before and after reload matched.

### Evaluation Limitations

- The dataset is synthetic and manually authored.
- Cross-validation results are not production performance guarantees.
- Full-data training predictions are not independent evaluation results.
- IN_SCOPE recall is 0.770 and remains an important limitation.
- The evaluation estimates generalization to unseen topic patterns.

---

## 6. API and Application

### API

Main file:

`src/api.py`

Known endpoints:

- `/` — serves the application interface.
- `/static` — serves static assets.
- `/health` — health check.
- `/api/chat` — chat request processing.

Previously verified API checks:

| Check | Result |
|---|---|
| Python compilation | Passed |
| `/` | 200 |
| `/static/style.css` | 200 |
| `/static/app.js` | 200 |
| `/health` | 200 |
| Existing automated tests | 49 passed |

### Response Behavior

- IN_SCOPE: retrieves relevant knowledge and returns the retrieved information with three sources.
- OUT_OF_SCOPE: returns an out-of-scope response.
- UNCLEAR_SCOPE: returns a clarification-oriented response.

The current API does not use an external LLM SDK or API key for response generation.

`src/pipeline.py` accepts an `llm_callable`, but this is not wired into the API.

The retrieved source excerpt is currently in English. No complete multilingual translation service is implemented.

---

## 7. User Interface — AWN AI

Main files:

- `src/static/index.html`
- `src/static/style.css`
- `src/static/app.js`

### Brand and Layout

The approved brand is:

**عَون | AWN AI**

The interface was redesigned to provide a cleaner and less crowded experience.

Current intended layout:

- Simplified sidebar.
- Brand identity and New Conversation button.
- Introduction section above the chat.
- Capabilities and process cards displayed horizontally.
- Transparency information below the cards.
- Independent chat workspace below the introduction section.
- Responsive layout for smaller screens.

Quick Access and Quick Prompts were removed from the redesigned welcome interface.

### Confirmed Interface Behavior

The user confirmed the following behaviors during interface development:

- New Conversation.
- Enter to send.
- Shift + Enter for a new line.
- Character counter.
- Send button disabled while a request is processing.
- Send button re-enabled after the response.
- Typing indicator appears while waiting and disappears when the response arrives.

The typing indicator fix uses a 300 ms delay before the chat API request. It was verified by the user and must not be modified unless a regression occurs.

### Testing Status

The user confirmed that the interface and its previously tested behaviors are working correctly after the redesign.

Do not repeat successful tests without a specific reason or reported regression.

---

## 8. Development History — Scope Detection V3

The following batches were completed and integrated:

| Batch | Pattern | Scope | Messages |
|---|---|---|---:|
| 1 | ORDERS_DELIVERY | IN_SCOPE | 40 |
| 2 | PAYMENTS_BILLING | IN_SCOPE | 40 |
| 3 | RETURNS_REFUNDS | IN_SCOPE | 40 |
| 4 | ACCOUNTS_CUSTOMER_SUPPORT | IN_SCOPE | 40 |
| 5 | PRODUCTS_PROMOTIONS | IN_SCOPE | 40 |
| 6 | SCIENCE_NATURE | OUT_OF_SCOPE | 40 |
| 7 | EDUCATION_LANGUAGE | OUT_OF_SCOPE | 40 |
| 8 | TECHNOLOGY_PROGRAMMING | OUT_OF_SCOPE | 40 |
| 9 | TRAVEL_GEOGRAPHY | OUT_OF_SCOPE | 40 |
| 10 | SPORTS_ENTERTAINMENT | OUT_OF_SCOPE | 40 |
| 11 | MISSING_CONTEXT | UNCLEAR_SCOPE | 40 |
| 12 | VAGUE_REQUESTS | UNCLEAR_SCOPE | 40 |
| 13 | PREVIOUS_CONVERSATION | UNCLEAR_SCOPE | 40 |
| 14 | UNSPECIFIED_PROBLEMS | UNCLEAR_SCOPE | 40 |
| 15 | UNCLEAR_STATUS | UNCLEAR_SCOPE | 40 |

All 15 batches were completed, reviewed, and integrated into the final V3 dataset.

---

## 9. Day 7 — Final Integration and Completion Work

Day 7 is the final session in the seven-session completion plan.

The remaining work is focused on final integration, documentation, and presentation readiness.

### Completed or User-Confirmed Work

- AWN AI brand identity approved.
- Chat interface redesigned.
- Introduction and information cards separated from the chat workspace.
- Quick Access removed.
- Typing indicator issue resolved and verified.
- Previously tested interface behaviors confirmed working by the user.
- The user confirmed that the project tests performed during the integration work are working correctly.

### Final Documentation Tasks

- Update `PROJECT_STATE.md`.
- Update `docs/WORK_LOG.md`.
- Ensure the project name and branding are consistent in user-facing documentation.
- Document the architecture and processing workflow.
- Record evaluation metrics and their limitations.
- Document known unsupported capabilities.
- Prepare a clear demo sequence.
- Prepare the project presentation and technical explanation.

Do not claim deployment, a live URL, or external service integration unless separately verified.

---

## 10. Known Limitations and Honest Claims

The following limitations must remain explicit in documentation and presentations:

1. Scope Detection V3 was evaluated on synthetic, manually authored data.
2. Cross-validation results are not production performance guarantees.
3. V1/V2 overlap auditing was not fully available for all V3 batches.
4. Category and intent evaluation datasets have known exposure limitations.
5. The knowledge base is static and does not connect to live store data.
6. The system cannot verify real-time order, payment, or refund status.
7. No external LLM response-generation service is currently wired into the API.
8. Retrieved source excerpts are currently English.
9. No deployment or live application URL has been verified.

Describe AWN AI accurately as an AI-powered customer support intelligence system combining classification, intent detection, scope detection, and hybrid knowledge retrieval.

---

## 11. Development Rules

- Work one step at a time.
- Provide complete code before explaining it.
- Do not repeat completed work.
- Do not invent variable names or assume files exist.
- Verify the current state before changing code.
- Preserve frozen datasets and experiments.
- Do not make unsupported performance claims.
- Record verified results, not assumptions.
- Do not modify working components without a documented reason.
- Maintain the work log whenever a meaningful milestone is completed.

---

## 12. Session Continuity Rule

At the beginning of each new session:

1. Read `PROJECT_STATE.md`.
2. Read `docs/WORK_LOG.md`.
3. Identify the last verified completed action.
4. Continue from the exact next pending action.
5. Avoid repeating completed workflows.

**Never restart a completed workflow without a documented reason.**

---

## 13. Current Next Actions

1. Complete the final project-state documentation.
2. Update `docs/WORK_LOG.md` with Day 7 progress and verified outcomes.
3. Review documentation for consistent AWN AI branding.
4. Prepare the end-to-end demo scenario.
5. Prepare the final presentation.
6. Perform a final project-readiness review.

**Project status:** Core ML components, Scope Detection V3 dataset and evaluation, API, and redesigned interface are in place. Final documentation and demo/presentation preparation remain.