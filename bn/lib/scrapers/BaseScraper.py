# /bn/lib/BaseScraper.py

import logging
import random
import traceback
from playwright.sync_api import sync_playwright


class BaseScraper:
    
    MAX_TIMEOUT_SECS = 10


    def __init__(self): 
        self.playwright = None
        self.browser = None
        self.page = None


    def init(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        ua = "Playwr1ght 1.30: What's New(s)? (demo) | whatsnews.jbrcodes.com | info@jbrcodes.com"
        self.browser = self.browser.new_context(user_agent=ua)
        self.page = self.browser.new_page()
    

    def scrape(self, fetch_url):
        posts = None
        try:
            posts = self.do_scrape(fetch_url)
        except Exception as err:
            logging.error('Exception: %s', err)
            logging.error('Traceback: %s', traceback.format_exc())
        return posts
    

    def wait_random_timeout(self):
        wait_ms = random.randint(3, BaseScraper.MAX_TIMEOUT_SECS) * 1000
        logging.info( f'wait {wait_ms}ms...' )
        self.page.wait_for_timeout(wait_ms)


    def close(self):
        self.browser.close()
        self.playwright.stop()
