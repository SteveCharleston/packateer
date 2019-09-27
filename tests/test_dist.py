import pytest
from packateerlib import Metadata, Dist

def test_dist(tmpdir, normal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(normal_yaml)

    m = Metadata(yaml)
    d = Dist("centos7", m)
    assert d.name == "centos7"

def test_metadata(tmpdir, normal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(normal_yaml)

    m = Metadata(yaml)
    d = Dist("centos7", m)

    d.metadata['pkgformat'] == "rpm"

def test_dist_order(tmpdir, normal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(normal_yaml)

    m = Metadata(yaml)
    d = Dist("centos7", m)
    assert d.order == ["centos7", "alldists"]

def test_dist_order_rec(tmpdir, normal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(normal_yaml)

    m = Metadata(yaml)
    d = Dist("foodist", m)
    assert d.order == ["foodist", "ubuntu1604", "debian", "alldists"]

def test_metadata_rec(tmpdir, normal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(normal_yaml)

    m = Metadata(yaml)
    d = Dist("foodist", m)

    assert d.metadata['distname'] == "xenial"

def test_dist_minimal(tmpdir, minimal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(minimal_yaml)

    m = Metadata(yaml)
    d = Dist("centos7", m)
    assert d.name == "centos7"

def test_dist_minimal_metadata(tmpdir, minimal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(minimal_yaml)

    m = Metadata(yaml)
    d = Dist("centos7", m)
    assert d.metadata == {'pkgformat' : 'deb'}

def test_minimal_dist_order(tmpdir, minimal_yaml):
    yaml = tmpdir.join("metadata.yaml")
    yaml.write(minimal_yaml)

    m = Metadata(yaml)
    d = Dist("centos7", m)
    assert d.order == ["centos7", "alldists"]
