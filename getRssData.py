import requests
import xml.etree.ElementTree as ET


async def loadRSS(url):
    response = await requests.get(url)
    return response.content

def parseXML(rss):
    root = ET.fromstring(rss)
    newsItems = []

    for item in root.findall('.channel/item'):
        news = {} 
        for child in item:
                if child.text is not None:
                    content = str(child.text)
                    if content.startswith("b'"):
                         content = content[1:]
                         content = content.strip("'")
                    news[child.tag] = content

        newsItems.append(news)
    return newsItems

async def getNews(url):
    rss = await loadRSS(url)
    news = parseXML(rss)
    return news