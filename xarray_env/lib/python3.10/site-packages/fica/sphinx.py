"""fica Sphinx extension"""

import importlib

from docutils.parsers.rst import directives
from sphinx.directives.code import CodeBlock
from sphinx.util.typing import OptionSpec

from .exporter import create_exporter
from .version import __version__


LEXER_OVERRIDES = {
    "json": "javascript",
}
"""alternative Pygments lexers to use for specific export formats"""


def import_and_get_config(object_path: str, exporter_type: str) -> str:
    """
    Import a :py:class:`Config<fica.Config>` subclass from a library and return its exported
    documentation string in the specified format.

    Args:
        object_path (``str``): a string containing the object to import and the library it is
            imported from, e.g. ``fica_demo.Config``
        exporter_type (``str``): the type of exporter to use; see
            :py:func:`fica.exporter.create_exporter`

    Returns:
        ``str``: the code block contents documenting the configurations in the imported object
    """
    mod, cls = object_path.rsplit(".", 1)
    module = importlib.import_module(mod)
    config_object = getattr(module, cls)
    return create_exporter(exporter_type).export(config_object)


class FicaDirective(CodeBlock):
    """
    A Sphinx directive for documenting a :py:class:`fica.Config` object.

    This directive subclasses Sphinx's code block directive, and so the resulting documentation
    string for the config object is displayed as a Sphinx code block with Pygments syntax
    highlighting. The behavior of Sphinx's underlying code block arguments are unaffected.
    """

    option_spec: OptionSpec = {
        **CodeBlock.option_spec,
        "format": directives.unchanged,
    }

    def run(self):
        """
        Import the config object and update ``self.content`` to contain the code for the code block.
        """
        if "format" not in self.options:
            self.options["format"] = "yaml"

        self.content = import_and_get_config(self.arguments[0], self.options["format"]).split("\n")
        self.arguments[0] = LEXER_OVERRIDES.get(self.options["format"], self.options["format"])
        return super().run()


def setup(app):
    """
    Add the ``fica`` directive to the Sphinx app.
    """
    app.add_directive("fica", FicaDirective)
    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
