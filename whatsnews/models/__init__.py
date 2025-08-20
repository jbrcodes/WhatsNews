# /whatsnews/models/__init__.py

import peewee as pw
from playhouse.signals import Model as SigModel  # required for signal support


db = pw.SqliteDatabase(None)


class BaseModel(SigModel):
    class Meta:
        database = db


def db_init_app(app):
    db.init( app.config['SQLITE_DB_PATH'] )
    db.pragma('foreign_keys', 1, permanent=True)


def redo_tables():
    from .FeedItem import FeedItem
    from .Site import Site
    from .User import User

    classes = [Site, FeedItem, User]
    db.drop_tables(classes)
    db.create_tables(classes)


def do_seed(sites_data):
    from .Site import Site
    
    Site.insert_many(sites_data).execute()