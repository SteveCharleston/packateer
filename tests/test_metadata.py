import pytest
from packateerlib import Metadata


def test_nopath(monkeypatch):
    monkeypatch.chdir("/tmp/")
    with pytest.raises(FileNotFoundError):
        m = Metadata(None)


def test_missing_path(monkeypatch):
    monkeypatch.chdir("/tmp/")
    with pytest.raises(FileNotFoundError):
        m = Metadata("metadata.yaml")


def test_minimal_dists_pkg(tmpdir, minimal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(minimal_yaml)

    m = Metadata(yaml, "debian", "test")
    assert m.packages == ["test"]
    assert m.dists == ["debian"]


def test_minimal_no_params(tmpdir, minimal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(minimal_yaml)

    m = Metadata(yaml)
    assert m.packages == []
    assert m.dists == []


def test_minimal_lists_params(tmpdir, minimal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(minimal_yaml)

    m = Metadata(yaml, dists="foo bar baz", packages="uno does tres")
    assert m.dists == ["foo", "bar", "baz"]
    assert m.packages == ["uno", "does", "tres"]

def test_normal_no_params(tmpdir, normal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(normal_yaml)

    m = Metadata(yaml)
    assert set(m.packages) == set(["aptly", "fpm", "emptypkg", "testpkg"])
    assert set(m.dists) == set(["ubuntu1604", "ubuntu1804", "foodist", "centos7"])
