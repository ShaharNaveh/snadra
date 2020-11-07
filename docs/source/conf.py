import datetime
import os
import sys

import sphinx_rtd_theme  # noqa: F401

import snadra

snadra_root = os.path.dirname(snadra.__file__)
sys.path.insert(0, snadra_root)


project = "snadra"
author = "ShaharNaveh"
copyright = f"2020-{datetime.datetime.now().year}, {author}"
version = snadra.__version__
release = version

exclude_patterns = []

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "numpydoc",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

templates_path = ["_templates"]



html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


autoclass_content = "both"
html_show_sourcelink = False

#sphinx.ext.autosummary
autosummary_generate = True

# sphinx.ext.autodoc
autodoc_inherit_docstrings = True

# sphinx_autodoc_typehints
set_type_checking_flag = True
typehints_fully_qualified = True
