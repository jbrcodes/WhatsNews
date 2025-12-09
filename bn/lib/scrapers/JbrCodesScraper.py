# /bn/lib/JbrCodesScraper.py

import re
from bn.lib.scrapers.BaseScraper import BaseScraper


class JbrCodesScraper(BaseScraper):

    def do_scrape(self, scrape_url):
        # Get everything we can from the home/index page
        dicts = []
        print('scrape index...')
        self.page.goto(scrape_url)
        divs = self.page.query_selector_all('#blog-index > div')[:3]
        for div in divs:
            data = {
                'title_src': div.query_selector('h2 a').text_content().strip(),
                'text_src': div.query_selector('p').text_content().strip(),
                'url': scrape_url + div.query_selector('h2 a').get_attribute('href')
            }
            dicts.append(data)

        # Now let's visit each detail page for the date
        for dict in dicts:
            self.wait_random_timeout()
            print('scrape detail...')
            self.page.goto(dict['url'])
            date_plus = self.page.query_selector('.jbr-pub-date').text_content().strip()
            dict['pub_date'] = re.sub(r'Published: ', '', date_plus)

        return dicts
