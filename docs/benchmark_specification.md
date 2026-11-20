# AWN AI — Benchmark Specification

**Document:** Benchmark Design and Evaluation Specification  
**Version:** 2.0  
**Project:** AWN AI — AI-Powered Customer Support Intelligence  
**Status:** Implemented and Evaluated  
**Purpose:** Document the Scope Detection V3 benchmark design, model evaluation methodology, results, and limitations.

---

## 1. Purpose

This document describes the benchmark methodology used to develop and evaluate the Scope Detection V3 component of AWN AI.

The benchmark assesses the ability of the system to distinguish between:

- **IN_SCOPE:** Requests that fall within the supported customer-support domain.
- **OUT_OF_SCOPE:** Requests outside the supported domain.
- **UNCLEAR_SCOPE:** Requests whose scope cannot be determined confidently from the available information.

The benchmark was designed to evaluate generalization across different linguistic patterns and writing styles while reducing the risk of template and pattern leakage between training and evaluation folds.

The benchmark is intended for controlled project evaluation. It does not represent a statistically representative sample of real-world customer-support traffic.

## 2. Benchmark Dataset

### 2.1 Dataset Overview

The Scope Detection V3 dataset contains 600 manually authored synthetic messages.

**Dataset file:**

`data/processed/scope_detection_v3.csv`

The dataset contains four columns:

| Field | Description |
|---|---|
| `message` | User message |
| `writing_style` | Writing style assigned to the message |
| `scope` | Expected scope classification |
| `pattern` | Linguistic pattern group |

### 2.2 Class Distribution

The dataset contains three balanced classes:

| Class | Examples | Percentage |
|---|---:|---:|
| IN_SCOPE | 200 | 33.33% |
| OUT_OF_SCOPE | 200 | 33.33% |
| UNCLEAR_SCOPE | 200 | 33.33% |
| **Total** | **600** | **100%** |

### 2.3 Pattern Distribution

The dataset contains 15 patterns, with 40 messages assigned to each pattern.

The patterns were designed to represent different types of requests and linguistic conditions relevant to scope detection.

### 2.4 Writing Style Distribution

The dataset contains five writing styles, with 120 messages per style.

Each writing style is represented across all 15 patterns, with eight messages per style-pattern combination.

This structure provides balanced representation across the defined writing styles and patterns.

## 3. Dataset Quality Assurance

The dataset underwent a quality assurance process covering 15 checks.

The checks included:

- Required column validation.
- Missing-value detection.
- Empty-message detection.
- Exact duplicate detection.
- Normalized duplicate detection.
- Whitespace and formatting checks.
- Class distribution verification.
- Pattern distribution verification.
- Writing-style distribution verification.
- Saved-file consistency verification.

**Final result: 15/15 quality checks passed.**

The saved CSV was reloaded and verified to match the validated dataset.

The dataset is synthetic and manually authored. Its quality checks establish structural and consistency properties; they do not establish representativeness of real customer-support traffic.

## 4. Model Evaluation Methodology

### 4.1 Evaluation Strategy

The Scope Detection V3 models were evaluated using:

**StratifiedGroupKFold with five folds.**

The evaluation used:

- Five folds.
- `pattern` as the grouping variable.
- Stratification to preserve class representation across folds.
- 480 training examples and 120 evaluation examples per fold.

Grouping by pattern was used to reduce the possibility of the same linguistic pattern appearing in both training and evaluation portions of a fold.

This approach evaluates generalization to held-out patterns rather than relying solely on randomly separated individual messages.

### 4.2 Model V1

V1 used:

- Word-level TF-IDF features.
- Logistic Regression classifier.

### 4.3 Model V2

V2 used:

- Word-level TF-IDF features.
- Character-level TF-IDF features.
- Linear Support Vector Classification (LinearSVC).

The word and character representations were combined to support the recognition of both semantic vocabulary and character-level linguistic variation.

### 4.4 Model Selection

Both models were evaluated using the same five-fold grouped evaluation strategy.

Mean fold Macro F1 was used as the primary model-selection metric.

V2 achieved a higher Macro F1 in all five folds and was selected as the final model.

## 5. Evaluation Results

### 5.1 Cross-Validation Results

| Metric | V1 | V2 |
|---|---:|---:|
| Mean Fold Macro F1 | 0.803732 | 0.852994 |
| Standard Deviation | 0.108728 | 0.074751 |
| Minimum Fold Macro F1 | — | 0.754556 |
| Maximum Fold Macro F1 | — | 0.923036 |

V2 outperformed V1 in all five evaluation folds.

Its higher mean Macro F1 and lower fold-to-fold standard deviation indicate stronger and more consistent performance under this evaluation setup.

The reported Macro F1 is the mean of the five fold-level Macro F1 scores. It must not be described as an out-of-fold Macro F1 score.

### 5.2 V2 Class-Level Results

| Class | F1-Score |
|---|---:|
| IN_SCOPE | 0.823529 |
| OUT_OF_SCOPE | 0.904872 |
| UNCLEAR_SCOPE | 0.835443 |

IN_SCOPE recall was 0.770.

These class-level results describe the reported V2 evaluation metrics and should not be interpreted as production performance guarantees.

### 5.3 Final Model Artifact

The selected model was trained on all 600 examples and saved as:

`models/scope_detection_v3.joblib`

The saved artifact was reloaded successfully, and predictions before and after reloading were verified to match.

Training on the complete dataset provides the final project model artifact. Predictions on that same training dataset are not an independent evaluation.

## 6. Scope Detection Behavior

The system uses the three scope labels to determine how a request should proceed through the customer-support pipeline.

| Scope | Expected System Behavior |
|---|---|
| IN_SCOPE | Continue to category and intent classification, followed by knowledge retrieval. |
| OUT_OF_SCOPE | Identify the request as outside the supported domain. |
| UNCLEAR_SCOPE | Indicate that the request requires clarification or additional context. |

Category and intent predictions are only produced for IN_SCOPE messages.

For OUT_OF_SCOPE and UNCLEAR_SCOPE messages, category and intent values are set to `None`.

### 6.1 Known Limitation

The message:

"I need help getting a refund"

was observed to receive an UNCLEAR_SCOPE prediction.

This is a known limitation identified during evaluation. It is documented rather than concealed or treated as evidence of perfect classification.

The model was not further tuned to eliminate this individual case.

## 7. Intent and Retrieval Evaluation

Intent classification and knowledge retrieval are separate components and must not be confused with the Scope Detection V3 benchmark.

### 7.1 Intent Classification

AWN AI includes a separate intent model artifact:

`models/lumora_intent_model_v2.joblib`

The intent model uses 11 categories.

Its evaluation must be reported separately from Scope Detection V3.

The existence of this component does not mean that Scope Detection V3 predicts the 27 intents described in the earlier benchmark specification.

### 7.2 Retrieval Evaluation

The retrieval component was evaluated using 22 manually authored queries.

| Metric | Result |
|---|---:|
| Precision@1 | 81.82% |
| Recall@3 | 100% |
| Mean Reciprocal Rank (MRR) | 90.91% |

Four queries did not retrieve the expected document at rank one. However, the correct document appeared at rank two for all four queries.

All 22 expected documents were retrieved within the top three results.

These results describe the evaluated query set and should not be generalized to all possible customer requests.

## 8. Data Separation and Leakage Considerations

The Scope Detection V3 evaluation uses grouped cross-validation to reduce pattern leakage between training and evaluation folds.

The following considerations apply:

1. Pattern groups are kept separate between the training and evaluation portions of each fold.
2. Class stratification is applied during fold generation.
3. Model comparison uses the same evaluation strategy.
4. The final selected model is trained on the complete V3 dataset.
5. Full-data training predictions are not reported as independent evaluation results.
6. The synthetic nature of the dataset must be considered when interpreting performance.

A complete overlap audit against every historical V1 and V2 example was not established for all dataset batches. Therefore, the documentation must not claim that a comprehensive historical overlap audit was completed.

## 9. Limitations

The benchmark has several limitations:

- The dataset contains 600 synthetic, manually authored messages.
- Its writing styles and patterns represent designed evaluation conditions rather than the full diversity of real customer language.
- Five-fold cross-validation provides an evaluation estimate under the defined grouping strategy, not a guarantee of future performance.
- The dataset does not establish production readiness.
- The observed performance cannot be generalized to real-world customer-support traffic without further external evaluation.
- Ambiguous messages may remain difficult to classify.
- The known refund-request limitation demonstrates that individual boundary cases require continued attention.

The benchmark should be expanded with independently collected and appropriately reviewed data when available.

## 10. Reproducibility and Documentation

The main benchmark artifacts are:

| Artifact | Location |
|---|---|
| Scope Detection V3 dataset | `data/processed/scope_detection_v3.csv` |
| Scope Detection V3 model | `models/scope_detection_v3.joblib` |
| Project state | `docs/PROJECT_STATE.md` |
| Work log | `docs/WORK_LOG.md` |
| Benchmark specification | `docs/benchmark_specification.md` |

Future evaluation reports should record:

- Dataset version.
- Model version.
- Feature extraction configuration.
- Cross-validation strategy.
- Evaluation date.
- Evaluation metrics.
- Known limitations.
- Any changes to labels, patterns, or preprocessing.

## 11. Final Status

**Scope Detection V3: Implemented and evaluated.**

The final dataset contains 600 messages across three balanced scope classes, 15 patterns, and five writing styles.

The dataset passed all 15 quality checks.

V2 was selected over V1 based on five-fold grouped cross-validation, achieving a mean fold Macro F1 of 0.852994.

The final model artifact was saved and successfully reloaded.

Intent classification and retrieval evaluation remain separate evaluation tracks and must not be represented as part of the Scope Detection V3 results.

The benchmark provides controlled project-level evidence. It does not establish production readiness or guarantee performance on real-world customer-support traffic.