import os
from typing import ClassVar
from starlette.background import BackgroundTask
from fastapi.templating import Jinja2Templates
from jinja2.loaders import split_template_path
from .extension import IncludeBlockExtension


__all__ = ['MY_DIR', 'ThemeTemplates']


MY_DIR = os.path.dirname(__file__)


class ThemeTemplates(Jinja2Templates):
    THEME_NAME: ClassVar[str] = 'justengel_theme'  # Required!
    DIRECTORY: ClassVar[str] = os.path.join(MY_DIR, 'templates')

    DEFAULT_CONTEXT = {
        'site_name': '',
        'title': '',
        }

    DEFAULT_FILTERS = {
        'with_theme': lambda name: name.replace('.html', '') + '.html',  # Replaced with use_theme
        'static': lambda url: url,  # Replaced with static
        }

    def __init__(self, main_directory: str, theme: str = None, static_url: str = None) -> None:
        self.DEFAULT_FILTERS = self.__class__.DEFAULT_FILTERS.copy()
        self.static_url = static_url
        self.theme = theme
        self.available_themes = []

        super().__init__(main_directory)

        # Add extensions
        self.env.add_extension(IncludeBlockExtension)

        # Initialize the themes
        self.init_themes()

        # Add initial defaults
        self.init_defaults()

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

    def init_themes(self):
        """Initialize the available themes."""
        prev_theme = prev_directory = None
        for base in reversed((self.__class__, ) + self.__class__.__bases__):
            theme_name = getattr(base, 'THEME_NAME', None)
            directory = getattr(base, 'DIRECTORY', None)
            if prev_theme != theme_name and prev_directory != directory:
                self.install_theme(theme_name, directory)
            elif prev_theme != theme_name:
                self.install_theme(theme_name)
            elif prev_directory != directory and directory is not None:
                self.add_directory(directory, index=1)
            prev_theme, prev_directory = theme_name, directory

    def install_theme(self, name: str, directory: str = None):
        """Install a theme.

        Args:
            name (str): Name of the theme directory to use
            directory (str)[None]: Directory to add to the loader search path.
                This is required if your theme direct does not exist in the current search path.
        """
        if directory is not None:
            self.add_directory(directory, index=1)  # Add directory to the searchpath
        self.available_themes.insert(0, name)

    def add_directory(self, directory: str, index: int = None):
        """Add a directory to the loader."""
        if directory not in self.env.loader.searchpath:
            if index is not None:
                self.env.loader.searchpath.insert(index, directory)
            else:
                self.env.loader.searchpath.append(directory)

    def exists(self, template: str):
        """Check if a template exists."""
        pieces = split_template_path(template)
        for searchpath in self.env.loader.searchpath:
            filename = os.path.join(searchpath, *pieces)
            if os.path.exists(filename):
                return True
        return False

    def init_defaults(self):
        """Initialize the default context and filters."""
        # Populate instance filters
        self.DEFAULT_FILTERS['with_theme'] = self.with_theme
        self.DEFAULT_FILTERS['static'] = self.static

        self.env.filters.update(self.DEFAULT_FILTERS)

    def set_defaults(self, **kwargs):
        """Change the default context values."""
        self.DEFAULT_CONTEXT.update(**kwargs)

    def get_context(self, **kwargs) -> dict:
        """Get the context values."""
        d = self.DEFAULT_CONTEXT.copy()
        d.update(kwargs)
        return d

    def with_theme(self, name) -> str:
        """Use an available theme with this template name"""
        if not name.endswith('.html'):
            name = name + '.html'

        available = self.available_themes.copy()
        if len(available) > 0 and self.theme != available[0]:
            available = [self.theme] + available

        for theme in available:
            template = os.path.join(theme, name).replace('\\', '/')
            if self.exists(template):
                return template

        return name

    def static(self, url: str, static_url: str = None) -> str:
        if static_url is None:
            static_url = self.static_url
        if static_url:
            return os.path.join(static_url, url)
        return url

    def install_app(self, app, **kwargs) -> 'ThemeTemplates':
        self.set_defaults(**kwargs)
        app.templates = self
        return self
