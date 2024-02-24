import tkinter as tk
import sendNews
import threading
import time
import asyncio

newsThread = None

async def newsThreadF(website):
    try:
        # result = sendNews.getNewsAndSend(website)
        result = await sendNews.startCheckingForNews(website, 5)

        if result == 'Feed Not Found':
            updateErrorLabel('Feed Not Found')
        else:
            updateErrorLabel('')
    except Exception as e:
        updateErrorLabel('Error')
        print('Error')

async def getWebsite():
    global newsThread
    newsThread = None
    gWebsite = sitename.get()
    # task = asyncio.create_task(newsThreadF(gWebsite))
    # result = await task
    newsThread = threading.Thread(target=newsThreadF, args=(gWebsite,)) #FIXME
    sendNews.startingSendingNews()
    newsThread.start()

def stopNews():
    sendNews.stopSendingNews()
    global newsThread
    newsThread.join()
    newsThread = None

def search():
    if newsThread is None or not newsThread.is_alive():
        print("Thread is now running")
        getWebsite()
    else:
        print("Thread is stopped")
        stopNews()

window = tk.Tk()
window.geometry("800x500")  # Width x Height

title = tk.Label(text="News Notifier", font=("Arial", 24))
title.pack()

websiteTitle= tk.Label(text="Enter a website that you want to receive notifications from", font=("Arial", 19))
websiteTitle.pack()
sitename = tk.Entry(width=20, font=("Arial", 19))
sitename.pack()

def updateErrorLabel(error):
    errorLabel.config(text=error)

errorLabel = tk.Label(text='', font=("Arial", 19)) # TODO update on change
errorLabel.pack()


startButton = tk.Button(
    text="Start receveing news",
    width=25,
    height=5,
    bg="green",
    fg="black",
    font=("Arial", 19),
    command=search
)
startButton.pack()
endButton = tk.Button(
    text="Stop receveing news",
    width=25,
    height=5,
    bg="red",
    fg="black",
    font=("Arial", 19),
    command=stopNews
)
endButton.pack()



window.mainloop()

#  window.destroy()


