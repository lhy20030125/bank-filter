import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from app.config import RANDOM_STATE, TARGET_COL

# Columns to drop (not predictive or leakage)
DROP_COLS = ["id", "duration"]

CATEGORICAL_COLS = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

NUMERIC_COLS = [
    "age",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]


def load_raw(csv_path) -> pd.DataFrame:
    """Load raw CSV and return DataFrame."""
    return pd.read_csv(csv_path)


def split_xy(df: pd.DataFrame):
    """Split features and target. Encode target: yes->1, no->0.

    If TARGET_COL is not in df (e.g. test.csv), returns (X, None).
    """
    df = df.drop(columns=[c for c in DROP_COLS if c in df.columns])
    if TARGET_COL in df.columns:
        y = df[TARGET_COL].map({"yes": 1, "no": 0})
        X = df.drop(columns=[TARGET_COL])
    else:
        y = None
        X = df
    return X, y


def load_train_val(csv_path, test_size=0.2):
    """Load training CSV and split into train/validation sets."""
    df = load_raw(csv_path)
    X, y = split_xy(df)
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
    )
    return X_train, X_val, y_train, y_val


def build_preprocessor() -> ColumnTransformer:
    """Build a ColumnTransformer for numeric + categorical features."""
    numeric_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)),
        ]
    )
    return ColumnTransformer(
        [
            ("num", numeric_pipeline, NUMERIC_COLS),
            ("cat", categorical_pipeline, CATEGORICAL_COLS),
        ]
    )


def get_feature_names():
    """Return ordered list of all feature names after preprocessing."""
    return NUMERIC_COLS + CATEGORICAL_COLS


def get_categorical_options(csv_path) -> dict:
    """Return unique values for each categorical column from raw data."""
    df = load_raw(csv_path)
    return {col: sorted(df[col].dropna().unique().tolist()) for col in CATEGORICAL_COLS}


def get_numeric_ranges(csv_path) -> dict:
    """Return (min, max) for each numeric column from raw data."""
    df = load_raw(csv_path)
    return {col: (float(df[col].min()), float(df[col].max())) for col in NUMERIC_COLS}
