# /jbrbabel/models/seed.py

from . import db
from .Site import Site
from .FeedItem import FeedItem


def redo_tables():
    classes = [Site, FeedItem]
    db.drop_tables(classes)
    db.create_tables(classes)


site_data = [
    {
        'name':     'elDiario.es',
        'url':      'https://eldiario.es',
        'feed_url': 'https://www.eldiario.es/rss/',
        'country':  'Spain'
    },{
        'name':     'Korean News',
        'url':      'https://www.yna.co.kr',
        'feed_url': 'https://www.yna.co.kr/rss/news.xml',
        'country':  'Korea'
    },{
        'name':     'Al Jazeera',
        'url':      'https://www.aljazeera.net',
        'feed_url': 'https://www.aljazeera.net/aljazeerarss/',
        'country':  'Qatar'
    },{
        'name':     'News Bulgaria',
        'url':      'https://www.novinite.bg',
        'feed_url': 'https://www.novinite.bg/rss',
        'country':  'Bulgaria'
    },{
        'name':     'Haaretz',
        'url':      'https://www.haaretz.co.il',
        'feed_url': 'https://www.haaretz.co.il/srv/htz---all-articles',
        'country':  'Israel'
    }
]

def do_seed():
    Site.insert_many(site_data).execute()