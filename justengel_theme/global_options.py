import os
from starlette.background import BackgroundTask
from .custom_template import ThemeTemplates


__all__ = ['get_default_theme', 'set_default_theme', 'get_theme', 'set_theme', 'template', 'install_theme',
           'add_directory', 'exists', 'set_defaults', 'get_context', 'with_theme', 'static',
           'get_static_directories', 'serve_static', 'install_app']


THEME: ThemeTemplates = None
DEFAULT_THEME: type = ThemeTemplates
DEFAULT_KWARGS: dict = {}


def get_default_theme() -> 'type':
    """Return the default theme type."""
    global DEFAULT_THEME
    return DEFAULT_THEME


def set_default_theme(theme_type, **default_kwargs):
    """Set the default theme type."""
    global DEFAULT_THEME, DEFAULT_KWARGS
    DEFAULT_THEME = theme_type
    if len(default_kwargs) > 0:
        DEFAULT_KWARGS = default_kwargs


def get_theme() -> 'ThemeTemplates':
    global THEME, DEFAULT_THEME, DEFAULT_KWARGS
    if THEME is None:
        THEME = DEFAULT_THEME(**DEFAULT_KWARGS)
    return THEME


def set_theme(tmp):
    global THEME
    THEME = tmp
    return THEME


def template(name: str, context: dict, status_code: int = 200, headers: dict = None, media_type: str = None,
             background: BackgroundTask = None, **kwargs):
    return get_theme().TemplateResponse(name, context, status_code=status_code, headers=headers,
                                  media_type=media_type, background=background, **kwargs)


def install_theme(name: str, directory: str = None):
    return get_theme().install_theme(name, directory=directory)


def add_directory(directory: str, index: int = None):
    return get_theme().add_directory(directory, index=index)


def exists(template: str) -> bool:
    return get_theme().exists(template)


def set_defaults(**kwargs):
    return get_theme().set_defaults(**kwargs)


def get_context(**kwargs) -> dict:
    return get_theme().get_context(**kwargs)


def with_theme(self, name) -> str:
    return get_theme().with_theme(name)


def static(url: str, static_url: str = None) -> str:
    return get_theme().static(url, static_url=static_url)


def get_static_directories():
    """Iterator for static directories."""
    return get_theme().get_static_directories()


def serve_static(app, static_url: str = None):
    return get_theme().serve_static(app, static_url=static_url)


def install_app(app, serve_static: bool = False, **kwargs) -> 'ThemeTemplates':
    return get_theme().install_app(app, serve_static=serve_static, **kwargs)
