import pandas as pd

from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


# 1. Load approved V3 dataset
data = pd.read_csv("data/processed/scope_detection_v3.csv")

X = data["message"]
y = data["scope"]
groups = data["pattern"]


# 2. Recreate original cross-validation
cv = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# 3. Recreate Model V2 exactly
word_char_features = FeatureUnion([
    (
        "word_tfidf",
        TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=10000
        )
    ),
    (
        "char_tfidf",
        TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            sublinear_tf=True,
            max_features=15000
        )
    )
])

model = Pipeline([
    ("features", word_char_features),
    (
        "classifier",
        LinearSVC(
            class_weight="balanced",
            random_state=42
        )
    )
])


# 4. Reconstruct out-of-fold predictions
oof_predictions = pd.Series(index=X.index, dtype="object")

for train_idx, test_idx in cv.split(X, y, groups=groups):
    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]

    model.fit(X_train, y_train)

    oof_predictions.iloc[test_idx] = model.predict(X_test)


# 5. Extract missed IN_SCOPE messages
errors = data.copy()
errors["predicted_scope"] = oof_predictions

false_negatives = errors[
    (errors["scope"] == "IN_SCOPE")
    & (errors["predicted_scope"] != "IN_SCOPE")
].copy()


# 6. Display summary
print("IN_SCOPE MISCLASSIFICATION ANALYSIS")
print("=" * 55)

print("Total IN_SCOPE messages:", (y == "IN_SCOPE").sum())
print("Missed IN_SCOPE messages:", len(false_negatives))

print("\nErrors by pattern:")
print(false_negatives["pattern"].value_counts())

print("\nErrors by writing style:")
print(false_negatives["writing_style"].value_counts())

print("\nErrors by predicted class:")
print(false_negatives["predicted_scope"].value_counts())


# 7. Display actual messages
print("\nMISCLASSIFIED MESSAGES")
print("=" * 55)

for _, row in false_negatives.iterrows():
    print(f"\nPattern: {row['pattern']}")
    print(f"Writing style: {row['writing_style']}")
    print(f"Actual: {row['scope']}")
    print(f"Predicted: {row['predicted_scope']}")
    print(f"Message: {row['message']}")
    print("-" * 55)

# 8. Save diagnostic results

false_negatives.to_csv(
    "data/processed/scope_v3_false_negatives.csv",
    index=False
)

print("\nDiagnostic report saved successfully.")

# 9. Save all misclassified messages

all_errors = errors[
    errors["scope"] != errors["predicted_scope"]
].copy()

all_errors.to_csv(
    "data/processed/scope_v3_all_errors.csv",
    index=False
)

print("\nALL CLASSIFICATION ERRORS")
print("=" * 55)

print("Total errors:", len(all_errors))

print("\nActual vs Predicted:")
print(
    pd.crosstab(
        all_errors["scope"],
        all_errors["predicted_scope"]
    )
)

print("\nErrors by actual class:")
print(all_errors["scope"].value_counts())

print("\nFull error report saved successfully.")

# 10. Inspect false positives

false_positives = errors[
    (errors["scope"] != "IN_SCOPE")
    & (errors["predicted_scope"] == "IN_SCOPE")
].copy()

print("\nFALSE POSITIVES — INCORRECT IN_SCOPE PREDICTIONS")
print("=" * 60)

for _, row in false_positives.iterrows():
    print(f"\nActual scope: {row['scope']}")
    print(f"Pattern: {row['pattern']}")
    print(f"Writing style: {row['writing_style']}")
    print(f"Message: {row['message']}")
    print("-" * 60)