# /jbrbabel/models/Site.py

import re
import feedparser
import peewee as pw
from . import BaseModel


MAX_DESC_WORDS = 40


class Site(BaseModel):
    
    id = pw.AutoField()
    name = pw.CharField()
    name_en = pw.CharField(default='')
    name_sort = pw.CharField()
    url = pw.CharField()
    feed_url = pw.CharField()
    country = pw.CharField()
    active = pw.BooleanField(default=True)
    last_fetched = pw.DateTimeField(null=True)

    class Meta:
        table_name = 'sites'


    def fetch_rss(self):
        feed_obj = feedparser.parse(self.feed_url)
        items = []

        for entry in feed_obj.entries:
            # Do some additional sanitizing that feedparser doesn't do
            summ = re.sub(r'<img .*?>', '', entry.summary)
            summ = re.sub(r'</?(div|p).*?>', '', summ)

            # Limit length of summary
            words = summ.split()
            if len(words) > MAX_DESC_WORDS:
                summ = ' '.join(words[:MAX_DESC_WORDS]) + '...'

            foo = {
                'title': entry.title,
                'summary': summ,
                'url': entry.link,
                'pub_date': entry.published,
                'feed': self
            }
            items.append(foo)

        return items


    def __repr__(self):
        return f'<Site {self.id} | {self.title}>'