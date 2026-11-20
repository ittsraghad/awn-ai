# عَون (AWN AI) — Work Log

This document records verified project activities, technical decisions, evaluation results, and remaining tasks.

---

## 2026-11-14 — Scope Detection V3 — Batch 5

### Objective
Create and audit the fifth IN_SCOPE topic batch: PRODUCTS_PROMOTIONS.

### Completed Work
- Created `batch_05` and `batch_05_df`.
- Added 40 messages.
- Assigned 8 messages to each writing style:
  - QUESTION: 8
  - PERSONAL: 8
  - REQUEST: 8
  - DESCRIPTIVE: 8
  - OTHER: 8
- Set scope to `IN_SCOPE`.
- Set pattern to `PRODUCTS_PROMOTIONS`.

### Verification
- Batch size: 40.
- Original unique messages: 40.
- Normalized unique messages: 40.
- Internal exact duplicates: 0.
- Internal normalized duplicates: 0.
- Overlap with V1: 0.
- Overlap with V2: 0.
- Overlap with previous V3 batches: 0.
- Manual review: APPROVED without message changes.

### Normalization Reconciliation
- Rebuilt the normalized message columns for Batches 1–4 using `normalize_message`.
- Rebuilt `v3_normalized` from the approved V3 source dataset.
- Verified 160 unique normalized messages before Batch 5 integration.
- All four previous batches passed normalization integrity checks.

### Final Result
- V3 shape: 200 × 4.
- Five approved batches integrated.
- 200 unique original messages.
- 200 unique normalized messages.

**Status: APPROVED AND INTEGRATED.**

---

## 2026-11-19 — Scope Detection V3 — Day 1

### Objective
Create and integrate Batches 6 and 7.

### Batch 6
- Pattern: `SCIENCE_NATURE`.
- Scope: `OUT_OF_SCOPE`.
- Messages: 40.
- One normalized overlap with V1 was identified and replaced.
- Final duplicate and overlap checks passed.
- Manually reviewed, approved, and integrated.

### Batch 7
- Pattern: `EDUCATION_LANGUAGE`.
- Scope: `OUT_OF_SCOPE`.
- Messages: 40.
- Exact and normalized duplicates: 0.
- Exact and normalized overlap with V1, V2, and existing V3: 0.
- Manually reviewed, approved, and integrated.

### Verification
- V3 shape: 280 × 4.
- IN_SCOPE: 200.
- OUT_OF_SCOPE: 80.
- Patterns: 7, with 40 messages each.
- Writing styles: 5, with 56 messages each.
- Unique original messages: 280.
- Unique normalized messages: 280.
- Integration assertions: PASS.

---

## 2026-11-20 — Scope Detection V3 — Day 2

### Objective
Create and integrate Batches 8 and 9.

### Completed Work
- Batch 8: `TECHNOLOGY_PROGRAMMING` — 40 messages.
- Batch 9: `TRAVEL_GEOGRAPHY` — 40 messages.
- Both batches were reviewed, approved, and integrated.

### Verification
- Exact duplicate checks passed.
- Normalized duplicate checks passed.
- Overlap checks against restored V3 passed.
- Final V3 shape: 360 × 4.
- IN_SCOPE: 200.
- OUT_OF_SCOPE: 160.
- Nine patterns with 40 messages each.
- Five writing styles with 72 messages each.
- Exact and normalized duplicates across V3: 0.

### Evaluation Note
V1 and V2 variables were unavailable after the notebook kernel restart. The overlap checks in this session were performed against restored V3 only. Frozen V1 and V2 datasets were not modified.

---

## 2026-11-20 — Scope Detection V3 — Day 3

### Objective
Create and integrate Batches 10 and 11.

### Completed Work
- Batch 10: `SPORTS_ENTERTAINMENT` — 40 messages.
- Batch 11: `MISSING_CONTEXT` — 40 messages.
- Both batches were reviewed, approved, and integrated.

### Verification
- Final V3 shape: 440 × 4.
- IN_SCOPE: 200.
- OUT_OF_SCOPE: 200.
- UNCLEAR_SCOPE: 40.
- Eleven patterns with 40 messages each.
- Five writing styles with 88 messages each.
- Exact duplicates: 0.
- Normalized duplicates: 0.

---

## 2026-11-20 — Scope Detection V3 — Day 4

### Objective
Create and integrate Batches 12 and 13.

### Completed Work
- Batch 12: `VAGUE_REQUESTS` — 40 messages.
- Batch 13: `PREVIOUS_CONVERSATION` — 40 messages.
- Both batches were manually reviewed, approved, and integrated.
- Each batch contained 8 messages per writing style.

### Verification
- Final V3 shape: 520 × 4.
- IN_SCOPE: 200.
- OUT_OF_SCOPE: 200.
- UNCLEAR_SCOPE: 120.
- Thirteen patterns with 40 messages each.
- Five writing styles with 104 messages each.
- Exact duplicates: 0.
- Normalized duplicates: 0.
- Integration assertions: PASS.

---

## 2026-11-20 — Scope Detection V3 — Day 5

### Objective
Complete the remaining dataset batches and final data quality audit.

### Completed Work
- Batch 14: `UNSPECIFIED_PROBLEMS` — 40 messages.
- Batch 15: `UNCLEAR_STATUS` — 40 messages.
- Both batches were reviewed, approved, and integrated.
- Completed the final dataset quality audit.

### Final Audit Results
- Total checks: 15.
- Passed: 15.
- Failed: 0.
- Dataset shape: 600 × 4.
- Scope distribution:
  - IN_SCOPE: 200.
  - OUT_OF_SCOPE: 200.
  - UNCLEAR_SCOPE: 200.
- Fifteen patterns with 40 messages each.
- Five writing styles with 120 messages each.
- Eight messages per writing style in every pattern.
- Missing values: 0.
- Empty messages: 0.
- Exact duplicates: 0.
- Normalized duplicates: 0.
- Leading/trailing whitespace issues: 0.

### Final Dataset
- Saved to `data/processed/scope_detection_v3.csv`.
- Reload verification passed.
- Saved data matched the original DataFrame.

**Limitation:** Full overlap comparison against frozen V1/V2 datasets was not available for all batches.

---

## 2026-11-20 — Scope Detection V3 — Day 6

### Objective
Train and evaluate the Scope Detection V3 models.

### Evaluation Strategy
- Dataset: 600 synthetic, manually authored messages.
- Evaluation: 5-fold StratifiedGroupKFold.
- Grouping: `pattern`.
- Each fold: 480 training messages and 120 test messages.
- The same fold splits were used for both models.

### Models Compared

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

### Selected Model Class Metrics

- IN_SCOPE F1: 0.823529.
- OUT_OF_SCOPE F1: 0.904872.
- UNCLEAR_SCOPE F1: 0.835443.

### Model Artifact
- Selected model: V2.
- Trained on all 600 V3 messages after evaluation.
- Saved to `models/scope_detection_v3.joblib`.
- File existence verified.
- Reload verification passed.
- Predictions before and after reload matched.

### Limitations
- The dataset is synthetic and manually authored.
- Cross-validation results are not production performance guarantees.
- Full-data training predictions are not independent evaluation results.
- IN_SCOPE recall remains 0.770.
- The evaluation estimates generalization to unseen topic patterns.

**Status: MODEL SELECTED, SAVED, AND RELOAD-VERIFIED.**

---

## 2026-11-20 — Day 7 — Final Integration and Interface

### Objective
Complete the final integration work, verify application behavior, improve the interface, and prepare the project for documentation and demonstration.

### 1. Application Interface Redesign

Updated:
- `src/static/index.html`
- `src/static/style.css`

Completed interface changes:
- Simplified the sidebar.
- Removed Quick Access.
- Removed Quick Prompts from the welcome interface.
- Moved the introductory content outside the chat container.
- Organized the introduction, capabilities, and process information into horizontal sections.
- Added a transparency information section below the introductory cards.
- Separated the chat workspace into its own section below the introductory content.
- Preserved the chat interface structure and its required element IDs.

### 2. Interface Behavior

The following behaviors were previously tested and confirmed working by the user:

- New Conversation.
- Enter to send.
- Shift + Enter for a new line.
- Character counter.
- Send button disabled while processing and re-enabled after the response.
- Typing indicator appears while waiting and disappears when the response arrives.

The typing indicator issue was resolved using a 300 ms delay before the chat API request.

**Important:** The typing indicator fix was verified by the user. Do not modify it without a specific regression.

### 3. End-to-End Behavior

The user confirmed that the previously tested application responses and interface behavior were working correctly.

Previously tested message categories included:
- IN_SCOPE.
- OUT_OF_SCOPE.
- UNCLEAR_SCOPE.

New Conversation and the main chat interactions were also tested during the integration work.

No additional repetition of successful tests is required unless a regression is reported.

### 4. API and Automated Test Evidence

Previously recorded API checks:

| Check | Result |
|---|---|
| Python compilation | Passed |
| `/` | HTTP 200 |
| `/static/style.css` | HTTP 200 |
| `/static/app.js` | HTTP 200 |
| `/health` | HTTP 200 |
| Existing automated test suite | 49 passed |

These are recorded as previously verified results. They should not be presented as a newly executed Day 7 test run.

### 5. Brand Decision

The project name was officially changed from Lumora to:

**عَون | AWN AI**

Approved tagline:

**ذكاء يفهم طلبك، ويوصلك للحل.**

The user approved the new identity.

The local project directory and existing technical artifact names have not been renamed as part of this documentation update.

### 6. Current Technical Boundaries

The project uses:
- Category classification.
- Intent classification.
- Scope detection.
- Hybrid knowledge retrieval.
- API-based message processing.
- A web-based chat interface.

The API does not currently use an external LLM SDK or API key for response generation.

There is no live store database integration, real-time order lookup, actual refund processing, or verified deployment URL.

### Day 7 Status

**User-confirmed:** Interface redesign and previously tested application behaviors are working.

**Remaining:** Final work-log review, branding consistency review, demo preparation, presentation preparation, and final readiness review.

---

## Important Technical Decisions and Restrictions

- V1 and V2 datasets remain frozen.
- Do not tune using previously exposed validation or test data.
- Do not describe previously inspected test results as independent.
- Scope Detection V3 is a synthetic, manually authored benchmark.
- Do not describe cross-validation results as production performance.
- Do not claim a complete V1/V2 overlap audit.
- Do not append unreviewed batches.
- Maintain balanced writing-style distribution.
- Preserve topic and scope label consistency.
- Do not modify working interface behavior without a documented reason.
- Do not claim LLM integration, live store integration, or deployment unless implemented and verified.

---

## How to Record Future Sessions

For every meaningful work session, record:

1. Date.
2. Objective.
3. Actions performed.
4. Actual outputs and verification results.
5. Decisions made.
6. Files or components changed.
7. Remaining work.
8. Exact next action.

Only record an action as completed after verifying its result.

---

## Current Project Checkpoint — 2026-11-20

### Completed
- Original category classification component.
- Intent classification component.
- Knowledge base.
- Hybrid retrieval evaluation.
- Scope Detection V3 dataset: 600 messages.
- Scope Detection V3 final quality audit: 15/15 passed.
- Scope Detection V3 model evaluation and selection.
- Selected model artifact saved and reload-verified.
- API and chat interface.
- Interface redesign.
- Main chat interactions tested and confirmed by the user.
- AWN AI brand identity approved.
- Project state documentation updated.

### Remaining Work
1. Review and finalize documentation.
2. Ensure consistent AWN AI branding in user-facing documents.
3. Prepare the final demo scenario.
4. Prepare the project presentation.
5. Complete the final project-readiness review.

**Next Action:** Continue with the documentation and demo-preparation phase. Do not repeat completed model development, dataset construction, or successful interface tests without a documented reason.