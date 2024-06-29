"""Allows you to create, read, update, and delete affiliations."""

# Built-in libraries:
import os
import sqlite3
from typing import List, Optional

# In-house code:
from . import logger

DB_FILE = os.environ.get("AFFILS_DB_FILE")


class Affiliation:
    """Define the members and the CRUD methods for an affiliation."""

    # pylint: disable=too-many-instance-attributes,too-few-public-methods

    def __init__(
        self,
        id_: Optional[int] = None,
        name: Optional[str] = None,
        coordinator: Optional[str] = None,
        coordinator_email: Optional[str] = None,
        status: Optional[str] = None,
        type_: Optional[str] = None,
        family: Optional[str] = None,
        members: Optional[List[str]] = None,
        approvers: Optional[List[str]] = None,
        clinvar_submitter_ids: Optional[List[int]] = None,
    ):
        """Initialize an affiliations object.

        Args:
            id_: The affiliation's identifying number.
            name: The full name of the affiliation.
            coordinator: The name of the person in charge of the affiliation.
            coordinator_email: The email of the person in charge of the affiliation.
            status: One of "pending", "active", or "retired".
            type_: One of "expert panel", "working group", or "clinical domain working group".
            family: The clinical domain of the affiliation.
            members: A list of names of the members in the affiliation.
            approvers: A list of names of approvers for the affiliation.
            clinvar_submitter_ids: IDs for submitting their work to ClinVar.
        """
        # pylint: disable=too-many-arguments
        self.id = id_
        self.name = name
        self.coordinator = coordinator
        self.coordinator_email = coordinator_email
        self.status = status
        self.type = type_
        self.family = family
        self.members = members
        self.approvers = approvers
        self.clinvar_submitter_ids = clinvar_submitter_ids
        self.errors: dict = {}

    @classmethod
    def _row_to_affiliation(cls, row: tuple) -> object:
        """Convert table row to instance of affiliations object."""
        return cls(*row)

    @classmethod
    def get_by_id(cls, id) -> Optional['Affiliation']:
        """Return an affiliation matching a given ID."""
        con = sqlite3.connect(DB_FILE)  # type: ignore
        cur = con.cursor()
        try:
            cur.execute(f"SELECT * FROM affiliations WHERE id = {id}")
            result = cur.fetchone()
        except sqlite3.Error as err:
            logger.error("Unable to get all affiliations")
            logger.error("Error code: %s", err.sqlite_errorcode)
            logger.error("Error name: %s", err.sqlite_errorname)
            con.rollback()
            result = None
        con.close()
        if result:
            return cls._row_to_affiliation(result)
        return None

    @classmethod
    def all(cls) -> Optional[List]:
        """Return all affiliations in the database."""
        all_affiliations = []
        con = sqlite3.connect(DB_FILE)  # type: ignore
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM affiliations")
            results = cur.fetchall()
        except sqlite3.Error as err:
            logger.error("Unable to get all affiliations")
            logger.error("Error code: %s", err.sqlite_errorcode)
            logger.error("Error name: %s", err.sqlite_errorname)
            con.rollback()
            results = None
        if results:
            for result in results:
                all_affiliations.append(cls._row_to_affiliation(result))
        con.close()
        return all_affiliations
