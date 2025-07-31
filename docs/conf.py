#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. codeauthor:: Hugo Plombat - LUPM <hugo.plombat@umontpellier.fr> & Wilfried Mercier - IRAP/LAM <wilfried.mercier@ilam.fr>

Configuration script for Sphinx documentation.
"""

from __future__ import annotations

import sys
import os

# Required for autodoc to work
sys.path.append(os.path.abspath('../..'))

def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip

###################################################
#               Project information               #
###################################################

project            = 'SFHandle'
copyright          = '2025, Wilfried Mercier'
author             = 'Wilfried Mercier'
show_authors       = True

autodoc_type_aliases = {'Interp_kind': 'Interp_kind'}

highlight_options  = {'default': {'lexers.python.PythonLexer'},
                     }

extensions         = ['sphinx.ext.autodoc',
                      'sphinx.ext.mathjax',
                      'sphinx.ext.viewcode',
                      'sphinx.ext.autosummary',
                      'sphinx.ext.intersphinx',
                      'jupyter_sphinx',
                      "sphinx_design"
                     ]

# The full version, including alpha/beta/rc tags
release            = '0.1'

# Add any paths that contain templates here, relative to this directory.
#templates_path     = ['_templates']
exclude_patterns   = []

#######################################################
#               Options for HTML output               #
#######################################################

html_theme = "pydata_sphinx_theme"

html_title = 'SFHandle'

# Force light mode by default
html_context = {"default_mode" : "light"}

html_theme_options = {
    "icon_links": [
        {
            # Label for this link
            "name": "GitHub",
            
            # URL where the link will redirect
            "url": "https://github.com/WilfriedMercier/SFHandle.git",
            
            # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "icon": "fa-brands fa-square-github",
            
            # The type of image to be used (see below for details)
            "type": "fontawesome",
        }],
    
    "logo": {
        
        # Alt text for blind people
        #"alt_text"    : "SFHandle documentation - Home",
        #"text"        : "SFHandle",
        #"image_light" : "_static/logo1.png",
        #"image_dark"  : "_static/logo1.png",
    },
    
    #"announcement"    : "",
    "show_nav_level"  : 2
}

# Add sypport for custom css file
html_static_path = ["_static"]
html_css_files   = ["mycss.css"]

html_collapsible_definitions = True

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

rst_prolog = """
.. role:: python(code)
  :language: python
  :class: highlight
  
.. _Row: https://docs.astropy.org/en/stable/api/astropy.table.Row.html
.. _NDArray: https://numpy.org/devdocs/reference/typing.html#numpy.typing.NDArray
.. _ArrayLike: https://numpy.org/devdocs/reference/typing.html#numpy.typing.ArrayLike
.. _Cigale: https://cigale.lam.fr/
.. _interp1d: https://docs.scipy.org/doc/scipy-1.16.0/reference/generated/scipy.interpolate.interp1d.html
"""

