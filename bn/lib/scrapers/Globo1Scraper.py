# /bn/lib/Globo1Scraper.py

import logging
import re
from bn.lib.scrapers.BaseScraper import BaseScraper


class Globo1Scraper(BaseScraper):

    def do_scrape(self, scrape_url):
        logging.info('scrape home...')
        self.page.goto(scrape_url)
        dicts = []

        # hAck!!
        logging.info('wait 10 (!!) secs...')
        self.page.wait_for_timeout(10000)
        logging.info('GO!!')

        # Interesting: Titles on home page don't correspond to titles on detail pages.
        # We'll keep the latter titles cuz that's where our link will take the reader.

        # Three headlines...
        headlines = self.page.query_selector_all('.bstn-hls .bstn-hl-wrapper')[:3]
        for hl in headlines:
            dict = {
                'url': hl.query_selector('a.bstn-hl-link').get_attribute('href')
            }
            dicts.append(dict)

        # Now let's visit each detail page
        for dict in dicts:
            self.wait_random_timeout()
            logging.info('scrape detail...')
            self.page.goto(dict['url'])

            dict['title_src'] = self.page.query_selector('h1.content-head__title').text_content().strip()
            dict['text_src'] = self.page.query_selector('h2.content-head__subtitle').text_content().strip()

            datetime = self.page.query_selector('.content__signature time').get_attribute('datetime')
            dict['pub_date'] = re.sub(r'T.*', '', datetime)

        return dicts
