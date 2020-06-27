import os
from jinja2 import lexer, nodes
from jinja2.ext import Extension
from jinja2.filters import do_mark_safe


__all__ = ['IncludeBlockExtension']


class IncludeBlockExtension(Extension):
    tags = {'include_block'}

    def template_contents(self, template, *args, **kwargs):
        """Helper callback."""
        tmp = self.environment.loader.get_source(self.environment, template)
        if isinstance(tmp, tuple):
            return tmp[0]
        return ''

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        template = parser.parse_expression()

        filts = []
        while isinstance(template, nodes.Filter):
            filt = self.environment.filters.get(template.name, None)
            if filt is not None:
                filts.append(filt)
            template = template.node

        if isinstance(template, nodes.Const):
            template = template.value

        for f in reversed(filts):
            template = f(template)

        name = os.path.basename(os.path.splitext(template)[0])
        content = self.template_contents(template)
        content = '{{% block {name} %}}{content}{{% endblock {name} %}}'.format(name=name, content=content)
        new_stream = self.environment._tokenize(content, template, filename=template, state=None)
        next(new_stream)
        old_stream, parser.stream = parser.stream, new_stream
        node = parser.parse_block()
        parser.stream = old_stream

        return node
