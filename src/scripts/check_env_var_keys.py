"""Makes sure keys in .env.template match those in .env."""

import os
import sys
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

load_dotenv()

TEMPLATE = dotenv_values(Path(os.getenv("AFFILS_WORKING_DIR")) / ".env.template")  # type: ignore
ACTUAL = dotenv_values(Path(os.getenv("AFFILS_WORKING_DIR")) / ".env")  # type: ignore

if __name__ == "__main__":
    if TEMPLATE.keys() != ACTUAL.keys():
        print(".env keys do not match. Check your .env files.")
        sys.exit(1)
