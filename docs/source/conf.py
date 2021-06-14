import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
# sys.path.insert(0, os.path.abspath('C:/Users/79016/GT/api/'))
extensions = ['sphinx.ext.autodoc', 'sphinx_markdown_builder']
project = 'GT-Test'
copyright = '2021'
author = 'AnastasiaDDM'
version = ''
release = '0.1'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = ['_static']
language = 'ru'
