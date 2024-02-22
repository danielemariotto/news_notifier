import tkinter as tk
import sendNews
import threading
newsThread = None

def getWebsite():
    global newsThread
    newsThread = None
    gWebsite = sitename.get()
    newsThread = threading.Thread(target=sendNews.getNewsAndSend, args=(gWebsite,))
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

errorLabel = tk.Label(text=sendNews.feedError, font=("Arial", 19)) # TODO update on change
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


