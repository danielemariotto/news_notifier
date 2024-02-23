import time
import findFeedUrl as findFeedUrl
from getRssData import get_news
from notifier import send_notification
status = 1
feedError = ''
def stopSendingNews():
    global status
    status = 0

def startingSendingNews():
    global status
    status = 1

def getNewsAndSend(website):
    if 'http://' in website:
        website = website.replace('http://', 'https://')

    if 'https://' not in website:
        website = 'https://' + website

    feed_url = findFeedUrl.find_url(website)
    if feed_url != 'Feed Not Found':
        all_news = get_news(feed_url)
        for newsitem in all_news:
            title = newsitem['title'][:61]+'...'
            message = newsitem['description'][:253]+'...'
            global status
            if status == 0:
                break 
            send_notification(title, message)
            time.sleep(5)  # wait a bit before clearing notification
    else:
        global feedError
        feedError = 'Feed Not Found'
        return feedError
if __name__ == "__main__":
    website = input('Insert a website you want news via notification: ')
    getNewsAndSend(website)