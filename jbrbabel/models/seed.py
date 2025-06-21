# /jbrbabel/models/seed.py

from . import db
from .Feed import Feed
from .FeedItem import FeedItem


def redo_tables():
    classes = [Feed, FeedItem]
    db.drop_tables(classes)
    db.create_tables(classes)


feed_data = [
    { 'title': 'Les Amis de Svieta', 'url': 'https://www.svieta.org/de/feed/', 'source_lang': 'DE' },
    { 'title': 'Al Jazeera', 'url': 'https://www.aljazeera.net/aljazeerarss/', 'source_lang': 'AR' },
    { 'title': 'News Bulgaria', 'url': 'https://www.novinite.bg/rss', 'source_lang': 'BG' },
    { 'title': 'Haaretz', 'url': 'https://www.haaretz.co.il/srv/htz---all-articles', 'source_lang': 'HE' }
]

def do_seed():
    Feed.insert_many(feed_data).execute()