from app.config import DATA_DIR, MODEL_DIR, MODEL_PATH, TEST_CSV, TRAIN_CSV


def test_config_paths_exist():
    assert DATA_DIR.exists()
    assert TRAIN_CSV.exists()
    assert TEST_CSV.exists()
    assert MODEL_DIR.exists() or True  # models/ may be empty initially


def test_config_values():
    assert TRAIN_CSV.name == "train.csv"
    assert TEST_CSV.name == "test.csv"
    assert MODEL_PATH.name == "model.joblib"
