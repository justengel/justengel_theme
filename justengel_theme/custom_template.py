import os
from starlette.background import BackgroundTask
from fastapi.templating import Jinja2Templates


__all__ = ['MY_DIR', 'ThemeTemplates']


MY_DIR = os.path.dirname(__file__)


class ThemeTemplates(Jinja2Templates):
    BASE_DIR = os.path.join(MY_DIR, 'templates')  # All defined BASE_DIR's will be used
    BASE_THEME = 'justengel_theme'

    DEFAULT_CONTEXT = {
        'site_name': '',
        'title': '',
        }

    DEFAULT_FILTERS = {
        'with_theme': lambda name: name.replace('.html', '') + '.html',  # Replaced with use_theme
        'static': lambda url: url,  # Replaced with static
        }

    def __init__(self, directory: str = None, static_url: str = None, theme: str = 'justengel_theme') -> None:
        self.DEFAULT_FILTERS = self.__class__.DEFAULT_FILTERS.copy()
        self.static_url = static_url
        self.theme = theme

        if directory is None:
            directory = self.BASE_DIR
        super().__init__(directory)

        # Add all subclass base directories
        if self.BASE_DIR != directory:
            self.add_directory(self.BASE_DIR)
        for base in self.__class__.__bases__:
            base_dir = getattr(base, 'BASE_DIR', None)
            if base_dir is not None and os.path.exists(base_dir):
                self.add_directory(base_dir)

        # Add initial defaults
        self.init_defaults()

    def add_directory(self, directory: str):
        """Add a directory to the loader."""
        if directory not in self.env.loader.searchpath:
            self.env.loader.searchpath.append(directory)

    def TemplateResponse(
            self,
            name: str,
            context: dict,
            status_code: int = 200,
            headers: dict = None,
            media_type: str = None,
            background: BackgroundTask = None,
            ):

        ctx = self.get_context()
        ctx.update(context)

        return super().TemplateResponse(name, ctx, status_code, headers, media_type, background)

    # ===== Helper functions =====
    def init_defaults(self):
        # Populate instance filters
        self.DEFAULT_FILTERS['with_theme'] = self.with_theme
        self.DEFAULT_FILTERS['static'] = self.static

        self.env.filters.update(self.DEFAULT_FILTERS)

    def set_defaults(self, **kwargs):
        self.DEFAULT_CONTEXT.update(**kwargs)

    def get_context(self, **kwargs) -> dict:
        d = self.DEFAULT_CONTEXT.copy()
        d.update(kwargs)
        return d

    def with_theme(self, name) -> str:
        if not name.endswith('.html'):
            name = name + '.html'
        path = os.path.join(self.theme, name).replace('\\', '/')
        if not path.startswith('/'):
            return '/' + path
        return path

    def static(self, url: str, static_url: str = None) -> str:
        if static_url is None:
            static_url = self.static_url
        if static_url:
            return os.path.join(static_url, url)
        return url

    def install(self, app, **kwargs) -> 'ThemeTemplates':
        self.set_defaults(**kwargs)
        app.templates = self
        return self
