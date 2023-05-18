import matplotlib.pyplot as plt
import json

with open("../data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ressorts = {
    "Lokales": 0,
    "Politik": 0,
    "Panorama": 0,
    "Wirtschaft": 0,
    "Sport": 0,
    "Meinung": 0,
    "Kultur": 0,
    "Meine Welt": 0,
    "Keine Angabe": 0
}

for article in data:
    if data[article]["ressort"] == "Meine-Welt": data[article]["ressort"] = "Meine Welt"
    try:
        ressorts[data[article]["ressort"].title()] += 1
    except KeyError:
        ressorts["Keine Angabe"] += 1
ressorts = dict(sorted(ressorts.items(), key=lambda value: value[1], reverse=True))

colors = [
    "#03045e",
    "#023e8a",
    "#0077b6",
    "#0096c7",
    "#00b4d8",
    "#48cae4",
    "#90e0ef",
    "#ade8f4",
    "#aaaaaa"
]

plt.pie(ressorts.values(), labels=ressorts.keys(), colors=colors, startangle=90, counterclock=False)
plt.show()