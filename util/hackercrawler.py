import urllib.request as urllib
import os
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


def getHackerNews(require_time, file_path):

    HACKER_FILE = file_path

    try:

        last_update = ""

        try:
            with open(HACKER_FILE, "r") as _f:
                last_update = _f.readline()
        except: pass

        if len(last_update) == 0 or datetime.strptime(require_time, "%Y-%m-%d %H-%M-%S") - datetime.strptime(last_update, "%Y-%m-%d %H-%M-%S") > timedelta(hour=1):
            # try update news
            hacker_page = urllib.urlopen("http://www.daemonology.net/hn-daily/")
            _soup = BeautifulSoup(hacker_page, "lxml")
            # get latest date
            content = _soup.body.find("div", class_="content")
            last_date = content.h2.string[-10:]
            newslist = [(item.a['href'], item.a.string) for item in content.find_all("span", class_="storylink")[:10]]

            # write to file
            with open(HACKER_FILE, 'w') as _f:
                _f.write(require_time + '\n')
                for link, title in newslist:
                    _f.write(link + "$" + title + "\n")
            return newslist
    except: pass

    newslist = []
    try:
        with open(HACKER_FILE, "r") as _f:
            last_update = _f.readline()
            for line in _f:
                newslist.append(tuple(line.split("$")))
    except: pass

    return newslist
