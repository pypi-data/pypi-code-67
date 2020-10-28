import os
import sys

import appdirs  # type: ignore
from six.moves import configparser

CONFIG_BASENAME = "pip.ini" if sys.platform == "win32" else "pip.conf"


def _get_config_paths():
    user_dir = appdirs.user_config_dir("pip", appauthor=False, roaming=True)
    site_dir = appdirs.site_config_dir("pip", appauthor=False, multipath=True)

    config_files = [
        os.path.join(user_dir, CONFIG_BASENAME),
        os.path.join(site_dir, CONFIG_BASENAME),
    ]
    if sys.platform.startswith("linux"):
        config_files.append("/etc/pip.conf")
    elif sys.platform == "win32" and site_dir is None or site_dir == r".\pip":
        # Add a manual fallback to C:\ProgramData if it could not be programmatically
        # determined
        config_files.append(r"C:\ProgramData\pip\pip.ini")

    return config_files


def read_pip_default_index():
    config_files = _get_config_paths()

    config = configparser.ConfigParser()
    config.read(config_files)

    try:
        return config.get("global", "index-url")
    except configparser.NoSectionError:
        return None
