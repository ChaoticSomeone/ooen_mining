# imports
from bs4 import BeautifulSoup as bs
from os.path import isfile
from platform import system as getOS
from os import system
import time
import requests, json

# Monatsauflistung
months = ["Jänner", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November",
          "Dezember"]

# Dateinamen
dataFile = "data.json"

# Umlaute

umlaute = ["ä", "ö", "ü", "Ä", "Ö", "Ü", "ß", "é"]
umlauteReplace = ["ae", "oe", "ue", "Ae", "Oe", "Ue", "ss", "e"]

# Config
Cooldown = 60 * 60  # Zeitspanne zwischen den Requests in Sekunden (Standardwert: 60 Minuten)

# Sonstige Variablen
t1 = time.time()
ignoreCooldown = True
newArticles = 0

while True:

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
    innerDivHTML = soup.find_all("div",
                                 class_="dreierTeaserVertikal__inner container__col--12 container__col--md6 container__col--lg6")
    comments = []
    for div in innerDivHTML:
        bottomLine = div.find("p", class_="dreierTeaserVertikal__bottomLine")
        if bottomLine is None:
            comments.append(0)
        else:
            comments.append(int(bottomLine.text.strip().split("\xa0")[0]))

    # Ressorts herauslesen
    ressortLinksHTML = soup.find_all("a",
                                     class_="dreierTeaserVertikal__topline__link dreierTeaserVertikal__topline__link--ressort")
    ressorts = []
    for ressortLink in ressortLinksHTML:
        splitLink = ressortLink["href"].split("/")
        filteredLink = list(filter(lambda text: len(text) > 0, splitLink))
        try:
            if len(filteredLink) > 0:
                if filteredLink[0] == "oberoesterreich":
                    filteredLink[0] = "lokales"
                ressort = filteredLink[0].title()
            else:
                ressort = "keine Angabe"
            ressorts.append(ressort)
        except:
            ressorts.append("keine Angabe")

    # Redakteur und Datum auslesen
    artikelLinksHTML = soup.find_all("a",
                                     class_="dreierTeaserVertikal__headline__link dreierTeaserVertikal__headline__link--fontSize")
    authors = []
    dates = []
    i = 0
    while i < len(artikelLinksHTML):
        print(f"\r{'.' * (i % 3 + 1)}{' ' * (3 - i % 3 + 1)}",
              end="")  # fancy loading (remove this line if it decreases performance)
        link = artikelLinksHTML[i]
        s = bs(requests.get(url + (link["href"][1:])).content, "html.parser")
        temp = s.find("div", class_="text-teaser text-darkgrey mb-32")
        if temp is not None:
            try:
                dataLine = temp.text.replace("\n", "").replace("\t", "").replace(" ", "").strip().split(",")
                authors.append(dataLine[0].split(" ", 1)[1])
            except:
                authors.append("unknown")
            try:
                date = list(filter(lambda text: text != "", dataLine[1].split(" ")))
            except:
                dates.append("unknown")
            if len(date) >= 3:
                dates.append(f"{date[0]} {months.index(date[1]) + 1}. {date[2]}")
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
        try:
            with open(dataFile, "r", encoding="utf-8") as f:
                prevData = json.load(f)
        except json.decoder.JSONDecodeError:
            prevData = {}
    i = 0
    while i < len(authors):
        j = 0
        while j < len(umlaute):
            authors[i] = authors[i].replace(umlaute[j], umlauteReplace[j])
            j += 1
        i += 1
    i = 0
    while i < len(titles):
        j = 0
        while j < len(umlaute):
            titles[i] = titles[i].replace(umlaute[j], umlauteReplace[j])
            j += 1
        i += 1
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
        if len(prevData.keys()) > 0 and not (titles[i] in prevData.keys()):
            newArticles += 1
        i += 1
    data.update(prevData)

    with open(dataFile, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Das Programm wartet 60 Minuten bis es wieder ausgeführt wird
    time.sleep(Cooldown)