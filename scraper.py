"""
ToDo:
 - Ressorts herauslesen
 - # Kommentare herauslesen
"""


# imports
from bs4 import BeautifulSoup as bs
from os.path import isfile
import requests, json

# Dateinamen
dataFile = "data.json"

# abrufen des gesamten HTML-Inhalts
url = "https://www.nachrichten.at/nachrichten/ticker/"
html = requests.get(url)

# Herausfiltern der Artikel
soup = bs(html.content, "html.parser")
content = soup.find(id="newstickerArtikel")


# Titel der Artikel herauslesen
titlesHTML = soup.find_all("h3", class_="dreierTeaserVertikal__headline")
titles = []
for title in titlesHTML:
    titles.append(title.text[:-1].replace(" ", "").strip())


# Erscheinungszeit herauslesen
timesHTML = soup.find_all("span", class_="dreierTeaserVertikal__topline__zeit")
times = []
for time in timesHTML:
    times.append((time.text+"\n").replace(" ", "").replace("|", ""))


# OÖN+ Artikel herauslesen
plusHTML = soup.find_all("article")
plus = []
for p in plusHTML:
    if p.has_attr("class"):
        if "ooen_plus" in p["class"]:
            plus.append("OÖN+\n")
        else:
            plus.append("Kostenlos\n")


# Anzahl der Kommentare herauslesen



# Gesammelte Daten als JSON speichern
data = {}
prevData = {}
if isfile(dataFile):
    with open(dataFile, "r", encoding="utf-8") as f:
        prevData = json.load(f)
i = 0
while i < len(titles):
    data[titles[i]] = {
        "isPremium": plus[i] == "OÖN+\n",
        "time": times[i],
    }
    i += 1
data.update(prevData)

with open(dataFile, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)