# /whatsnews/models/__init__.py

import peewee as pw

db = pw.SqliteDatabase(None)


class BaseModel(pw.Model):
    class Meta:
        database = db


def db_init_app(app):
    db.init( app.config['SQLITE_DB_PATH'] )
    db.pragma('foreign_keys', 1, permanent=True)

    # Let Peewee autoconnect take care of this (for now at least)

    # @app.before_request
    # def _before_request():
    #     db.connect()

    # @app.after_request
    # def _after_request(response):
    #     db.close()
    #     return response
