import sys
from pathlib import Path

import pytest

# Ensure app is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import TEST_CSV, TRAIN_CSV


@pytest.fixture(scope="session")
def train_df():
    """Load training data once per session."""
    import pandas as pd

    return pd.read_csv(TRAIN_CSV)


@pytest.fixture(scope="session")
def test_df():
    """Load test data once per session."""
    import pandas as pd

    return pd.read_csv(TEST_CSV)
