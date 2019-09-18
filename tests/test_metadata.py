import yaml
from unittest.mock import patch, mock_open
from packateerlib import Metadata

minimal_yaml = """
"""
def test_minimal_dists_pkg(monkeypatch):
    with patch("builtins.open", mock_open(read_data=minimal_yaml)) as mock_file:
        m = Metadata("foo", "debian", "test")
        print(m._data)
        assert m.packages == ["test"]

def test_minimal_no_params():
    with patch("builtins.open", mock_open(read_data=minimal_yaml)) as mock_file:
        m = Metadata("foo")
