"""
Download ads from  sauto.cz
Iteratively browse the advertisements and save the complete pages.

@author: jirka
"""

import argparse
import os
import sys
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

URL = 'http://www.sauto.cz/osobni/hledani#!category=1&condition=1&condition=2&condition=4&fuel=2&subCategory=6&manu' \
      'facturer=93&model=705&page=1'

FILE_PREFIX = 'octavia_2017-03'
OUTPUT_DIR = 'data_html_temp'


class DownloadAds:

    def __init__(self, args=None):

        parsed_args = self.parse_cmd_args()

        self._web_url = URL if parsed_args.url is None else parsed_args.url
        self._fileprefix = FILE_PREFIX if parsed_args.file_prefix is None else parsed_args.file_prefix
        self._outputdir = OUTPUT_DIR if parsed_args.output_dir is None else parsed_args.output_dir

        self._wait_page_load = .5  # gives implicit wait for loading page

        self._driver = webdriver.Chrome()

    def run(self):

        print("Processing pages: ")

        self._driver.get(self._web_url)
        self._driver.maximize_window()  # For maximizing window
        # self._driver.implicitly_wait(self._wait_page_load)
        time.sleep(self._wait_page_load)

        b_continue = True
        cnt = 0

        while b_continue:

            cnt += 1

            pg = self._driver.execute_script('return document.documentElement.innerHTML')
            self.save_html_page(pg, cnt)
            self._driver.delete_all_cookies()

            try:
                # wait until element nextPage is located
                element = WebDriverWait(self._driver, 20).until(
                    EC.presence_of_element_located((By.ID, "nextPage"))
                )
                element.click()

                # another wait. For some reason it was not working without this
                val = random.randint(10, 100)/float(10)
                print('Waiting time: %2.2f' % val)
                time.sleep(val)

            except Exception:
                print('Unexpected error: ', sys.exc_info())
                print('or reached the last page')
                b_continue = False

        self._driver.close()

    def save_html_page(self, page, cnt, trim=False):

        sname = '{:}_{:03}.html'.format(self._fileprefix, cnt)

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        sname = os.path.join(OUTPUT_DIR, sname)

        with open(sname, 'w') as fr:
            fr.write(page.encode('utf-8'))

        print('Saved: {0}'.format(sname))

    @staticmethod
    def parse_cmd_args():
        parser = argparse.ArgumentParser(description='DownloadAds -- download and save ads')
        parser.add_argument('-u', '--url', help='Url', required=False)
        parser.add_argument('-p', '--file-prefix', help='File prefix for saved files', required=False)
        parser.add_argument('-o', '--output-dir', help='Directory for saving', required=False)
        return parser.parse_args()

if __name__ == '__main__':

    # prepare
    try:
        os.system("Xvfb :42 -ac -screen 0 1000x1200x30 &")
        os.system("export DISPLAY=:42")
        os.system("java -jar selenium-server-standalone-3.3.0.jar &")
    except:
        print('Selenium error')

    main = DownloadAds(sys.argv)
    main.run()

    print('Done ')




