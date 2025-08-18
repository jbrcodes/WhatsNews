# /whatsnews/blues/cli.py

import click
import json
import logging

from flask import Blueprint, current_app
from whatsnews.lib.deepl import deepl_init
from whatsnews.models import redo_tables, do_seed
from whatsnews.models.Site import Site
from whatsnews.models.FeedItem import FeedItem


bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('foo')
def foo():
    print('This is a (foo) test!')


@bp.cli.command('db-init')
def db_init():
    redo_tables()


@bp.cli.command('db-seed')
@click.argument('filename')
def db_seed(filename):
    try:
        with open(filename, 'r') as f:
            sites_data = json.load(f)
        do_seed(sites_data)
    except Exception as err:
        print(err)


@bp.cli.command('fetch')
def fetch():
    deepl_init( current_app.config['DEEPL_API_KEY'] )

    logging.info('BEGIN whatsnews fetch')

    for site in Site.select().where(Site.active):
        name = site.name_en if site.name_en != '' else site.name
        logging.info( f'{name}...' )

        # Save prior item IDs for this site
        prior_items = FeedItem.select().where((FeedItem.site == site))
        prior_item_ids = [i.id for i in prior_items]

        # Try to do "dangerous" stuff: fetch, translate
        try:
            dicts = site.fetch_rss()[:3]  # (not yet saved in DB)
            dicts1 = FeedItem.add_translations(dicts)
            FeedItem.insert_many(dicts1).execute()  # save in DB

            # If we get this far, everything worked; delete prior items
            if len(prior_item_ids) > 0:
                FeedItem.delete().where(FeedItem.id.in_(prior_item_ids)).execute()
        except Exception as err:
            logging.error( f"Error with site '{name}': {err}" )

    logging.info('END whatsnews fetch')