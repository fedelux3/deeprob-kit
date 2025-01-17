import os
import sys
sys.path.insert(0, os.path.abspath('../'))

# -- Project information -----------------------------------------------------
project = 'DeeProb-kit'
author = 'Lorenzo Loconte'
copyright = '2021, {}'.format(author)
release = version = '0.6.4'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.githubpages',
    'sphinx.ext.viewcode',
    'myst_parser',
    'sphinx_rtd_theme'
]
source_suffix = ['.rst', '.md']
exclude_patterns = ['api/modules.rst']

# -- Options for HTML output -------------------------------------------------
html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'display_version': True,
    'navigation_depth': 6,
    'collapse_navigation': True,
}
html_style = 'css/custom.css'
html_logo = 'deeprob-logo-minimal.svg'
html_only = True

# -- Autodoc settings --------------------------------------------------------
autoclass_content = 'init'
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_default_options = {
    'member-order': 'bysource',
    'special-members': '__call__',
}

# -- MyST settings -----------------------------------------------------------
suppress_warnings = ["myst.header"]
