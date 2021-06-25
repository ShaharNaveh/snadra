import pytest

from _snadra.cmd.utils import iter_dir


def test_iter_dir(modules_dir):
    result = [path.name for path in iter_dir(modules_dir)]
    expected = ["module_1.py", "module_2.py"]
    assert sorted(result) == sorted(expected)


def test_iter_dir_skip(modules_dir):
    skip = {"module_2"}
    result = [path.name for path in iter_dir(modules_dir, skip=skip)]
    expected = ["module_1.py"]
    assert sorted(result) == sorted(expected)


def test_iter_dir_include_suffix(modules_dir):
    include_suffixes = {".txt"}
    result = [
        path.name for path in iter_dir(modules_dir, include_suffixes=include_suffixes)
    ]
    expected = ["module_4.txt"]
    assert sorted(result) == sorted(expected)
