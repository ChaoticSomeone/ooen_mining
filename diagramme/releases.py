import matplotlib.pyplot as plt
import json

with open("../data.json", "r", encoding="utf-8") as f:
	data = json.load(f)

times = {}
for i in range(0,24):
	times[("0" if i < 10 else "") + f"{i}"] = [0, 0]
for article in data:
	times[data[article]["time"].split(":")[0]][0] += 1
	if data[article]["isPremium"]: times[data[article]["time"].split(":")[0]][1] += 1


articles = [times[key][0] for key in times.keys()]
premium = [times[key][1] for key in times.keys()]

plt.xticks(range(0,24))

plt.title("Artikel der OÖN")
plt.xlabel("Zeit [h]")
plt.ylabel("Anzahl Artikel [1]")

plt.plot(range(0,24), articles, label="Anzahl der Artikel (incl. OÖN+)")
plt.plot(range(0,24), premium, label="Anzahl OÖN+ Artikel")
plt.legend()
plt.show()