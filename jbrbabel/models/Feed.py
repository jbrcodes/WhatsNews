# /jbrbabel/models/Feed.py

import feedparser
import peewee as pw
from . import BaseModel


MAX_DESC_WORDS = 10


class Feed(BaseModel):
    
    id = pw.AutoField()
    title = pw.CharField()
    url = pw.CharField()
    source_lang = pw.CharField()
    last_fetched = pw.DateTimeField(null=True)

    class Meta:
        table_name = 'feeds'


    def fetch_rss(self):
        feed_obj = feedparser.parse(self.url)
        items = []

        for entry in feed_obj.entries:
            words = entry.description.split()
            if len(words) > MAX_DESC_WORDS:
                desc = ' '.join(words[:MAX_DESC_WORDS]) + '...'
            else:
                desc = entry.description

            foo = {
                'title': entry.title,
                'description': desc,
                'url': entry.link,
                'pub_date': entry.published,
                'feed_id': self.id
            }
            items.append(foo)
        return items


    def __repr__(self):
        return f'<Feed {self.id} | {self.title}>'