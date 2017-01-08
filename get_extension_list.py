import time
import re
import pprint
import json
import select
import sys

from collections import defaultdict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from proxy.proxy import HTTPProcess


webstore_url = 'https://chrome.google.com/webstore/category/extensions'
rating_regex = re.compile(r'Average\s+rating\s+([^\s]+).*?(\d+)\s+users',re.I)
link_regex = re.compile(r'https://chrome\.google\.com/webstore/detail/([^\/]+)/([\w\d]+)',re.I)

def extract_extensions(driver, extensions):
    links = list(driver.find_elements_by_class_name('a-u'))

    for link in links:
        link_match = link_regex.match(link.get_attribute('href'))
        if link_match:
            extension_name = link_match.group(1)
            extension_id = link_match.group(2)
            try:
                rating = link.find_element_by_class_name('q-N-nd')
                rating_match = rating_regex.match(rating.get_attribute('aria-label'))
            except:
                rating_match = None
            if rating_match:
                rating_score = float(rating_match.group(1))
                rating_users = int(rating_match.group(2))
            else:
                rating_score = 0.0
                rating_users = 0
            extensions[extension_name] = {
                'id' : extension_id,
                'rating' : {
                    'score' : rating_score,
                    'users' : rating_users
                }
            }
            print(extension_name, extension_id, rating_score, rating_users)



def main(args):

    if len(args) < 2:
        print("Usage: {} [output filename]".format(args[0]))
        return -1
    output_filename = args[1]

    chrome = webdriver.Chrome()
    chrome.get(webstore_url)

    print("Press any key to abort scrolling and export extensions...")
    while True:
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        if select.select([sys.stdin,],[],[],0.0)[0]:
            break

    extensions = {}
    extract_extensions(chrome, extensions)

    chrome.close()

    print("Extracted {} extensions".format(len(extensions)))

    print("Storing in {}".format(output_filename))
    with open(output_filename,'w') as output_file:
        output_file.write(json.dumps(extensions, indent=2))

if __name__ == '__main__':
    main(sys.argv)