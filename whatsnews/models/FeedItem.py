# /whatsnews/models/FeedItem.py

import peewee as pw
from . import BaseModel
from .Site import Site
from whatsnews.lib.deepl import translate_strs


class FeedItem(BaseModel):
    
    id = pw.AutoField()
    title = pw.CharField()
    title_en = pw.CharField()
    summary = pw.CharField()
    summary_en = pw.CharField()
    pub_date = pw.DateTimeField()
    url = pw.CharField()
    site = pw.ForeignKeyField(Site, backref='feed_items', on_delete='CASCADE')

    class Meta:
        table_name = 'feed_items'


    @classmethod
    def add_translations(cls, dicts):
        strs = []
        for dict in dicts:
            strs.append(dict['title'])
            strs.append(dict['summary'])
        
        strs_en = translate_strs(strs)

        i = 0
        for dict in dicts:
            dict['title_en'] = strs_en[i]
            dict['summary_en'] = strs_en[i+1]
            i += 2
        
        return dicts


    def __repr__(self):
        return f'<FeedItem {self.id} | {self.title[:30]}>'