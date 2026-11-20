# AWN AI — Annotation Guidelines

**Document:** Scope, Category, and Intent Annotation Guidelines  
**Version:** 2.0  
**Project:** AWN AI — AI-Powered Customer Support Intelligence  
**Status:** Updated and Reviewed  
**Purpose:** Establish consistent annotation rules for scope detection, category classification, and intent classification.

---

## 1. Purpose

This document defines the annotation rules used by AWN AI to interpret and classify customer-support messages.

Its purpose is to establish consistent definitions for supported scope labels, customer-support categories, and associated intents.

The guidelines are designed to:

- Distinguish supported customer-support requests from unrelated requests.
- Identify messages that require additional context.
- Maintain consistent category and intent definitions.
- Reduce ambiguity between similar labels.
- Support reliable dataset preparation and model evaluation.
- Provide a reference for future annotation and quality assurance activities.

The document covers two related but separate classification stages:

1. Scope Detection: determining whether a message is within the supported domain, outside it, or unclear.
2. Category and Intent Classification: identifying the customer-support category and specific intent of an in-scope message.

These stages must not be treated as interchangeable classification tasks.

## 2. Annotation Architecture

AWN AI uses a staged classification approach.

### 2.1 Scope Detection

The first stage determines whether a user message belongs to the supported customer-support domain.

It uses three labels:

- IN_SCOPE
- OUT_OF_SCOPE
- UNCLEAR_SCOPE

### 2.2 Category and Intent Classification

Messages classified as IN_SCOPE can proceed to category and intent classification.

The supported taxonomy contains:

- 11 customer-support categories.
- 27 associated intents.

Each standard category-intent example is assigned one expected category and one expected intent.

### 2.3 Relationship Between the Two Stages

| Scope Label | Category Prediction | Intent Prediction |
|---|---|---|
| IN_SCOPE | Applicable | Applicable |
| OUT_OF_SCOPE | Not applicable | Not applicable |
| UNCLEAR_SCOPE | Not applicable | Not applicable |

Category and intent predictions must not be assigned to messages that have not been identified as IN_SCOPE.

Scope Detection V3 and category-intent classification are separate evaluation tasks. Results from one task must not be presented as results from the other.

---

## 3. Scope Labels and Definitions

### 3.1 IN_SCOPE

A message is IN_SCOPE when its primary purpose falls within the customer-support services represented by AWN AI's supported taxonomy.

Examples include requests about:

- Customer accounts.
- Order creation, modification, cancellation, and tracking.
- Delivery options and delivery periods.
- Shipping addresses.
- Payment methods and payment problems.
- Invoices.
- Refund policies and refund requests.
- Customer-service contact.
- Complaints and reviews.
- Newsletter subscriptions.

**Annotation rule:**

Classify a message as IN_SCOPE when the available information establishes a meaningful connection to a supported customer-support request.

Do not require the message to use exact category or intent terminology.

### 3.2 OUT_OF_SCOPE

A message is OUT_OF_SCOPE when its primary purpose is unrelated to the supported customer-support domain.

Examples may include:

- General knowledge questions unrelated to the supported service.
- Requests for unrelated educational explanations.
- Programming questions unrelated to customer support.
- Requests about unrelated personal interests.
- Other requests that cannot reasonably be handled using the supported customer-support taxonomy.

**Annotation rule:**

Do not assign an arbitrary customer-support category to an unrelated request.

A message should be OUT_OF_SCOPE because its purpose is outside the supported domain, not simply because it is difficult to understand.

### 3.3 UNCLEAR_SCOPE

A message is UNCLEAR_SCOPE when the available information is insufficient to determine whether the request belongs to the supported customer-support domain.

Examples may include:

- Very short messages without sufficient context.
- Vague requests that do not identify the subject.
- Messages that could reasonably refer to either a supported or unsupported activity.
- Requests requiring clarification before their purpose can be established.

**Annotation rule:**

Do not assume that an unclear message is automatically IN_SCOPE or OUT_OF_SCOPE.

The absence of sufficient context should be preserved as uncertainty rather than replaced with an unsupported assumption.

### 3.4 Scope Annotation Principles

The following principles apply to all three scope labels:

1. Annotate the primary purpose of the complete message.
2. Consider the meaning of the message rather than isolated keywords.
3. Do not assume that mentioning a product, order, payment, or account automatically makes a request IN_SCOPE.
4. Do not classify a message as OUT_OF_SCOPE merely because its wording is unusual.
5. Use UNCLEAR_SCOPE when the available information does not support a reliable scope decision.
6. Spelling mistakes and informal language do not independently determine scope.
7. Apply the same scope definitions across all writing styles.
8. Do not use model predictions as proof that an annotation is correct.

---

## 4. Category and Intent Definitions

The following taxonomy defines the supported customer-support categories and their associated intents.

These definitions apply to category and intent annotation after a message has been established as IN_SCOPE.

### 4.1 ACCOUNT

Customer requests related to creating, accessing, and managing personal or user accounts.

| Intent | Definition |
|---|---|
| create_account | Creating or opening a new customer account. |
| delete_account | Closing or deleting an existing account. |
| edit_account | Modifying, updating, or correcting existing account or profile information. |
| recover_password | Recovering or resetting forgotten or inaccessible account credentials, including passwords, PINs, or account access keys. Also includes asking for information about the recovery or reset process. |
| registration_problems | Experiencing difficulties or errors during account registration or sign-up, or asking for help reporting registration problems. |
| switch_account | Switching between existing accounts or changing the currently active account or account type. |

**Boundary rules:**

- Creating or opening a new account belongs to `create_account`.
- Reporting a problem or difficulty during registration belongs to `registration_problems`.
- Deleting or closing an existing account belongs to `delete_account`.
- Modifying existing profile information belongs to `edit_account`.
- Switching between existing accounts or changing the active account belongs to `switch_account`.
- Recovering or resetting a password, PIN, or access key belongs to `recover_password`.
- A request to change account information should not automatically be classified as switching accounts.
- Generic statements about using an account do not necessarily indicate an intention to switch accounts. Additional context may be required.

### 4.2 CANCEL

Requests concerning cancellation fees or penalties.

| Intent | Definition |
|---|---|
| check_cancellation_fee | Asking about cancellation charges, early termination fees, withdrawal fees, or penalties, including how to find information about these charges. |

**Boundary rules:**

- Asking about cancellation or early termination fees belongs to `check_cancellation_fee`.
- Asking to cancel an existing purchase or order belongs to ORDER, specifically `cancel_order`.
- A fee inquiry is not the same as a request to cancel a purchase.
- Cancellation fees may relate to services or agreements and are not necessarily limited to purchases.

### 4.3 CONTACT

Requests to communicate with customer support.

| Intent | Definition |
|---|---|
| contact_customer_service | Asking how to contact customer service, requesting available support channels, or asking about customer service availability and operating hours. |
| contact_human_agent | Explicitly requesting communication with a human customer service representative, operator, or support agent. |

**Boundary rules:**

- Asking how to contact customer service or asking about support hours belongs to `contact_customer_service`.
- Explicitly requesting to speak with a real person, human representative, or operator belongs to `contact_human_agent`.
- A request for general support information should not automatically be classified as a request for a human agent.

### 4.4 DELIVERY

Requests concerning delivery methods, delivery availability, and estimated delivery times.

| Intent | Definition |
|---|---|
| delivery_options | Requesting information about available delivery or shipping methods and options, including whether delivery or ordering is available for a specified location. |
| delivery_period | Requesting information about the expected delivery timeframe, estimated arrival date, or how long an order, shipment, or parcel takes to arrive. |

**Boundary rules:**

- Asking which delivery or shipping methods are available belongs to `delivery_options`.
- Asking whether delivery or ordering is available for a particular city or country may belong to `delivery_options`.
- Asking how long delivery takes or when a shipment is expected to arrive belongs to `delivery_period`.
- Asking about the status, progress, or location of a specific existing order belongs to ORDER, specifically `track_order`.
- Asking about available delivery methods is different from asking about the expected delivery duration.
- A question about placing an order from a particular location may be ambiguous between delivery availability and the purchasing process. Use the primary purpose of the request and available context.

### 4.5 FEEDBACK

Customer complaints, reviews, opinions, and feedback submissions.

| Intent | Definition |
|---|---|
| complaint | Expressing the intention to file, submit, or lodge a formal complaint or customer claim against a company, organization, product, or service. Also includes asking for guidance on how to submit such a complaint or claim. |
| review | Expressing the intention to write, submit, or share a review, comment, opinion, or general feedback about a product, service, company, or customer experience. |

**Boundary rules:**

- Asking to file or lodge a complaint or customer claim belongs to `complaint`.
- Asking to leave a review, write a comment, or share an opinion belongs to `review`.
- A negative opinion does not automatically represent a formal complaint.
- The word "feedback" alone does not determine the intent; classification must consider the customer's primary purpose.
- A message clearly requesting both a formal complaint and a separate review should be recorded as multi-intent for separate evaluation.

### 4.6 INVOICE

Requests concerning viewing, checking, locating, or obtaining invoices and bills.

| Intent | Definition |
|---|---|
| check_invoice | Requesting help locating, accessing, viewing, or checking an existing invoice or bill, including invoices associated with a previous purchase or a specified person. |
| get_invoice | Requesting to obtain, download, receive, or have an existing invoice or bill sent, including invoices associated with a specified person, purchase, or time period. |

**Boundary rules:**

- Asking where to find, view, or check an existing invoice belongs to `check_invoice`.
- Asking to obtain, download, receive, or have a copy of an invoice sent belongs to `get_invoice`.
- The words "invoice" and "bill" may refer to the same document in this classification context.
- A generic request to get an invoice without specifying how should be interpreted using the surrounding context.
- Questions about payment methods or transaction problems belong to PAYMENT, not INVOICE.

### 4.7 ORDER

Requests related to creating, modifying, cancelling, or tracking purchases.

| Intent | Definition |
|---|---|
| cancel_order | Requesting cancellation of an existing order or purchase, either directly or by asking for help or instructions to cancel it. |
| change_order | Requesting modifications to an existing order, including adding products, removing products, or changing its contents. |
| place_order | Asking to create or place a new order, expressing an intention to purchase products, or requesting assistance with the purchasing process. |
| track_order | Checking the current status of an existing order, tracking its progress or location, or asking about its estimated time of arrival (ETA). |

**Boundary rules:**

- Cancelling an entire existing order belongs to `cancel_order`.
- Adding or removing individual products from an existing order belongs to `change_order`, not `cancel_order`.
- Modifying the contents of an existing order belongs to `change_order`.
- Creating a new purchase belongs to `place_order`.
- Asking for assistance or instructions to complete a new purchase belongs to `place_order`.
- Checking the status, progress, location, or ETA of a specific existing order belongs to `track_order`.
- Mentioning a reason for cancellation, such as being unable to afford the purchase or no longer wanting the product, does not change the primary intent when the requested action is order cancellation.
- A payment failure during a purchase should not automatically be classified as an ORDER request. If the primary issue concerns the transaction or payment itself, PAYMENT may be more appropriate.

### 4.8 PAYMENT

Requests concerning payment methods and payment problems.

| Intent | Definition |
|---|---|
| check_payment_methods | Requesting information about the payment methods or payment options accepted, supported, or available, including how to view or check them. |
| payment_issue | Requesting help reporting, addressing, or resolving payment problems, including failed or unsuccessful online payment transactions. |

**Boundary rules:**

- Asking which payment methods or options are accepted belongs to `check_payment_methods`.
- Reporting a failed or unsuccessful payment transaction belongs to `payment_issue`.
- Asking for help with a payment problem belongs to `payment_issue`.
- Asking about available payment options is different from reporting a problem with an attempted payment.
- A payment problem should not automatically be classified as ACCOUNT or ORDER simply because the message mentions an account or purchase.
- A request to obtain money back after a purchase belongs to REFUND when the primary purpose is reimbursement rather than resolving the original payment transaction.

### 4.9 REFUND

Requests concerning refund policies, refund requests, and refund status.

| Intent | Definition |
|---|---|
| check_refund_policy | Requesting information about refund policies, eligibility conditions, and circumstances under which a refund or reimbursement can be requested, including whether specific service charges are refundable. |
| get_refund | Requesting a refund, reimbursement, rebate, or compensation for money paid, including asking how to submit or obtain a refund. |
| track_refund | Requesting updates or information about the status and progress of an existing refund, reimbursement, rebate, or compensation request, including checking for delays or problems. |

**Boundary rules:**

- Asking whether a purchase or service charge is refundable belongs to `check_refund_policy`.
- Requesting money back for a purchase belongs to `get_refund`.
- Asking for an update on an already requested refund belongs to `track_refund`.
- Asking about refund eligibility is different from requesting an actual refund.
- Asking about the status of an existing refund is different from submitting a new refund request.
- Terms such as "reimbursement", "rebate", and "money back" may indicate a refund-related request.
- The term "compensation" may have different meanings in real-world contexts. Annotators should consider whether the message clearly refers to money paid back or to another form of compensation.

### 4.10 SHIPPING

Requests concerning adding, submitting, modifying, or correcting shipping addresses.

| Intent | Definition |
|---|---|
| change_shipping_address | Requesting help modifying, updating, or correcting an existing shipping or delivery address, including resolving problems encountered while changing the address. |
| set_up_shipping_address | Requesting help adding, entering, submitting, or setting up a new or additional shipping or delivery address, including resolving problems encountered during the process. |

**Boundary rules:**

- Modifying, updating, or correcting an existing address belongs to `change_shipping_address`.
- Adding or registering a new or additional address belongs to `set_up_shipping_address`.
- Asking how to enter or submit a new delivery address belongs to `set_up_shipping_address`.
- Reporting an error while entering or submitting a new address also belongs to `set_up_shipping_address`.
- A request to replace or correct an existing address should not automatically be classified as setting up a new address.
- Words such as "different", "another", or "new" should be interpreted in context. They do not independently determine the intent.

### 4.11 SUBSCRIPTION

Requests concerning newsletter subscriptions.

| Intent | Definition |
|---|---|
| newsletter_subscription | Requesting to subscribe to or unsubscribe from a newsletter, or reporting difficulties managing newsletter subscription preferences. |

**Boundary rules:**

- Asking to subscribe to a newsletter belongs to `newsletter_subscription`.
- Asking to unsubscribe from a newsletter belongs to `newsletter_subscription`.
- Asking to stop receiving promotional or newsletter emails may belong to this intent when the primary purpose is managing newsletter preferences.
- A request concerning a paid service subscription should not automatically be treated as a newsletter request. Additional context may be required because the taxonomy defines this intent around newsletters.

---

## 5. Important Classification Boundaries

The following distinctions are particularly important when annotating similar customer requests.

| Distinction | Classification Rule |
|---|---|
| CANCEL vs. ORDER | Cancellation fees belong to CANCEL; cancelling a purchase belongs to ORDER. |
| DELIVERY vs. SHIPPING | Delivery options, availability, and estimated arrival times belong to DELIVERY; adding or changing an address belongs to SHIPPING. |
| PAYMENT vs. REFUND | Payment transaction problems belong to PAYMENT; requesting money back or checking refund status belongs to REFUND. |
| INVOICE vs. PAYMENT | Finding or obtaining an invoice belongs to INVOICE; payment methods and transaction problems belong to PAYMENT. |
| get_refund vs. track_refund | Requesting a new refund belongs to get_refund; checking an existing refund belongs to track_refund. |
| check_refund_policy vs. get_refund | Asking about refund eligibility belongs to check_refund_policy; requesting reimbursement belongs to get_refund. |
| check_invoice vs. get_invoice | Checking or locating an invoice belongs to check_invoice; obtaining, downloading, or receiving a copy belongs to get_invoice. |
| change_shipping_address vs. set_up_shipping_address | Editing an existing address belongs to change_shipping_address; adding or submitting a new address belongs to set_up_shipping_address. |
| contact_customer_service vs. contact_human_agent | Asking about support channels or operating hours belongs to contact_customer_service; explicitly requesting a human representative belongs to contact_human_agent. |
| complaint vs. review | Filing a formal complaint or customer claim belongs to complaint; sharing a review, comment, or opinion belongs to review. |
| create_account vs. registration_problems | Creating a new account belongs to create_account; experiencing or reporting difficulties during registration belongs to registration_problems. |
| edit_account vs. switch_account | Changing existing account details belongs to edit_account; switching between accounts or changing the active account belongs to switch_account. |
| recover_password vs. registration_problems | Recovering or resetting account credentials belongs to recover_password; problems occurring during account registration belong to registration_problems. |
| place_order vs. change_order | Creating a new purchase belongs to place_order; modifying an existing purchase belongs to change_order. |
| change_order vs. cancel_order | Adding or removing products from an existing order belongs to change_order; cancelling the entire order belongs to cancel_order. |
| track_order vs. delivery_period | Checking the status or ETA of a specific order belongs to track_order; asking about general delivery duration belongs to delivery_period. |
| track_order vs. delivery_options | Tracking a specific existing order belongs to track_order; asking about available delivery methods belongs to delivery_options. |
| check_payment_methods vs. payment_issue | Asking about accepted payment options belongs to check_payment_methods; reporting a failed or problematic transaction belongs to payment_issue. |
| CONTACT vs. other categories | A request for contact information belongs to CONTACT unless another specific support request is the primary purpose of the message. |

---

## 6. Ambiguous and Multi-Intent Messages

### 6.1 Ambiguous Messages

A message is ambiguous when its intended meaning cannot be determined confidently from the available information.

Examples:

**Example 1:**

"Where is my package?"

The message may refer to order tracking or delivery information.

**Example 2:**

"My package has not arrived yet."

The message indicates a delivery-related concern, but does not clearly establish whether the customer wants to track the order, ask about a delay, or report a delivery problem.

**Example 3:**

"I want to stop receiving your emails."

The message may refer to newsletter preferences or another type of email communication.

**Annotation rule:**

Do not invent missing context. Mark the example as ambiguous for separate evaluation and identify what clarification is needed.

For Scope Detection, ambiguity about the specific category or intent does not automatically mean UNCLEAR_SCOPE. Use UNCLEAR_SCOPE only when the available information is insufficient to determine whether the request belongs to the supported customer-support domain.

### 6.2 Multi-Intent Messages

A message is multi-intent when it contains two or more distinct customer requests.

Example:

"I want to cancel my order and check the cancellation fee."

Possible intents:

- `cancel_order` — ORDER
- `check_cancellation_fee` — CANCEL

**Annotation rule:**

Do not force a multi-intent example into a single-label category-intent annotation when multiple distinct requests are genuinely present.

For a separate multi-intent evaluation, record each expected category and intent.

The Scope Detection V3 dataset uses one scope label per message. A message containing multiple supported customer-support requests may still be IN_SCOPE.

Multi-intent identification is a separate capability and must not be claimed as fully implemented or evaluated by Scope Detection V3.

---

## 7. Out-of-Scope Messages

An out-of-scope message does not belong to any of the 11 supported customer-support categories.

Examples may include unrelated questions or requests outside the customer-support services represented by the taxonomy.

**Annotation rules:**

- Assign OUT_OF_SCOPE when the primary purpose is outside the supported customer-support domain.
- Do not assign an arbitrary category simply because the category classifier supports only 11 categories.
- Do not confuse an unrelated request with a request that is merely unclear.
- Do not classify a request as OUT_OF_SCOPE only because its wording is unfamiliar.
- Scope Detection must be evaluated separately from category and intent classification.

The Scope Detection V3 dataset contains independently authored OUT_OF_SCOPE examples. It is separate from the earlier proposed Challenge Set described in the previous benchmark specification.

---

## 8. Annotation Quality Rules

Annotators should follow these principles:

1. Classify according to the customer's intended request, not isolated keywords.
2. Consider the complete message and its context.
3. Do not treat spelling mistakes, informal language, or grammatical errors as different intents.
4. Distinguish between requesting an action, asking for information, and tracking an existing process.
5. Do not invent information that is not present in the message.
6. Mark genuinely ambiguous and multi-intent messages separately when the evaluation task requires it.
7. Keep annotation decisions consistent across the dataset.
8. Apply the same classification boundaries to formal, informal, and misspelled messages.
9. Distinguish between modifying part of an existing order and cancelling the entire order.
10. Do not assume that every example's original dataset label is correct.
11. Record suspected label inconsistencies for review instead of silently changing original labels.
12. Preserve the original dataset and document any proposed corrections separately.
13. Distinguish between adding a new shipping address and modifying an existing one.
14. Distinguish between a payment transaction problem and a request for reimbursement.
15. Use the primary purpose of the message when several related terms appear together.
16. Do not treat model confidence as proof that an annotation is correct.
17. Apply the three scope definitions consistently.
18. Do not assign category or intent labels to OUT_OF_SCOPE or UNCLEAR_SCOPE messages.
19. Preserve genuine uncertainty instead of inventing a definite label.
20. Do not change an expected label merely to match a model prediction.

---

## 9. Scope Detection V3 Dataset Guidelines

### 9.1 Dataset Overview

Scope Detection V3 is a manually authored synthetic dataset created for the scope detection task.

Dataset location:

`data/processed/scope_detection_v3.csv`

The dataset contains 600 messages and four columns:

| Field | Description |
|---|---|
| `message` | User message being classified. |
| `writing_style` | Assigned writing style. |
| `scope` | Expected scope label. |
| `pattern` | Linguistic pattern group. |

### 9.2 Dataset Distribution

The dataset contains three balanced scope classes:

| Scope | Examples |
|---|---:|
| IN_SCOPE | 200 |
| OUT_OF_SCOPE | 200 |
| UNCLEAR_SCOPE | 200 |
| **Total** | **600** |

It also contains:

- 15 patterns, with 40 messages per pattern.
- Five writing styles, with 120 messages per style.
- Eight messages per writing-style and pattern combination.

### 9.3 Dataset Construction Principles

The dataset was designed to provide balanced representation across its scope labels, writing styles, and patterns.

Messages were manually authored to represent different linguistic conditions rather than relying exclusively on repeated templates.

The dataset construction process included checks for:

- Missing values.
- Empty messages.
- Exact duplicates.
- Normalized duplicates.
- Whitespace and formatting issues.
- Expected class distribution.
- Expected pattern distribution.
- Expected writing-style distribution.
- Consistency between the validated dataset and the saved CSV.

The final dataset passed all 15 documented quality checks.

### 9.4 Scope Annotation Rules for V3

Every V3 message must have exactly one expected scope label.

The following rules apply:

- IN_SCOPE messages must represent requests within the supported customer-support domain.
- OUT_OF_SCOPE messages must represent requests outside that domain.
- UNCLEAR_SCOPE messages must lack sufficient information for a confident scope decision.
- The assigned label must reflect the message meaning rather than the model's prediction.
- The same annotation principles must apply across all writing styles and patterns.

The three labels must remain distinct throughout dataset preparation, training, and evaluation.

---

## 10. Limitations

These guidelines are based on the original synthetic customer-support dataset, its category-intent taxonomy, and the independently authored Scope Detection V3 dataset.

The category and intent definitions were refined through inspection of representative examples from all 27 intents.

The review identified several observations and potential data-quality concerns.

In particular:

- Some examples labeled `create_account` appeared closer to `registration_problems`.
- Some examples labeled `switch_account` did not clearly express an intention to switch accounts.
- Some examples labeled `change_order` contained vague wording that did not specify the intended modification.
- Some `place_order` examples contained unusual word choices that may represent language or data-quality issues.
- Some delivery-related examples could be interpreted as either delivery availability or assistance with placing an order.
- Some refund examples used terms such as "compensation" that may require additional context.
- Some newsletter-related wording could be confused with other types of subscriptions or email preferences.

These observations indicate possible label noise or semantic ambiguity. They do not establish that the original labels are incorrect across the dataset.

The reviewed examples are representative samples, not an exhaustive inspection of every record.

The Scope Detection V3 dataset is synthetic and manually authored. Passing its quality checks establishes structural and consistency properties but does not prove that its messages represent all real-world customer-support language.

The benchmark results must therefore be interpreted within the limits of the dataset and evaluation methodology.

In particular:

- The dataset does not establish production readiness.
- The defined writing styles and patterns do not represent every possible language variation.
- Ambiguous messages may remain difficult to classify.
- Strong results on synthetic data must not be generalized to real-world customer-support traffic without further evidence.
- The current taxonomy does not cover every possible customer-support request.
- The guidelines do not establish that multi-intent detection is fully implemented.
- The guidelines do not establish that every category and intent boundary has been exhaustively validated.

---

## 11. Future Extensions

The following activities remain potential improvements and have not been claimed as completed:

- More extensive positive and negative boundary examples for all 27 intents.
- A systematic label-noise audit and formal adjudication process.
- Inter-annotator agreement evaluation involving independent annotators.
- Expansion of the scope detection dataset with additional independently authored examples.
- Further validation using real-world customer-support messages.
- Separate multi-intent detection and evaluation.
- More extensive testing of ambiguous requests and clarification behavior.
- Documentation of any approved corrections to original dataset labels.
- Additional independent evaluation data to assess generalization.

Any future changes to annotation definitions should be documented and version-controlled.

---

## 12. Versioning and Documentation

This document is version 2.0 and replaces the previous annotation guidelines version 1.3.

It brings the existing category-intent taxonomy together with the scope annotation rules used in Scope Detection V3.

The following project artifacts are relevant:

| Artifact | Location |
|---|---|
| Annotation Guidelines | `docs/annotation_guidelines.md` |
| Benchmark Specification | `docs/benchmark_specification.md` |
| Scope Detection V3 Dataset | `data/processed/scope_detection_v3.csv` |
| Scope Detection V3 Model | `models/scope_detection_v3.joblib` |
| Project State | `docs/PROJECT_STATE.md` |
| Work Log | `docs/WORK_LOG.md` |

Future annotation and evaluation reports should record:

- Guideline version.
- Dataset version.
- Model version, where applicable.
- Annotation date.
- Evaluation methodology.
- Known limitations.
- Any approved annotation changes.

---

**End of Document**