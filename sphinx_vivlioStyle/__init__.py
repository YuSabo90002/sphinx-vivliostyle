from sphinx_vivlioStyle.directives.ifbuilder import IfBuilderDirective
from sphinx_vivlioStyle.directives.ifinclude import IfIncludeDirective
from sphinx_vivlioStyle.directives.pdfinclude import PdfIncludeDirective


def setup(app):
    app.add_directive('if-builder', IfBuilderDirective)
    app.add_directive('if-include', IfIncludeDirective)
    app.add_directive('pdf-include', PdfIncludeDirective)

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
