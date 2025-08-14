# /whatsnews/models/__init__.py

import peewee as pw

db = pw.SqliteDatabase(None)


class BaseModel(pw.Model):
    class Meta:
        database = db


def db_init_app(app):
    db.init( app.config['SQLITE_DB_PATH'] )
    db.pragma('foreign_keys', 1, permanent=True)


def redo_tables():
    from .FeedItem import FeedItem
    from .Site import Site

    classes = [Site, FeedItem]
    db.drop_tables(classes)
    db.create_tables(classes)


def do_seed(sites_data):
    from .Site import Site
    
    Site.insert_many(sites_data).execute()