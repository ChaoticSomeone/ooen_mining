import matplotlib.pyplot as plt
import json

with open("../data.json", "r", encoding="utf-8") as f:
	data = json.load(f)

times = {}
days = []
dayCount = 0
for i in range(0,24):
	times[("0" if i < 10 else "") + f"{i}"] = [0, 0]
for article in data:
	days.append(data[article]["date"])
	times[data[article]["time"].split(":")[0]][0] += 1
	if data[article]["isPremium"]: times[data[article]["time"].split(":")[0]][1] += 1
dayCount = len(set(days))


articles = [times[key][0] / dayCount for key in times.keys()]
premium = [times[key][1] / dayCount for key in times.keys()]

plt.xticks(range(0,24))

plt.title("Artikel der OÖN")
plt.xlabel("Zeit [h]")
plt.ylabel("Anzahl Artikel [1]")

plt.plot(range(0,24), articles, label="Anzahl der Artikel (incl. OÖN+)")
plt.plot(range(0,24), premium, label="Anzahl OÖN+ Artikel")
plt.legend()
plt.show()