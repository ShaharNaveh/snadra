"""
Main application entry point.

This gets ran when you execute:

$ snadra

or

$ python -m snadra
"""
import asyncio

from snadra._core.db.base import start_db
from snadra._core.db.config import engine
from snadra._core.parsers import CommandParser


async def main():
    snadra_console = CommandParser()
    snadra_console._setup_prompt()

    await asyncio.create_task(start_db(engine=engine))
    await snadra_console.run()


if __name__ == "__main__":
    asyncio.run(main())
