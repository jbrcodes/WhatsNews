# /bn/lib/scrapers/IranIntlScraper.py

import logging
import re
from bn.lib.scrapers.BaseScraper import BaseScraper


class IranIntlScraper(BaseScraper):

    def do_scrape(self, scrape_url):

        #
        # Index page
        #

        # Get everything we can from the home/index page
        dicts = []
        logging.info('scrape home...')
        self.page.goto(scrape_url)
        sections = self.page.query_selector_all('main.page__main > section.cluster')
        count = 0

        for sec in sections:
            if len(dicts) >= 3:
                break
            
            count += 1

            # Multiple things in a row; skip
            if sec.evaluate('el => el.classList.contains("cluster--hotTake")'):
                logging.info( f'skip hot take {count}' )
                continue

            # Video carousel; skip
            if sec.query_selector('div.swiper') is not None:
                logging.info( f'skip carousel {count}' )
                continue

            # Header, three cols, main post in right 1/2 (CSS class "undefined")
            if sec.evaluate('el => el.classList.contains("undefined")'):
                art = sec.query_selector('article')  # get first (of possibly multiple) article(s)
                dict = {
                    'title_src': art.query_selector('header h3').text_content().strip(),
                    'url': art.query_selector('header a').get_attribute('href')
                }
                dicts.append(dict)
                logging.info( f'"undefined" {count} {dict["url"]}' )
                continue

            # Catch-all? (Everything else?)
            art = sec.query_selector('article')  # get first (of possibly multiple) article(s)
            dict = {
                'title_src': art.query_selector('h4.cluster-item__headline').text_content().strip(),
                'url': art.query_selector('a.cluster-item__link').get_attribute('href')
            }
            dicts.append(dict)
            logging.info( f'catch-all? {count} {dict["url"]}')
            # END OF LOOP

        #
        # Detail pages
        #

        # Now let's visit each detail page for the summary and date
        for dict in dicts:
            self.wait_random_timeout()
            logging.info('scrape detail...')
            self.page.goto(dict['url'])

            # Get lead/summary
            dict['text_src'] = self.page.query_selector('article main p').text_content().strip()

            # Get date
            datetime = self.page.query_selector('header time').get_attribute('datetime')
            dict['pub_date'] = re.search(r'(\d{4}-\d\d-\d\d)', datetime).group(1)

        return dicts
