import pytest

minimal = """
"""

normal = """
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
    testpkg:
        Version: 1.0.0
    emptypkg: {}

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
            testpkg: {}
"""

@pytest.fixture()
def minimal_yaml():
    return minimal

@pytest.fixture()
def normal_yaml():
    return normal
