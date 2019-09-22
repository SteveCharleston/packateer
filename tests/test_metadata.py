import pytest
import yaml
from unittest.mock import patch, mock_open
from packateerlib import Metadata
from pathlib import Path

minimal_yaml = """
"""

normal_yaml = """
vars:
    pkgpath: ./packages/
    distpath: ./dists/
    repopath: ./repos/

packages:
    aptly:
        Version: 1.4.0
        vars:
            downloadurl: "https://github.com/aptly-dev/aptly/releases/download/v1.4.0/aptly_1.4.0_linux_amd64.tar.gz"
    fpm:
        Version: 1.11.0

dists:
    debian:
        pkgformat: deb
        distname: wheezy
        abstract: true
        packages:
            fpm:
                pkg-rev: 0
    ubuntu1604:
        pkgformat: deb
        distname: xenial
        parent: debian
        packages:
            test:
                Breaks: breaker
                vars:
                    metaubuntu: erben
    ubuntu1804:
        distname: bionic
        parent: debian

    foodist:
        parent: ubuntu1604
        packages:
            test:
                pkg-rev: 0
                vars:
                    une: does

    centos7:
        pkgformat: rpm
        vars:
            httpduser: 48
            httpdusername: apache
            httpdgroup: 48
            httpdgroupname: apache
            proxygroup: 23
            proxygroupname: squid
        packages:
            test:
                pkg-rev: 0
"""

def test_nopath(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: False)
    with pytest.raises(FileNotFoundError):
        m = Metadata(None)

def test_minimal_dists_pkg(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    with patch("builtins.open", mock_open(read_data=minimal_yaml)) as mock_file:
        m = Metadata("dummypath", "debian", "test")
        assert m.packages == ["test"]
        assert m.dists == ["debian"]

def test_minimal_no_params(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    with patch("builtins.open", mock_open(read_data=minimal_yaml)) as mock_file:
        m = Metadata("dummypath")
        assert m.packages == []
        assert m.dists == []

def test_minimal_lists_params(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    with patch("builtins.open", mock_open(read_data=minimal_yaml)) as mock_file:
        m = Metadata("dummypath", dists="foo bar baz", packages="uno does tres")
        assert m.dists == ["foo", "bar", "baz"]
        assert m.packages == ["uno", "does", "tres"]

def test_normal_no_params(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self: True)
    with patch("builtins.open", mock_open(read_data=normal_yaml)) as mock_file:
        m = Metadata("dummypath")
        assert set(m.packages) == set(["aptly", "fpm"])
        assert set(m.dists) == set(["ubuntu1604", "ubuntu1804", "foodist", "centos7"])
