import matplotlib.pyplot as plt
import json

with open("../data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

times = {}
days = []
dayCount = 0
for i in range(0,24):
    times[("0" if i < 10 else "") + f"{i}"] = {
        "Lokales": 0,
        "Panorama": 0,
        "Wirtschaft": 0
    }

for key in data.keys():
    timeKey = data[key]["time"].split(":")[0]
    if data[key]["ressort"].title() in times["00"].keys():
        times[timeKey][data[key]["ressort"].title()] += 1

ressorts = {
    "Lokales": [],
    "Panorama": [],
    "Wirtschaft": []
}

for tKey in times.keys():
    for key in times[tKey].keys():
        ressorts[key].append(times[tKey][key])


plt.xticks(range(0,24))
plt.title("Erscheinungszeiten der Ressorts")
plt.xlabel("Zeit [h]")
plt.ylabel("Anzahl Artikel [1]")

for key in ressorts:
    plt.stackplot(range(0,24), ressorts[key])
plt.legend(["Anzahl der Artikel des Ressort Lokales", "Anzahl der Artikel des Ressort Panorama", "Anzahl der Artikel des Ressort Wirtschaft"])
plt.show()
