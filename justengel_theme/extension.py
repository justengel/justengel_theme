import os
from jinja2 import lexer, nodes
from jinja2.ext import Extension
from jinja2.filters import do_mark_safe


__all__ = ['IncludeBlockExtension']


class IncludeBlockExtension(Extension):
    tags = {'include_block'}
    fields = {'template', 'block_name'}  # block_name is optional

    def template_contents(self, template, *args, **kwargs):
        """Helper callback."""
        tmp = self.environment.loader.get_source(self.environment, template)
        if isinstance(tmp, tuple):
            return tmp[0]
        return ''

    def value_from_filter(self, node):
        filts = []
        while isinstance(node, nodes.Filter):
            filt = self.environment.filters.get(node.name, None)
            if filt is not None:
                filts.append(filt)
            node = node.node

        if isinstance(node, nodes.Const):
            node = node.value

        for f in reversed(filts):
            node = f(node)

        if not isinstance(node, str):
            node = node
        return node

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        template = self.value_from_filter(parser.parse_expression())
        if parser.stream.current.type != 'block_end':
            block_name = self.value_from_filter(parser.parse_expression())
        else:
            block_name = os.path.basename(os.path.splitext(template)[0])
        content = self.template_contents(template)
        content = '{{% block {name} %}}{content}{{% endblock {name} %}}'.format(name=block_name, content=content)
        new_stream = self.environment._tokenize(content, template, filename=template, state=None)
        next(new_stream)
        old_stream, parser.stream = parser.stream, new_stream

        node = parser.parse_block()
        node.lineno = lineno

        parser.stream = old_stream

        return node
