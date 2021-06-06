"""
Display credentials
"""
from typing import TYPE_CHECKING

from sqlalchemy import insert
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from snadra._core.db.config import async_session
from snadra._core.db.models import Credential
import snadra._utils as snutils
from snadra._utils import CommandMeta

if TYPE_CHECKING:
    import argparse


class Command(CommandMeta):
    """
    Help message for "creds".
    """

    keywords = {"creds"}
    description = "List all credentials in the database"
    long_help = "LONG HELP FOR CREDS command"

    arguments = {}

    async def run(self, args: "argparse.Namespace") -> None:
        """
        List all credentials in the database.

        Parameters
        ----------
        args : :class:`argparse.Namespace`
            The arguments for the command.
        """
        snutils.console.log("It's working!")
        async with async_session() as session:
            async with session.begin():
                session.add_all(
                    [
                        Credential(
                            credtype="cool cred type",
                            domain="cool domain",
                            username="cool user",
                            password="cool password",
                            host="cool host",
                            os="Linux",
                            sid="",
                            notes="Some notes",
                        )
                    ]
                )
                # await session.commit()
                stmt = select(Credential)
                snutils.console.log(f"{stmt=}")
                result = await session.execute(stmt)
                snutils.console.log(f"{result=}")

                for a1 in result.scalars():
                    snutils.console.log(a1)
                    # snutils.console.log(f"created at: {a1.create_date}")

        # stmt = select(A).options(selectinload(A.bs))

        # async with Session.begin() as session:
        # session.add(Credential(username="example_user_1", password="1234"))
