# /jbrbabel/models/FeedItem.py

import peewee as pw
from . import BaseModel
from jbrbabel.lib.deepl import translate_strs


class FeedItem(BaseModel):
    
    id = pw.AutoField()
    title = pw.CharField()
    title_en = pw.CharField()
    description = pw.CharField()
    description_en = pw.CharField()
    pub_date = pw.DateTimeField()
    url = pw.CharField()
    feed_id = pw.IntegerField()

    class Meta:
        table_name = 'feed_items'


    @classmethod
    def add_translations(cls, dicts):
        strs = []
        for dict in dicts:
            strs.append(dict['title'])
            strs.append(dict['description'])
        
        strs_en = translate_strs(strs)

        i = 0
        for dict in dicts:
            dict['title_en'] = strs_en[i]
            dict['description_en'] = strs_en[i+1]
            i += 2
        
        return dicts


    def __repr__(self):
        return f'<FeedItem {self.id} | {self.title[:30]}>'