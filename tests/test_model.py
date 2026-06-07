import pytest
from sklearn.pipeline import Pipeline

from app.config import TRAIN_CSV
from app.data_loader import load_train_val
from app.model import evaluate, load_model, model_exists, predict, save_model, train_model


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


def test_save_and_load_model(trained_pipeline):
    save_model(trained_pipeline)
    assert model_exists()
    loaded = load_model()
    assert isinstance(loaded, Pipeline)


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
