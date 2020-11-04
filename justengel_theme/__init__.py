from .__meta__ import version as __version__

from .custom_template import MY_DIR, ThemeTemplates

from .global_options import get_default_theme, set_default_theme, get_theme, set_theme, template, install_theme, \
    add_directory, exists, set_defaults, get_context, with_theme, static, \
    get_static_directories, serve_static, install_app
