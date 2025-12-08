# /bn/models/Site.py

import logging
import re
import traceback
import feedparser
import peewee as pw
from . import BaseModel
from bn.lib.DeepLTranslator import DeepLTranslator


MAX_TEXT_WORDS = 40


class Site(BaseModel):
    
    id = pw.AutoField()
    name = pw.CharField()
    name_en = pw.CharField(default='')
    name_sort = pw.CharField()
    country = pw.CharField()
    url = pw.CharField()
    fetch_type = pw.CharField(max_length=10)  # rss | scraper
    fetch_url = pw.CharField()
    fetch_scraper = pw.CharField(default='')
    lang_src = pw.CharField(max_length=2)
    lang_dest = pw.CharField(max_length=2)
    is_active = pw.BooleanField(default=True)
    last_fetched = pw.DateTimeField(null=True)

    class Meta:
        table_name = 'sites'


    def fetch_and_translate(self) -> None:
        from bn.models.Post import Post

        # Get prior post IDs for this site
        prior_posts = Post.select().where(Post.site == self)
        prior_post_ids = [p.id for p in prior_posts]
        
        # Try to do "dangerous" stuff: fetch, translate
        try:
            new_posts = self._fetch_rss()[:3]  # (not yet saved in DB)
            new_posts1 = self._add_translations(new_posts)
            Post.bulk_create(new_posts1)

            # If we get this far, everything worked; delete prior posts
            if len(prior_post_ids) > 0:
                Post.delete().where(Post.id.in_(prior_post_ids)).execute()
        except Exception as err:
            logging.error( f"Error with site '{self.name}': {err}" )
            logging.error('Traceback: %s', traceback.format_exc())


    def _fetch_rss(self):
        from bn.models.Post import Post

        feed_obj = feedparser.parse(self.fetch_url)
        posts = []

        for entry in feed_obj.entries:
            # Do some additional sanitizing that feedparser doesn't do
            text = re.sub(r'<img .*?>', '', entry.summary)
            text = re.sub(r'</?(div|p).*?>', '', text)
            text = re.sub(r'<br[^/>]*/?>', '', text)

            # Limit length of summary
            words = text.split()
            if len(words) > MAX_TEXT_WORDS:
                text = ' '.join(words[:MAX_TEXT_WORDS]) + '...'

            # Create Post and append to list
            data = {
                'title_src': entry.title,
                'text_src': text,
                'url': entry.link,
                'pub_date': entry.published,  # FIX ME: convert to yyyy-mm-dd
                'site': self
            }
            posts.append( Post(**data) )

        return posts
    

    def _fetch_scraper(self):
        pass
    

    def _add_translations(self, posts):
        strs_src = []
        for post in posts:
            strs_src.append(post.title_src)
            strs_src.append(post.text_src)
        
        trans_obj = DeepLTranslator()
        strs_dest = trans_obj.translate_strings(strs_src, self.lang_src, self.lang_dest)

        i = 0
        for post in posts:
            post.title_dest = strs_dest[i]
            post.text_dest = strs_dest[i+1]
            i += 2
        
        return posts


    def __repr__(self):
        return f'<Site {self.id} | {self.name_en or self.name}>'