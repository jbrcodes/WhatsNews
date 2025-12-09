# /bn/lib/AajTakScraper.py

import re
from bn.lib.scrapers.BaseScraper import BaseScraper


HindiMonths = {
    'जनवरी': '01',
    'फरवरी': '02',
    'मार्च': '03',
    'अप्रैल': '04',
    'मई': '05',
    'जून': '06',
    'जुलाई': '07',
    'अगस्त': '08',
    'सितंबर': '09',
    'अक्टूबर': '10',
    'नवंबर': '11',
    'दिसंबर': '12'
}


class AajTakScraper(BaseScraper):

    def do_scrape(self, scrape_url):
        print('scrape home...')
        self.page.goto(scrape_url)
        dicts = []

        # First article...
        left_col = self.page.query_selector('.left-story')
        dict = {
            'title_src': left_col.query_selector('.des h2').text_content().strip(),
            'text_src': left_col.query_selector('.des p').text_content().strip(),
            'url': left_col.query_selector('a').get_attribute('href')
        }
        dicts.append(dict)

        # Second article...
        hss = left_col.query_selector('.home-single-story')
        dict = {
            'title_src': hss.query_selector('h3').text_content().strip(),
            'text_src': hss.query_selector('.single_str .title h3').text_content().strip(),
            'url': hss.query_selector('a').get_attribute('href')
        }
        dicts.append(dict)

        # Third article... "Big News", no text (yet)
        art = self.page.query_selector('#badi_khabar_2 .badikhaber-outer li')
        dict = {
            'title_src': art.query_selector('a').text_content().strip(),
            'text_src': '',
            'url': art.query_selector('a').get_attribute('href')
        }
        dicts.append(dict)

        # Now let's visit each detail page for the date
        for dict in dicts:
            self.wait_random_timeout()
            print('scrape detail...')
            self.page.goto(dict['url'])

            # Get text for third article
            if dict['text_src'] == '':
                dict['text_src'] = self.page.query_selector('.content-area h2').text_content().strip()

            # 2nd <li> contains full date (with month in Hindi)
            date_hindi = self.page.query_selector('.content-area .brand-detial-main li:nth-child(2)') \
                .text_content().strip()
            m = re.search(r'(\d\d) (\S+) (\d{4})', date_hindi)
            dict['pub_date'] = f'{m.group(3)}-{HindiMonths[m.group(2)]}-{m.group(1)}'

        return dicts
