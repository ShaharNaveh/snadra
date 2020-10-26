"""
Testing general things about the commands
"""
from typing import List


def test_no_duplicate_keywords(command_parser):
    """
    Check if two commands or more are sharing the same keyword.
    """
    result: List[str] = []
    for command in command_parser.commands:
        for keyword in command.KEYWORDS:
            result.append(keyword)

    expected = list(set(result))
    assert sorted(result) == sorted(expected)
