import bs4 #pip install BeautifulSoup4
from bs4 import BeautifulSoup

# Python 3
# import urllib
# from urllib.parse import urlsplit

# Python 2
# https://docs.python.org/2/library/urlparse.html
import urlparse

import collections
from collections import deque

# https://requests.readthedocs.io/en/master/
import requests
import requests.exceptions

url = "https://scrapethissite.com/"

# a queue of urls to be crawled
new_urls = deque()
new_urls.append(url)

# a set of urls that we have already processed 
processed_urls = set()

# a set of domains inside the target website
local_urls = set()

# a set of broken urls
broken_urls = set()

# urls that are outside of the local address
foreign_urls = set()

# process urls one by one until we exhaust the queue
while len(new_urls)>0:
    # move url from the queue to processed url set
    url = new_urls.popleft()
    processed_urls.add(url)
    # print the current url
    print("Processing %s" % url)

    try:
        response = requests.get(url)
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        # add broken urls to it's own set, then continue
        broken_urls.add(url)
        continue

    # extract base url to resolve relative links
    rl = urlparse.urlsplit(url)
    print(rl)
    base = rl.netloc # 'scrapethissite.com'
    strip_base = base.replace("www.", "")
    base_url = rl.geturl() # 'https://scrapethissite.com/'
    path = rl.path #extra stuff after the basic url

    soup = BeautifulSoup(response.text, "html.parser")
    for link in soup.find_all('a'):
        # extract link url from the anchor
        anchor = ''
        if "href" in link.attrs:
            anchor = link.attrs["href"]
        
        if anchor.startswith('/'):
            local_link = base_url + anchor
            local_urls.add(local_link)    
        elif strip_base in anchor:
            local_urls.add(anchor)
        elif not anchor.startswith('http'):
            local_link = path + anchor
            local_urls.add(local_link)
        else:
            foreign_urls.add(anchor)

    # makes sure that we only crawl the local urls
    # if we want to crawl all urls, then we append the link above to new_urls
    for u in local_urls: 
        if u not in new_urls and u not in processed_urls:
            new_urls.append(u)

print("processed_urls", processed_urls)
print("local_urls", local_urls)
print("broken_urls", broken_urls)