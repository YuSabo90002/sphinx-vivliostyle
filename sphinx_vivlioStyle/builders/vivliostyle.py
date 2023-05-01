import os
from typing import Any, Dict
import subprocess

from docutils.nodes import Node
from docutils import nodes
from .translator import vivlioStyleTransrator

from docutils.io import StringOutput
from io import open
from os import path
from sphinx.builders.singlehtml import SingleFileHTMLBuilder
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import ensuredir, os_path
from sphinx.application import Sphinx

logger = logging.getLogger(__name__)

class vivlioStyleBuilder(SingleFileHTMLBuilder):
    name = "vivliostyle"
    format = "vfm"  # Must be html instead of "pdf", otherwise plantuml has problems
    epilog = __('The markdown files are in %(outdir)s.')
    file_suffix = ".pdf"
    out_suffix='.md'
    links_suffix = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.app.config.vivlioStyle_theme is not None:
            print(f"Setting theme to {self.app.config.vivlioStyle_theme}")
            self.app.config.html_theme = self.app.config.vivlioStyle_theme

        # We need to overwrite some config values, as they are set for the normal html build, but
        # vivlioStyle can normally not handle them.
        self.app.config.html_sidebars = self.app.config.vivlioStyle_sidebars;
        self.app.config.html_theme_options = self.app.config.vivlioStyle_theme_options;  # Sphinx would write warnings, if given options are unsupported.

        # Add vivlioStyle specific functions to the html_context. Mostly needed for printing debug information.
        self.app.config.html_context['vivlioStyle_debug'] = self.config['vivlioStyle_debug']
        self.app.config.html_permalinks=False

    def get_config_var(self, name, default):
        """
        Gets a config variables for scss out of the Sphinx configuration.
        If name is not found in config, the specified default var is returned.

        Args:
            name: Name of the config var to use
            default: Default value, if name can not be found in config

        Returns: Value
        """
        vivlioStyle_vars = self.app.config.vivlioStyle_vars
        if name not in vivlioStyle_vars:
            return default
        return vivlioStyle_vars[name]

    def get_theme_option_var(self, name, default):
        """
        Gets a option  variables for scss out of the Sphinx theme options.
        If name is not found in theme options, the specified default var is returned.

        Args:
            name: Name of the option var to use
            default: Default value, if name can not be found in config

        Returns: Value
        """
        vivlioStyle_theme_options = self.app.config.vivlioStyle_theme_options
        if name not in vivlioStyle_theme_options:
            return default
        return vivlioStyle_theme_options[name]
    
    def write_additional_files(self):
        super().write_additional_files()
        back_outsuffinx=self.out_suffix
        self.out_suffix=".html"
        ctx=self.get_doc_context("","","")
        self.out_suffix=back_outsuffinx
        self.handle_page("contents",ctx,"toc.html")
        self.out_suffix=".js"
        self.handle_page("vivliostyle.config",ctx,"vivliostyle.config.js")

    def fix_refuris(self, tree: Node) -> None:
        fname=self.config.root_doc + self.out_suffix
        for refnode in tree.findall(nodes.reference):
            if 'refuri' not in refnode:
                continue
            refnode['refuri']=f"{fname}#{refnode.astext()}"
    
    def author_add(app,pagename,templatename,context,doctree):
        context.update(author=app.config.author)


    def finish(self) -> None:
        self.finish_tasks.add_task(super().gen_pages_from_extensions)
        super().finish()

        index_path = self.app.outdir

        args = [ 'vivliostyle','build' ]

        #if isinstance(self.config['vivlioStyle_flags'], list) and (0 < len(self.config['vivlioStyle_flags'])) :
            #args.extend(self.config['vivlioStyle_flags'])

        timeout = self.config['vivlioStyle_timeout']

        
        retries = self.config['vivlioStyle_retries']

        for n in range(1 + retries):
            try:
                subprocess.run(args,cwd=index_path)
                break
            except subprocess.TimeoutExpired:
                logger.warning(f"TimeoutExpired in weasyprint, retrying")

                if  n == retries-1:
                    raise RuntimeError(f"maximum number of retries {retries} failed in weasyprint")


def setup(app: Sphinx) -> Dict[str, Any]:
    app.set_translator('vivliostyle',vivlioStyleTransrator)
    app.add_config_value("vivlioStyle_vars", {}, "html", types=[dict])
    app.add_config_value("vivlioStyle_file_name", None, "html", types=[str])
    app.add_config_value("vivlioStyle_debug", False, "html", types=bool)
    app.add_config_value("vivlioStyle_timeout", None, "html", types=[int])
    app.add_config_value("vivlioStyle_retries", 0, "html", types=[int])
    app.add_config_value("vivlioStyle_flags", None, "html", types=[list])
    app.add_config_value("vivlioStyle_theme", "vivlioStyle_theme", "html", types=[str])
    app.add_config_value("vivlioStyle_theme_options", {}, "html", types=[dict])
    app.add_config_value("vivlioStyle_sidebars", {'**': ["localtoc.html"]}, "html", types=[dict])
    app.add_builder(vivlioStyleBuilder)
    app.connect("html-page-context",vivlioStyleBuilder.author_add)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
