import time
import findFeedUrl as findFeedUrl
from getRssData import getNews
from notifier import sendNotification
status = 1
feedError = ''
guid_list = []
gFeed_url = ''


def stopSendingNews():
    global status
    status = 0

def startingSendingNews():
    global status
    status = 1

def setListAlreadyPresent(all_news):
    for newsitem in all_news:
        guid_list.append(newsitem['guid'])

def sendNewNews(all_news):
    for newsitem in all_news[0:20]:
        if newsitem['guid'] not in guid_list:
            guid_list.append(newsitem['guid'])
            guid_list.pop(0)
            title = newsitem['title'][:61]+'...'
            message = newsitem['description'][:253]+'...'
            sendNotification(title, message)

async def getFeedUrl(website):
    if 'http://' in website:
        website = website.replace('http://', 'https://')

    if 'https://' not in website:
        website = 'https://' + website

    feed_url = await findFeedUrl.findUrl(website)
    if feed_url != 'Feed Not Found':
        global gFeed_url
        gFeed_url = feed_url
        return feed_url
    else:
        global feedError
        feedError = 'Feed Not Found'
        return feedError

async def startCheckingForNews(website, minuteCheckInterval):
    feed_url_response = await getFeedUrl(website)
    if feed_url_response != 'Feed Not Found':
        global status
        status = 1

        #get news first time. dont't send notifications
        all_news = await getNews(feed_url_response)
        setListAlreadyPresent(all_news)
        
        #check for news every x minutes
        while status == 1:
            all_news = await getNews(feed_url_response)
            sendNewNews(all_news)
            time.sleep(2 * minuteCheckInterval) # check every x minutes
    else:
        return feed_url_response # error

async def getNewsAndSend(website):
    if 'http://' in website:
        website = website.replace('http://', 'https://')

    if 'https://' not in website:
        website = 'https://' + website

    feed_url = findFeedUrl.findUrl(website)
    if feed_url != 'Feed Not Found':
        global gFeed_url
        gFeed_url = feed_url
        all_news = await getNews(feed_url)
        for newsitem in all_news:
            global status
            if status == 0:
                break 
            title = newsitem['title'][:61]+'...'
            message = newsitem['description'][:253]+'...'
            sendNotification(title, message)
            time.sleep(5)  # wait a bit before clearing notification
    else:
        global feedError
        feedError = 'Feed Not Found'
        return feedError
if __name__ == "__main__":
    website = input('Insert a website you want news via notification: ')
    getNewsAndSend(website)