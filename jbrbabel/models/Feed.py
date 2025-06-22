# /jbrbabel/models/Feed.py

import re
import feedparser
import peewee as pw
from . import BaseModel


MAX_DESC_WORDS = 30


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
            # Hack: remove possible image tag(s) from description
            desc = re.sub(r'<img .*?>', '', entry.description)

            # Limit length of description
            words = desc.split()
            if len(words) > MAX_DESC_WORDS:
                desc = ' '.join(words[:MAX_DESC_WORDS]) + '...'

            foo = {
                'title': entry.title,
                'description': desc,
                'url': entry.link,
                'pub_date': entry.published,
                'feed': self
            }
            items.append(foo)

        return items


    def __repr__(self):
        return f'<Feed {self.id} | {self.title}>'