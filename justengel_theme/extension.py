from jinja2 import lexer, nodes
from jinja2.ext import Extension
from jinja2.filters import do_mark_safe


class IncludeOverrideExtension(Extension):
    tags = {'include_override'}

    def parse_import_context(self, node, default):
        if self.stream.current.test_any(
                "name:with", "name:without"
                ) and self.stream.look().test("name:context"):
            node.with_context = next(self.stream).value == "with"
            self.stream.skip()
        else:
            node.with_context = default
        return node

    def parse(self, parser):
        node = nodes.Include(lineno=next(parser.stream).lineno)
        node.template = parser.parse_expression()
        if parser.stream.current.test("name:ignore") and parser.stream.look().test(
                "name:missing"
                ):
            node.ignore_missing = True
            parser.stream.skip(2)
        else:
            node.ignore_missing = False
        return parser.parse_import_context(node, True)

    # def parse(self, parser):
    #     lineno = next(parser.stream).lineno
    #     token = parser.stream.expect(lexer.TOKEN_STRING)
    #     template = nodes.Const(token.value)
    #     token = parser.stream.current
    #     if token.value == '|':
    #         next(parser.stream)
    #         filt_name = parser.stream.current.value
    #         next(parser.stream)
    #         filt = self.environment.filters.get(filt_name, None)
    #         if filt is not None:
    #             template.value = filt(template.value)
    #     call = self.call_method('include_override', [template], lineno=lineno)
    #     return nodes.Output([call], lineno=lineno)

    def include_override(self, template):
        """Helper callback."""
        tmp = self.environment.loader.get_source(self.environment, template)
        if isinstance(tmp, tuple):
            # return tmp[0]
            return do_mark_safe(tmp[0])
        return ''
