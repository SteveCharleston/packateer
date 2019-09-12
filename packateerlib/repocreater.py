import os
import shlex
import shutil
from contextlib import suppress
from glob import glob
from packateerlib import Dist, Metadata
from pathlib import Path
from subprocess import run
from typing import Dict

class RepoCreater(object):

    """Takes formally build package files and puts them into a repository."""

    def __init__(self, dist: Dist, conf: Metadata) -> None:
        """Initializes all variables that are needed to create the Repository.

        Args:
            dist (Dist): Distribution to build the repository for.
            conf (Metadata): Metadata configuration of this project.


        """
        self._dist = dist
        self._conf = conf

        self._repopath = Path("./repos/") / dist.name
        with suppress(KeyError):
            self._repopath = Path(dist.metadata['repopath']) / dist.name
        

        #Origin: Tfk
        #Label: Tfk
        #Codename: $distname
        #Architectures: i386 amd64
        #Components: main
        #Description: Apt repository for project Tfk
        #SignWith: $GPGKEY

        repodata: Dict[str, str] = dict()

        repodata['Origin'] = dist.name
        with suppress(KeyError):
            repodata['Origin'] = dist.metadata['origin']

        repodata['Label'] = dist.name
        with suppress(KeyError):
            repodata['Label'] = dist.metadata['label']

        repodata['Codename'] = dist.name
        with suppress(KeyError):
            repodata['Codename'] = dist.metadata['distname']

        repodata['Architectures'] = "i386 amd64"
        with suppress(KeyError):
            repodata['Architectures'] = " ".join(dist.metadata['architectures'])

        repodata['Components'] = "main"
        with suppress(KeyError):
            repodata['Components'] = dist.metadata['component']

        with suppress(KeyError):
            repodata['Description'] = dist.metadata['description']

        with suppress(KeyError):
            repodata['SignWith'] = dist.metadata['signwith']

        self._repodata = repodata

    def build(self) -> None:
        """Creates the repository.

        """
        # clean old repo
        shutil.rmtree(self._repopath, ignore_errors=True)
        (self._repopath / "conf").mkdir(parents=True, exist_ok=True)

        # write repo configuration
        with open(self._repopath / "conf" / "distributions", 'w') as f:
            for key, val in self._repodata.items():
                f.write("{}: {}\n".format(key, val))

        # create and execute command for repo building
        debs = glob(str(self._dist._distpath / "*.deb"))
        print(debs)
        cmd = ("reprepro --ask-passphrase --basedir {} includedeb {} {}"
                .format(self._repopath,
                    self._repodata['Codename'],
                    " ".join(debs)))

        run(shlex.split(cmd))
