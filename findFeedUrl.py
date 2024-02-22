# search for rss feed by website url

from bs4 import BeautifulSoup as bs4
import requests
import urllib.parse
import feedparser

def find_url(site):
    raw = requests.get(site).text
    result = []
    possible_feeds = []
    html = bs4(raw, features="lxml")
    feed_urls = html.findAll('link', rel='alternate') # ?-> rel='alternate'
    if len(feed_urls) > 1:
        for f in feed_urls:
            t = f.get('type', None) # ?
            if t:
                if 'rss' in t or 'xml' in t:
                    href = f.get('href', None)
                    if href:
                        possible_feeds.append(href)
    parsed_url = urllib.parse.urlparse(site) # why needed second check?
    base = parsed_url.scheme+'://'+parsed_url.hostname
    atags = html.findAll('a')
    for a in atags:
        href = a.get('href', None)
        if href:
            if "xml" in href or "rss" in href or "feed" in href:
                if 'http://' in href or 'https://' in href:
                    possible_feeds.append(href)
                else:
                    possible_feeds.append(base+href)
    for url in list(set(possible_feeds)):
        f = feedparser.parse(url)
        if len(f.entries) > 0:
            if url not in result:
                result.append(url)
    # return(result)
    if len(result) == 0:
        possible_feeds = []
        for p in common_rss_paths:
            possible_feeds.append(site+p)
        for url in list(set(possible_feeds)):
            f = feedparser.parse(url)
            if len(f.entries) > 0:
                r = requests.get(url) 
                result.append(r.url)
                break
    # else:
    #     # print(result)

    if len(result) > 1:
        for el in result:
            if 'comment' not in el:
                result = []
                result.append(el)
    if len(result) == 0:
        print('Rss feed not found')
        return 'Feed Not Found'
    else:
        r = requests.get(result[0]) 
        result = r.url
        return(result)

common_rss_paths = [
    "/feed",
    "/feeds",
    "/rss",
    "/feed/rss",
    "/feed/rss2",
    "/feed/rdf",
    "/feed/atom",
    "/index.rss",
    "/index.rdf",
    "/index.xml",
    "/rss.xml",
    "/atom.xml",
    "/?feed=rss",
    "/?feed=rss2",
    "/?feed=atom",
]
