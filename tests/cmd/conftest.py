import pytest

from _snadra.cmd.base import Commands


@pytest.fixture(scope="session")
def commands():
    return Commands()


@pytest.fixture(scope="session")
def modules_dir(tmp_path_factory):
    files = {
        "module_1.py",
        "module_2.py",
        "module_3",
        "module_4.txt",
    }
    tmp_dir = tmp_path_factory.mktemp("modules_dir")

    for file_name in files:
        file_path = tmp_dir / file_name
        file_path.touch()

    return tmp_dir
