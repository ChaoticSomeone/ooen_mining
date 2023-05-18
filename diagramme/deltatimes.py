import matplotlib.pyplot as plt
import json

def ReverseDictionary(dictionary):
    newDict = {}
    for key in reversed(dictionary.keys()):
        newDict[key] = dictionary[key]
    return newDict

with open("../data.json", "r", encoding="utf-8") as f:
    data = ReverseDictionary(json.load(f))

times = []
for key in data.keys():
    hour = int(data[key]["time"].split(":")[0]) * 60 # h to min
    minute = int(data[key]["time"].split(":")[1][0:2])
    times.append(hour + minute)

deltatimes = []
i = 1
while i < len(times):
    dt = times[i] - times[i-1]
    if dt >= 0:
        deltatimes.append(dt)
    i += 1

plt.title("Zeitdifferenz zwischen den Artikeln")
plt.xlabel("Zeitdifferenz [min]")
plt.ylabel("Anzahl der Artikel [1]")

plt.hist(deltatimes, bins=12, linewidth=0.5, edgecolor="white", range=(0,60))
plt.show()