# /whatsnews/blues/cli.py

import logging

from flask import Blueprint, current_app
from whatsnews.lib.deepl import deepl_init
from whatsnews.models.seed import redo_tables, do_seed
from whatsnews.models.Site import Site
from whatsnews.models.FeedItem import FeedItem


bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command('foo')
def foo():
    print('This is a (foo) test!')


@bp.cli.command('db-init')
def db_init():
    redo_tables()
    do_seed()


@bp.cli.command('fetch')
def fetch():
    deepl_init( current_app.config['DEEPL_API_KEY'] )

    logging.info('BEGIN whatsnews fetch')

    for site in Site.select()[:2]:
        name = site.name_en if site.name_en != '' else site.name
        logging.info( f'{name}...' )

        # Save existing item IDs for this site
        old_items = FeedItem.select().where((FeedItem.site == site))
        old_item_ids = [i.id for i in old_items]

        # Try to do "dangerous" stuff: fetch, translate
        try:
            dicts = site.fetch_rss()[:3]  # (not yet saved in DB)
            dicts1 = FeedItem.add_translations(dicts)
            FeedItem.insert_many(dicts1).execute()  # save in DB

            # If we get this far, everything worked; delete old items
            if len(old_item_ids) > 0:
                FeedItem.delete().where(FeedItem.id.in_(old_item_ids)).execute()
        except Exception as err:
            logging.error( f"Error with site '{name}': {err}" )

    logging.info('END whatsnews fetch')