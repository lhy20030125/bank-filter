import pandas as pd

from app.config import TEST_CSV, TRAIN_CSV
from app.data_loader import (
    CATEGORICAL_COLS,
    DROP_COLS,
    NUMERIC_COLS,
    build_preprocessor,
    get_categorical_options,
    get_feature_names,
    get_numeric_ranges,
    load_raw,
    load_train_val,
    split_xy,
)


def test_load_raw_train():
    df = load_raw(TRAIN_CSV)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "subscribe" in df.columns


def test_load_raw_test():
    df = load_raw(TEST_CSV)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "subscribe" not in df.columns


def test_split_xy_with_target():
    df = load_raw(TRAIN_CSV)
    X, y = split_xy(df)
    assert "subscribe" not in X.columns
    assert all(c not in X.columns for c in DROP_COLS)
    assert y is not None
    assert set(y.unique()) <= {0, 1}


def test_split_xy_without_target():
    df = load_raw(TEST_CSV)
    X, y = split_xy(df)
    assert y is None
    assert len(X.columns) == len(NUMERIC_COLS) + len(CATEGORICAL_COLS)


def test_load_train_val():
    X_train, X_val, y_train, y_val = load_train_val(TRAIN_CSV)
    assert len(X_train) > len(X_val)
    assert len(X_train) + len(X_val) == len(load_raw(TRAIN_CSV))
    assert len(y_train) + len(y_val) == len(load_raw(TRAIN_CSV))


def test_build_preprocessor():
    preprocessor = build_preprocessor()
    assert preprocessor is not None
    # Check it has the right transformers
    names = [name for name, _, _ in preprocessor.transformers]
    assert "num" in names
    assert "cat" in names


def test_get_feature_names():
    names = get_feature_names()
    assert names == NUMERIC_COLS + CATEGORICAL_COLS
    assert len(names) == len(NUMERIC_COLS) + len(CATEGORICAL_COLS)


def test_get_categorical_options():
    opts = get_categorical_options(TRAIN_CSV)
    assert set(opts.keys()) == set(CATEGORICAL_COLS)
    for col, values in opts.items():
        assert len(values) > 0
        assert isinstance(values, list)


def test_get_numeric_ranges():
    ranges = get_numeric_ranges(TRAIN_CSV)
    assert set(ranges.keys()) == set(NUMERIC_COLS)
    for col, (lo, hi) in ranges.items():
        assert lo <= hi
