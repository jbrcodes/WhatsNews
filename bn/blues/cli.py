# /bn/blues/cli.py

import click
import json
import logging

from flask import Blueprint, current_app
from bn.models import redo_tables, do_seed
from bn.models.Site import Site


bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('foo', help='A little test...')
def foo():
    print('This is a (foo) test!')


@bp.cli.command('add-admin', help="Create user 'admin'")
@click.argument('password')
def add_admin(password):
    from bn.models.User import User

    try:
        user = User.create(username='admin', password=password, is_admin=True)
    except Exception as err:
        print('Error:', err)


@bp.cli.command('db-init', help='Drop/create tables')
def db_init():
    redo_tables()


@bp.cli.command('db-seed', help='Seed sites table from JSON file')
@click.argument('filename')
def db_seed(filename):
    try:
        with open(filename, 'r') as f:
            sites_data = json.load(f)
        do_seed(sites_data)
    except Exception as err:
        print(err)


@bp.cli.command('fetch', help='Fetch/translate/save RSS items for active sites')
def fetch():
    from bn.lib.DeepLTranslator import DeepLTranslator
    
    logging.info('BEGIN babelnews fetch')

    DeepLTranslator.init( current_app.config['DEEPL_API_KEY'] )
    for site in Site.select().where(Site.is_active):
        name = site.name_en if site.name_en != '' else site.name
        logging.info( f'==> {name}...' )
        site.fetch_and_translate()

    logging.info('END babelnews fetch')