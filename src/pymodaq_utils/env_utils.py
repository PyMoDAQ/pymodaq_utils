import os
import sys

from importlib import metadata
from importlib.metadata import PackageNotFoundError
from pathlib import Path

def guess_virtual_environment() -> str:
    '''
        Try to guess the current python environment used.

        Returns
        -------
        str: the guessed environment name or the string "unknown"
    '''
    def _venv_name_or_path():
        #Try to guess from system environment
        for var in ['VIRTUAL_ENV', 'CONDA_DEFAULT_ENV', 'PYENV_VERSION', 'TOX_ENV_NAME']:
            value = os.environ.get(var)
            if value:
                return value
        #if true, probably running in a venv
        if sys.prefix != sys.base_prefix:
            return sys.prefix
        return 'unknown'
    return Path(_venv_name_or_path()).name


def hash_pymodaq_packages_version() -> str:
        import hashlib
        versions = []
        for package in ['pymodaq_utils', 'pymodaq_data', 'pymodaq_gui', 'PyMoDAQ']:
            try:
                versions.append(metadata.version(package))
            except PackageNotFoundError:
                #package not found, it can be skipped
                pass
        hashed = hashlib.sha256(''.join(versions).encode())
        return hashed.digest()[:8].hex()
