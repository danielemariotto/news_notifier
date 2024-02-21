# simple Desktop Notifier application using Python. A desktop notifier is a simple application which produces a notification message in form of a pop-up message on desktop.

# Features:
# search for rss feed by giving topic or website url
# get list of site base on topic
# top news headlines
# crypto news
# google alert news
# rss feed from sites

import time
import find_feed_url as find_feed_url
from get_rss_data import get_news
from notifier import send_notification
website = input('Insert a website you want news via notification: ')

if 'http://' in website:
    website = website.replace('http://', 'https://')

if 'https://' not in website:
    website = 'https://' + website

feed_url = find_feed_url.find_url(website)
if feed_url is not None:
    all_news = get_news(feed_url)
    for newsitem in all_news:
        title = newsitem['title'][:61]+'...'
        message = newsitem['description'][:253]+'...'
        send_notification(title, message)
        time.sleep(5)  # wait a bit before clearing notification