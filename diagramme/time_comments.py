import matplotlib.pyplot as plt
import json

with open("../data.json", "r", encoding="utf-8") as f:
	data = json.load(f)

times = {}
days = []
dayCount = 0
for i in range(0,24):
	times[("0" if i < 10 else "") + f"{i}"] = 0
for key in data.keys():
	days.append(data[key]["date"])
	times[data[key]["time"].split(":")[0]] += data[key]["comments"]
dayCount = len(set(days))

comments = [times[key] / dayCount for key in times.keys()]

plt.xticks(range(0,24))
plt.title("Artikel der OÖN")
plt.xlabel("Zeit [h]")
plt.ylabel("Anzahl Kommentare [1]")

plt.plot(range(0,24), comments, label="Anzahl der Kommentare")
plt.legend()
plt.show()