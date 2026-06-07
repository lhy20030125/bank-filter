import pandas as pd
import pytest

from app.config import TRAIN_CSV
from app.data_loader import load_raw


@pytest.fixture
def sample_df():
    return load_raw(TRAIN_CSV).head(100)


def test_load_raw_returns_dataframe(sample_df):
    assert isinstance(sample_df, pd.DataFrame)
    assert len(sample_df) == 100
