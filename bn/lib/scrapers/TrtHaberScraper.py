# /bn/lib/TrtHaberScraper.py

import logging
import re
from bn.lib.scrapers.BaseScraper import BaseScraper


class TrtHaberScraper(BaseScraper):

    def do_scrape(self, scrape_url):
        logging.info('scrape home...')
        self.page.goto(scrape_url)
        dicts = []

        # Home page: Get titles and URLs

        # First article (hero)...
        hero = self.page.query_selector('div.special-hero-related-card-new')
        link = hero.query_selector('div.text-frame div.title a.site-url')
        dict = {
            'title_src': link.text_content().strip(),
            'url': link.get_attribute('href')
        }
        dicts.append(dict)

        # Second article (from news container)...
        title = self.page.query_selector('.news-container .text-frame .title')
        dict = {
            'title_src': title.query_selector('a').text_content().strip(),
            'url': title.query_selector('a').get_attribute('href')
        }
        dicts.append(dict)

        # Third article... ("Çok Okunanlar" / "Most Read")
        most = self.page.query_selector('.headline-widget-wrapper .top .text-frame')
        dict = {
            'title_src': most.query_selector('.title a').text_content().strip(),
            'url': most.query_selector('.title a').get_attribute('href')
        }
        dicts.append(dict)

        # Now let's visit each detail page for the summary/text and date
        for dict in dicts:
            self.wait_random_timeout()
            logging.info('scrape detail...')
            logging.info('  ' + dict['url'])
            self.page.goto(dict['url'])

            dict['text_src'] = self.page.query_selector('h2.news-spot').text_content().strip()

            datetime = self.page.query_selector('.news-info-bar time').get_attribute('datetime')
            dict['pub_date'] = re.sub(r' .*', '', datetime)

        return dicts
