"""
Script to be run to compare JSON file and a JSON file of API response.

Both files need to be saved in the `scripts` folder in directory before running.

You can then run this script by running: 
`python manage.py runscript affils_compare` in the command line from the directory.

Follow steps outlined in [tutorial.md](
doc/tutorial.md/#running-the-loadpy-script-to-import-data-into-the-database).
"""

from pathlib import Path
import os
import json
from deepdiff import DeepDiff  # type: ignore

CURRENT_DIR = os.path.dirname(__file__)
FILENAME = os.path.join(CURRENT_DIR, "affils_diff_output.txt")

AFFIL_JSON_PATH = Path(__file__).parent / "affiliations.json"
AFFIL_RESPONSE_PATH = Path(__file__).parent / "affils_response.json"


def run():
    """Compare JSON file to API response and return a txt file of any differences."""
    with open(AFFIL_JSON_PATH, encoding="utf-8") as f, open(
        AFFIL_RESPONSE_PATH, encoding="utf-8"
    ) as f2:
        affils_json = json.load(f)
        affils_response = json.load(f2)
        affils_json_dict = {}
        affils_response_dict = {}

        # Build dict for each file.
        for affil in affils_json:
            affil_id = affil["affiliation_id"]
            affils_json_dict[affil_id] = affil
        for affil in affils_response:
            affil_id = affil["affiliation_id"]
            affils_response_dict[affil_id] = affil

        # Compare both files
        diff = DeepDiff(affils_json_dict, affils_response_dict)
        with open(FILENAME, "w", encoding="utf-8") as f:
            print(diff, file=f)
