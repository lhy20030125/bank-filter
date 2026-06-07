import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline

from app.config import MODEL_DIR, MODEL_PATH, RANDOM_STATE
from app.data_loader import build_preprocessor


def train_model(X_train, y_train) -> Pipeline:
    """Train a RandomForest pipeline with preprocessing."""
    preprocessor = build_preprocessor()
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        class_weight="balanced",
    )
    pipeline = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", clf),
        ]
    )
    pipeline.fit(X_train, y_train)
    return pipeline


def save_model(pipeline: Pipeline):
    """Save trained pipeline to disk."""
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)


def load_model() -> Pipeline:
    """Load trained pipeline from disk."""
    return joblib.load(MODEL_PATH)


def model_exists() -> bool:
    """Check if a saved model exists."""
    return MODEL_PATH.exists()


def predict(pipeline: Pipeline, X) -> dict:
    """Return prediction, probability, and feature importances."""
    proba = pipeline.predict_proba(X)[0]
    pred_class = int(np.argmax(proba))
    pred_label = "yes" if pred_class == 1 else "no"

    # Feature importances from the classifier
    clf = pipeline.named_steps["classifier"]
    importances = clf.feature_importances_

    return {
        "prediction": pred_label,
        "probability_yes": float(proba[1]),
        "probability_no": float(proba[0]),
        "feature_importances": importances,
    }


def evaluate(pipeline: Pipeline, X_test, y_test) -> dict:
    """Evaluate model on test set and return metrics."""
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    return {
        "auc": float(roc_auc_score(y_test, y_proba)),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "classification_report": classification_report(y_test, y_pred, target_names=["no", "yes"]),
    }
