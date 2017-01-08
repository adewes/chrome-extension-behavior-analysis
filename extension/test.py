import time
import logging
import sys
import json

from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from proxy.proxy import HTTPProcess

websites = [
    'https://en.wikipedia.org/wiki/List_of_wikis',
    'https://www.uni-tuebingen.de',
    'https://www.uni-sb.de',
    'https://www.eff.org',
    'https://www.mozilla.org',
    'https://www.arbeitsagentur.de',
    'https://www.tagesschau.de',
    'https://www.ptb.de',
    'https://www.inria.fr',
    'https://www.google.de/?gfe_rd=cr&ei=dr9fWKHfJc7i8AeutpSwAg#q=test',
    'https://www.facebook.com/Speicherstadt-Kaffeer%C3%B6sterei-118962444840064/',
    'https://www.youtube.com/watch?v=WhU1ZXLsKCg',
    'https://www.google.de/maps/@49.3428062,6.78282,13z?hl=en',
    'https://twitter.com/josephfcox'
]

def log_sites(driver, proxy, websites):

    results = defaultdict(set)

    for website in websites:
        time.sleep(2)
        #we make sure the log queue is empty...
        while not proxy.log_queue.empty():
            proxy.log_queue.get()

        print("\nOpening {}".format(website))
        try:
            driver.get(website)
        except KeyboardInterrupt:
            raise
        except:
            pass

        while not proxy.log_queue.empty():
            result = proxy.log_queue.get()
            print("Adding server {} to log".format(result[1]))
            results[website].add(result[1])

        print("\n")

    return results


def main():

    if len(sys.argv) < 3:
        sys.stderr.write("Usage: {} [extension filename] [report filename]\n".format(sys.argv[0]))
        exit(-1)

    extension_filename = sys.argv[1]
    report_filename = sys.argv[2]

    proxy = HTTPProcess("localhost",8899)
    try:
        proxy.start()
        time.sleep(3)
        test_extension(extension_filename, report_filename)
    finally:
        proxy.terminate()
        proxy.join()

def test_extension(proxy, extension_filename, report_filename, baseline=False):

    driver_executable = "/usr/lib/chromium-browser/chromedriver"

    chrome_options_with_extension = webdriver.ChromeOptions()
    chrome_options_with_extension.add_argument('--proxy-server=http://localhost:8899')
    chrome_options_with_extension.add_extension(extension_filename)

    if baseline:
        chrome_options_without_extension = webdriver.ChromeOptions()
        chrome_options_without_extension.add_argument('--proxy-server=http://localhost:8899')
   
    driver_with_extension = webdriver.Chrome(driver_executable, chrome_options=chrome_options_with_extension) 
    #we wait a bit...
    time.sleep(3)
    try:
        if baseline:
            driver_without_extension = webdriver.Chrome(driver_executable, chrome_options=chrome_options_without_extension)
            driver_without_extension.set_page_load_timeout(10)
        try:
            driver_with_extension.set_page_load_timeout(10)
            result_with_extension = log_sites(driver_with_extension, proxy, websites)
            
            if baseline:
                result_without_extension = log_sites(driver_without_extension, proxy, websites)
            else:
                result_without_extension = {}
            for d in (result_with_extension, result_without_extension):
                for url in d:
                    d[url] = list(d[url])

            with open(report_filename, 'w') as output_file:
                json.dump({'with_extension': result_with_extension,
                           'without_extension' : result_without_extension,
                           'filename' : extension_filename}, output_file, indent=2)
        finally:
             if baseline:
                 driver_without_extension.quit()
    finally:
        driver_with_extension.quit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s\t%(asctime)s\t%(message)s',
                        datefmt='%s')
    main()
