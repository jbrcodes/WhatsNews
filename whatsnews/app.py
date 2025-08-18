# /whatsnews/app.py

import logging
import re

from flask import Flask, g
from jinjax import Catalog
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

    from .blues.admin import bp as admin_bp
    from .blues.site import bp as site_bp
    admin_bp.register_blueprint(site_bp)
    app.register_blueprint(admin_bp)

    #
    # Template Filters
    #

    @app.template_filter('strip_http')
    def strip_http(url):
        return re.sub(r'^https?://', '', url)
    
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

    return app


def _config_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'    
    )
