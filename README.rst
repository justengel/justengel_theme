===============
justengel_theme
===============

Fastapi Jinja theming system.


Include Block Tag
=================

This template system heavily uses the include_block tag. This tag will include an html file as a block.
This tag can be overridden with an html file matching the name or by a block tag matching the base name.

Create a base for your theme

.. code-block:: html

    {# theme_templates/theme/base.html #}
    <html>
    <body>
    {% include_block theme/sidenav.html %}

    {% block contents %}
    <h1>Hello World!</h1>
    {% endblock %}
    </body>
    </html>

Normal navigation for your theme

.. code-block:: html

    {# theme_templates/theme/sidenav.html #}
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/page1">Page 1</a></li>
      <li><a href="/page2">Page 2</a></li>
    </ul>


**Override with block**

Override navigation by using a block. The block name will be the same as the base html filename.
Note: different templates directory

.. code-block:: html

    {# templates/main.html #}
    {% extends "theme/base.html" %}

    {% block sidenav %}
    <ul>
      <li>Hello</li>
    </ul>
    {% endblock sidenav %}


**Override with HTML file**

Alternatively you can override by using an html file. Note: different templates directory

.. code-block:: html

    {# templates/theme/sidenav.html #}
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/link">Link to my other site</a></li>
    </ul>

Fastapi using the templates

.. code-block:: python

    from fastapi import FastAPI, Request
    from justengel_theme import ThemeTemplates

    MYD_DIR = os.path.dirname(__file__)

    # Search for project files first
    project_dir = os.path.join(MY_DIR, 'templates')
    templates = ThemeTemplates(project_dir)

    # Search for theme files if project files are not found
    theme_dir = os.path.join(MY_DIR, 'theme_templates')
    templates.add_directory(theme_dir)

    app = FastAPI()

    @app.get('/')
    def index(request: Request):
        return material.TemplateResponse('main.html', {'request': request})
