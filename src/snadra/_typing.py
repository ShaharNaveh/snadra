"""
Provides custom helpers for type annotating the code base.
"""
import os
from typing import Union

StrPath = Union[str, os.PathLike]
