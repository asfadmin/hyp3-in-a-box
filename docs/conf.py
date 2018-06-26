#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Hyp3 In A Box documentation build configuration file, created by
# sphinx-quickstart on Tue Jun  5 11:11:18 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

paths = [
    '../lambdas/find_new_granules/src',
    '../lambdas/scheduler/src',
    '../lambdas/send_email/src',
    '../lambdas',
    '../lambdas/setup_db/src',
    '../cloudformation/tropo',
    '../modules/hyp3_db/src',
    '../modules/hyp3_events/src',
    '../modules/granule_search/src',
    '..'
]

for p in paths:
    sys.path.insert(0, os.path.abspath(p))


def setup(app):
    app.add_stylesheet('css/no-bullet-lists.css')


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Hyp3 In A Box'
copyright = '2018, William Horn, Rohan Weeden'  # pylint: disable=E0102
author = 'William Horn, Rohan Weeden'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.0.1'
# The full version, including alpha/beta/rc tags.
release = '0.0.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'logo': 'images/satellite.png',
    'logo_name': True,
    'description': "Portable version of asf's HyP3 procecssing system",
    'github_user': 'asfadmin',
    'github_repo': 'hyp3-in-a-box',
    'extra_nav_links': {
        'HyP3 On-Demand Processing': 'http://hyp3.asf.alaska.edu/',
        'HyP3 API': 'http://hyp3.asf.alaska.edu://api.hyp3.asf.alaska.edu/',
        'Find Granules': 'https://vertex.daac.asf.alaska.edu/',
        'ASF Website': 'https://www.asf.alaska.edu/'
    },
    'sidebar_width': '240px',
    'page_width': '1150px',
    'show_related': True
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
        'donate.html',
    ]
}

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Hyp3InABoxdoc'


# -- Options for LaTeX output ---------------------------------------------

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
    (master_doc, 'Hyp3InABox.tex', 'Hyp3 In A Box Documentation',
     'William Horn, Rohan Weeden', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'hyp3inabox', 'Hyp3 In A Box Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Hyp3InABox', 'Hyp3 In A Box Documentation',
     author, 'Hyp3InABox', 'One line description of project.',
     'Miscellaneous'),
]
