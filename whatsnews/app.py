# /whatsnews/app.py

import logging
import re

from flask import Flask, g, redirect, request, url_for   # do I need 'session' here too?
from flask_session import Session
from jinjax import Catalog

from whatsnews.blues.auth.models import user_auth
from .models import db_init_app


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config_all.py')
    if app.config['DEBUG']:
        app.config.from_pyfile('config_dev.py')
    else:
        app.config.from_pyfile('config_prod.py')

    _config_logging()

    #
    # Database
    #

    db_init_app(app)

    #
    # Blueprints
    #

    from .blues.cli import bp as cli_bp
    app.register_blueprint(cli_bp)
    from .blues.public import bp as public_bp
    app.register_blueprint(public_bp)
    from .blues.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blues.admin import bp as admin_bp
    from .blues.site import bp as site_bp
    admin_bp.register_blueprint(site_bp)
    app.register_blueprint(admin_bp)

    #
    # Flask-Session
    #

    sess = Session()
    sess.init_app(app)

    #
    # Template Filters
    #

    @app.template_filter('strip_http')
    def strip_http(url):
        return re.sub(r'^https?://', '', url)
    
    app.jinja_env.globals['user_auth'] = user_auth

    #
    # JinjaX
    #

    catalog = Catalog(jinja_env=app.jinja_env, file_ext='.html')
    catalog.add_folder('whatsnews/jinjax')

    #
    # "Middleware"
    #

    @app.before_request
    def add_catalog_to_g():
        g.jinjax_catalog = catalog
    
    @app.before_request
    def check_for_admin():
        ''' "Guard" the entire admin area '''
        if request.full_path.startswith('/admin/') and not user_auth.is_logged_in():
            return redirect( url_for('auth.login', next=request.full_path) )

    return app


def _config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'    
    )
