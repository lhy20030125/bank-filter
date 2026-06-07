import pytest
from sklearn.pipeline import Pipeline

from app.config import MODEL_PATH, TRAIN_CSV
from app.data_loader import load_train_val
from app.model import evaluate, model_exists, predict, train_model


@pytest.fixture(scope="module")
def trained_pipeline():
    """Train a small pipeline for testing."""
    X_train, X_val, y_train, y_val = load_train_val(TRAIN_CSV)
    return train_model(X_train, y_train)


@pytest.fixture(scope="module")
def val_data():
    """Load validation data."""
    _, X_val, _, y_val = load_train_val(TRAIN_CSV)
    return X_val, y_val


def test_train_model_returns_pipeline(trained_pipeline):
    assert isinstance(trained_pipeline, Pipeline)
    assert "preprocessor" in trained_pipeline.named_steps
    assert "classifier" in trained_pipeline.named_steps


def test_evaluate_auc_above_threshold(trained_pipeline, val_data):
    X_val, y_val = val_data
    metrics = evaluate(trained_pipeline, X_val, y_val)
    assert metrics["auc"] >= 0.75
    assert 0 <= metrics["accuracy"] <= 1
    assert 0 <= metrics["f1"] <= 1


def test_evaluate_has_report(trained_pipeline, val_data):
    X_val, y_val = val_data
    metrics = evaluate(trained_pipeline, X_val, y_val)
    assert "classification_report" in metrics
    assert "no" in metrics["classification_report"]
    assert "yes" in metrics["classification_report"]


def test_save_and_load_model(trained_pipeline, tmp_path):
    # Save to a temp location
    import joblib

    tmp_model = tmp_path / "test_model.joblib"
    joblib.dump(trained_pipeline, tmp_model)
    loaded = joblib.load(tmp_model)
    assert isinstance(loaded, Pipeline)


def test_model_exists():
    # After training, model should exist
    assert model_exists() is True or MODEL_PATH.exists()


def test_predict_returns_correct_keys(trained_pipeline, val_data):
    X_val, _ = val_data
    result = predict(trained_pipeline, X_val.iloc[[0]])
    assert "prediction" in result
    assert "probability_yes" in result
    assert "probability_no" in result
    assert "feature_importances" in result
    assert result["prediction"] in ("yes", "no")
    assert 0 <= result["probability_yes"] <= 1
    assert 0 <= result["probability_no"] <= 1
