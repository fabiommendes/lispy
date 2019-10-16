import pytest
from pathlib import Path

examples_path = Path(__file__).parent / 'examples'


@pytest.fixture
def example():
    return lambda p: open(examples_path / p).read()