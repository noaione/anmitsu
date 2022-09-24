from __future__ import annotations

import sys
from os.path import expandvars
from pathlib import Path

__version__ = "0.1.2"
if sys.platform == "win32":
    USER_PATH = Path(expandvars("%LOCALAPPDATA%/AnmitsuAzuki"))
else:
    USER_PATH = Path(expandvars("$HOME/.anmitsu"))


API_BASE_PATH = "https://production.api.azuki.co"
WEB_BASE_PATH = "https://www.azuki.co"
