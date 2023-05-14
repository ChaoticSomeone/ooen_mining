# imports
from bs4 import BeautifulSoup as bs
from os.path import isfile
import requests, json


# Monatsauflistung
months = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]


# Dateinamen
dataFile = "data.json"

# abrufen des gesamten HTML-Inhalts
url = "https://www.nachrichten.at/nachrichten/ticker/"
html = requests.get(url)
soup = bs(html.content, "html.parser")


# Titel der Artikel herauslesen
titlesHTML = soup.find_all("h3", class_="dreierTeaserVertikal__headline")
titles = []
for title in titlesHTML:
    titles.append(title.text[:-1].replace(" ", "").strip())


# Erscheinungszeit herauslesen
timesHTML = soup.find_all("span", class_="dreierTeaserVertikal__topline__zeit")
times = []
for time in timesHTML:
    times.append(time.text.replace(" ", "").replace("|", ""))


# OÖN+ Artikel herauslesen
plusHTML = soup.find_all("article")
plus = []
for p in plusHTML:
    if p.has_attr("class"):
        plus.append("ooen_plus" in p["class"])

# Anzahl der Kommentare herauslesen
innerDivHTML = soup.find_all("div", class_="dreierTeaserVertikal__inner container__col--12 container__col--md6 container__col--lg6")
comments = []
for div in innerDivHTML:
    bottomLine = div.find("p", class_="dreierTeaserVertikal__bottomLine")
    if bottomLine is None:
        comments.append(0)
    else:
        comments.append(int(bottomLine.text.strip().split("\xa0")[0]))


# Ressorts herauslesen
ressortLinksHTML = soup.find_all("a", class_="dreierTeaserVertikal__topline__link dreierTeaserVertikal__topline__link--ressort")
ressorts = []
for ressortLink in ressortLinksHTML:
    splitLink = ressortLink["href"].split("/")
    filteredLink = list(filter(lambda text: len(text) > 0, splitLink))
    if len(filteredLink) > 0:
        if filteredLink[0] == "oberoesterreich":
            filteredLink[0] = "lokales"
        ressort = filteredLink[0].title()
    else:
        ressort = "keine Angabe"
    ressorts.append(ressort)


# Redakteur und Datum auslesen
artikelLinksHTML = soup.find_all("a", class_="dreierTeaserVertikal__headline__link dreierTeaserVertikal__headline__link--fontSize")
authors = []
dates = []
i = 0
while i < len(artikelLinksHTML):
    print(f"\r{'.' * (i % 3 + 1)}{' ' * (3 - i % 3 + 1)}", end="") # fancy loading (remove this line if it decreases performance)
    link = artikelLinksHTML[i]
    s = bs(requests.get(url + (link["href"][1:])).content, "html.parser")
    temp = s.find("div", class_="text-teaser text-darkgrey mb-32")
    if temp is not None:
        dataLine = temp.text.replace("\n", "").replace("\t", "").replace(" ", "").strip().split(",")
        authors.append(dataLine[0].split(" ", 1)[1])
        if len(dataLine) >= 2:
            date = list(filter(lambda text: text != "", dataLine[1].split(" ")))
            if len(date) >= 3:
                dates.append(f"{date[0]} {months.index(date[1]) + 1}. {date[2]}")
            else:
                dates.append("unknown")
        else:
            dates.append("unknown")

    else:
        authors.append("unknown")
        dates.append("unknown")
    i += 1

# Gesammelte Daten als JSON speichern
data = {}
prevData = {}
if isfile(dataFile):
    with open(dataFile, "r", encoding="utf-8") as f:
        prevData = json.load(f)
i = 0
while i < len(titles):
    data[titles[i]] = {
        "isPremium": plus[i],
        "date": dates[i],
        "time": times[i],
        "comments": comments[i],
        "ressort": ressorts[i],
        "author": authors[i]
    }
    i += 1
data.update(prevData)

with open(dataFile, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)