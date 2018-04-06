# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
from datetime import date
import os
import sys

sys.path.insert(0, os.path.abspath(r'..'))
from isogeo_pysdk import (Isogeo, IsogeoChecker, IsogeoTranslator,
                          IsogeoUtils, __version__)

# -- Build environment -----------------------------------------------------
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
   

# -- Project information -----------------------------------------------------

project = 'Isogeo PySDK'
author = 'Julien M. @ Isogeo'
copyright = u'2016 - {0}, {1}'.format(date.today().year, author)

# The short X.Y version
version = __version__
# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
#language = 'fr'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "samples/*", "Thumbs.db", ".DS_Store",
                    "*env*", "libs/*"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'

if on_rtd:
    html_theme = 'default'
else:
    import guzzle_sphinx_theme
    html_theme = 'guzzle_sphinx_theme'
    html_theme_path = guzzle_sphinx_theme.html_theme_path()
    extensions.append("guzzle_sphinx_theme")
    # Guzzle theme options
    html_theme_options = {
        "project_nav_name": project,

        # Path to a touch icon
        "touch_icon": "",

        # Specify a base_url used to generate sitemap.xml links. If not
        # specified, then no sitemap will be built.
        "base_url": "http://isogeo-api-pysdk.readthedocs.io",

        # Allow a separate homepage from the master_doc
        # "homepage": "index",

        # Allow the project link to be overriden to a custom URL.
        "projectlink": "https://github.com/Guts/isogeo-api-py-minsdk/",
    }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'IsogeoPySDK_doc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'IsogeoPySDK.tex', 'Isogeo PySDK Documentation',
     'Isogeo PySDK', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'isogeopysdk', 'Isogeo PySDK Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'IsogeoPySDK', 'Isogeo PySDK Documentation',
     author, 'IsogeoPySDK', 'Isogeo API Python SDK.',
     'Miscellaneous'),
]


# -- Options for Sphinx API doc ----------------------------------------------
if on_rtd:
    # handling RTD not supporting apidoc
    # see: https://github.com/rtfd/readthedocs.org/issues/1139
    def run_apidoc(_):
        from sphinx.apidoc import main as apidoc_main

        cur_dir = os.path.abspath(os.path.dirname(__file__))
        output_path = os.path.join(cur_dir, '_apidoc')
        modules = os.path.join(cur_dir, os.path.normpath(r"../isogeo_pysdk"))
        exclusions = [
            '../isogeo_pysdk/samples',
        ]
        apidoc_main([None, '-e', '-f', '-M', '-o', output_path, modules] + exclusions)

    def setup(app):
        app.connect('builder-inited', run_apidoc)
else:
    def run_apidoc(_):
        from sphinx.ext.apidoc import main

        cur_dir = os.path.abspath(os.path.dirname(__file__))
        output_path = os.path.join(cur_dir, '_apidoc')
        modules = os.path.join(cur_dir, r"..\isogeo_pysdk")
        exclusions = [
            '../isogeo_pysdk/samples',
        ]
        main(['-e', '-f', '-M', '-o', output_path, modules] + exclusions)

    def setup(app):
        app.connect('builder-inited', run_apidoc)
