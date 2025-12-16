# /bn/models/Site.py

import datetime
import logging
import re
import traceback
import feedparser
import peewee as pw
from . import BaseModel
from bn.lib.DeepLTranslator import DeepLTranslator  #, LangsRTL


MAX_TEXT_WORDS = 40


class Site(BaseModel):
    
    id = pw.AutoField()
    slug = pw.CharField()
    name = pw.CharField()
    name_en = pw.CharField(default='')
    name_sort = pw.CharField()
    country = pw.CharField()
    language = pw.CharField()
    url = pw.CharField()
    fetch_type = pw.CharField(max_length=10)  # rss | scraper
    fetch_url = pw.CharField()
    scraper_class_name = pw.CharField(default='')
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
            if self.fetch_type == 'rss':
                new_posts = self._fetch_rss()  # (not yet saved in DB)
            else:
                new_posts = self._fetch_scraper()
            new_posts1 = self._add_translations(new_posts[:3])
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

            # Limit length of text
            text = self._limit_word_count(text)

            # Massage pub_date
            m = re.search(r'(\d\d? \w{3} \d{4})', entry.published)  # 5 Oct 2020
            dt = datetime.datetime.strptime(m.group(1), '%d %b %Y')
            pub_date = dt.strftime('%Y-%m-%d')  # 2020-10-05

            # Create Post and append to list
            dict = {
                'title_src': entry.title,
                'text_src': text,
                'url': entry.link,
                'pub_date': pub_date,
                'site': self
            }
            posts.append( Post(**dict) )

        return posts
    

    def _fetch_scraper(self):
        import importlib
        from bn.models.Post import Post

        mod_name = f"bn.lib.scrapers.{self.scraper_class_name}"
        mod = importlib.import_module(mod_name)
        class_ = getattr(mod, self.scraper_class_name)

        scraper = class_()
        scraper.init()
        post_dicts = scraper.scrape(self.fetch_url)
        scraper.close()

        posts = []
        for dict in post_dicts:
            post = Post(**dict, site=self)
            post.text_src = self._limit_word_count(post.text_src)
            posts.append(post)

        return posts
    

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
    

    def _limit_word_count(self, text):
        words = re.split(r'\s+', text)
        if len(words) > MAX_TEXT_WORDS:
            return ' '.join(words[:MAX_TEXT_WORDS]) + '...'
        else:
            return ' '.join(words)


    def __repr__(self):
        return f'<Site {self.id} | {self.name_en or self.name}>'