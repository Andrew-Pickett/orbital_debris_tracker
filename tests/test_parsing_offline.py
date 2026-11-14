from pathlib import Path

import pytest
from pydantic import TypeAdapter

from app.database.models import DataModel


def test_example_data_parses():
    fixture = Path(__file__).parent / "fixtures" / "example_data.json"
    records = TypeAdapter(list[DataModel]).validate_json(fixture.read_text())

    assert records
    assert records[0].NORAD_CAT_ID
    assert records[0].MEAN_MOTION == pytest.approx(1.00283904, abs=1e-7)
    assert records[0].DECAY_DATE is None
