import matplotlib.pyplot as plt
import numpy as np

articles = np.array([
#    0  1  2  3  4  5  6  7  8  9 10 11 12  13  14 15 16
	15, 5, 4, 2, 6, 6, 4, 4, 7, 5, 8, 7, 4, 10, 11, 5
])

premium = np.array([
#   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16
	7, 2, 2, 1, 3, 5, 2, 1, 3, 0, 2, 1, 0, 4, 5, 2
])

times = range(0, len(articles))

plt.xticks(times, [f"{h}:00" for h in times])
plt.yticks(range(0, max(articles)+1))

plt.title("Artikel der OÖN")
plt.xlabel("Zeit [h]")
plt.ylabel("Anzahl Artikel [1]")

plt.plot(times, articles, label="Anzahl der Artikel (incl. OÖN+)")
plt.plot(times, premium, label="Anzahl OÖN+ Artikel")
plt.legend()
plt.show()