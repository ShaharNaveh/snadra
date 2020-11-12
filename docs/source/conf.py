import datetime
import os
import sys

import snadra

snadra_root = os.path.dirname(snadra.__file__)
sys.path.insert(0, snadra_root)

SRC_PATH = os.path.dirname(snadra_root)


project = "snadra"
author = "ShaharNaveh"
copyright = f"2020-{datetime.datetime.now().year}, {author}"
version = snadra.__version__
release = version

exclude_patterns = []

extensions = [
    "autoapi.extension",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",  # Needs to be loaded after napoleon
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "pygments": ("https://pygments.org", None),
    "python": ("https://docs.python.org/3", None),
}

templates_path = ["_templates"]

header = """\
.. currentmodule:: snadra
.. ipython:: python
   :suppress:
   import snadra
"""


html_theme = "alabaster"

html_sidebars = {
    "**": [
        "about.html",
        "searchbox.html",
        "localtoc.html",
        "relations.html",
    ]
}


html_theme_options = {
    "fixed_sidebar": False,
    "show_powered_by": False,
    "github_user": "ShaharNaveh",
    "github_repo": "snadra",
    "github_banner": False,
    "show_related": False,
    "sidebar_collapse": True,
}

html_static_path = ["_static"]

html_show_sourcelink = False

# autoapi.extension
autoapi_type = "python"
autoapi_dirs = [SRC_PATH]
autoapi_member_order = "groupwise"
autoapi_keep_files = True
autoapi_template_dir = "_templates/_autoapi_templates"

# sphinx.ext.autosummary
autosummary_generate = True
autosummary_imported_members = False

# sphinx.ext.autodoc
autodoc_typehints = "description"
autoclass_content = "both"
autodoc_member_order = "groupwise"
autodoc_inherit_docstrings = True

# sphinx_autodoc_typehints
set_type_checking_flag = True
typehints_fully_qualified = True
