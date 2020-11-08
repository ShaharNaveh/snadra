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
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
]

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

templates_path = ["_templates"]


html_theme = "sphinx_rtd_theme"
html_sidebars = {
    "**": [
        "about.html",
        "searchbox.html",
        "localtoc.html",
        "relations.html",
    ]
}

"""
html_theme_options = {
    "logo": "logo.png",
    "show_powered_by": False,
    "fixed_sidebar": True,
    "sidebar_collapse": True,
    #'github_button': False,
}
"""

html_static_path = ["_static"]


html_show_sourcelink = False

# sphinx.ext.autosummary
autosummary_generate = True

# sphinx.ext.autodoc
autoclass_content = "both"
autodoc_member_order = "groupwise"
autodoc_inherit_docstrings = True

# sphinx_autodoc_typehints
set_type_checking_flag = True
typehints_fully_qualified = True
