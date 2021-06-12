"""
Main application entry point.

This gets ran when you execute:

$ snadra

or

$ python -m snadra
"""
import asyncio
import sys

from _snadra.cmd import CommandParser
from _snadra.db.config import async_session, engine
from _snadra.db.utils import insert_default_rows, start_db


async def main():
    snadra_console = CommandParser()
    snadra_console._setup_prompt()

    await asyncio.create_task(start_db(engine=engine))
    await asyncio.create_task(insert_default_rows(session=async_session))
    await snadra_console.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
