import os
from fastapi import FastAPI, Request
import justengel_theme

MY_DIR = os.path.dirname(__file__)

app = FastAPI()
templates = justengel_theme.ThemeTemplates(os.path.join(MY_DIR, 'templates'), theme='left_nav_theme')
templates.install_theme('left_nav_theme')
templates.install_app(app, site_name='Demo')


@app.get('/')
def index(request: Request):
    ctx = {'request': request, 'base_url': request.base_url,
           'title': 'index'
           }
    return templates.TemplateResponse('demo/index.html', ctx)


@app.get('/page1')
def page1(request: Request):
    ctx = {'request': request, 'base_url': request.base_url,
           'title': 'Page 1'
           }
    return templates.TemplateResponse('demo/page1.html', ctx)


@app.get('/page2')
def page2(request: Request):
    ctx = {'request': request, 'base_url': request.base_url,
           'title': 'Page 2',
           }
    return templates.TemplateResponse('demo/page2.html', ctx)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
