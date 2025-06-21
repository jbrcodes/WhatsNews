# /jbrbabel/blues/cli.py

from flask import Blueprint, current_app
from jbrbabel.lib.deepl import deepl_init
from jbrbabel.models.seed import redo_tables, do_seed
from jbrbabel.models.Feed import Feed
from jbrbabel.models.FeedItem import FeedItem


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

    for feed in Feed.select():  # DEBUG
        print( f'{feed.title} ({feed.source_lang})' )
        dicts = feed.fetch_rss()[:3]  # NOT YET SAVED
        dicts1 = FeedItem.add_translations(dicts)  # DEBUG
        FeedItem.insert_many(dicts1).execute()