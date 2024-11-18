# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'Simulation of Stationary Energy Storage Systems'
copyright = '2023, Technical University of Munich, Chair of Electrical Energy Storage Technology'
# author = 'tbd'

# The full version, including alpha/beta/rc tags
# release = '1.3.5'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',  # enable Napoleon Sphinx v>1.3
    'sphinx.ext.extlinks'  # enables external links with a key
]

napoleon_google_docstring = True
napoleon_numpy_docstring = True
autodoc_inherit_docstrings = False
autodoc_typehints = 'none'

master_doc = 'index'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store','_source']
add_module_names = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_logo = "./SimSES_Logo_black.png"

# html_theme_options = {
#     'logo': 'SimSES.png'
# }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

latex_elements = {
    'papersize': 'a4paper',
    'printindex': '\\footnotesize\\raggedright\\printindex',
    'fncychap': r'\usepackage[Bjornstrup]{fncychap}',
    'pointsize': '12pt'}


latex_documents = [
  (master_doc, 'simses.tex', 'SimSES',
   'Marc Möller, Daniel Kucevic', 'manual'),
]
