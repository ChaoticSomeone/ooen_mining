import matplotlib.pyplot as plt
import numpy as np

d_times = (
    34, 0, 0, 0, 0, 0, 0, 0, 2, 11, 4, 8, 6, 7, 9, 13, 17, 10,
    13, 13, 30, 4, 17, 9, 14, 43, 10, 12, 10, 11, 11, 6, 10,
    13, 4, 15, 12, 3, 9, 4, 13, 22, 25, 5, 20, 11, 27, 27, 6, 7
)
print(len(d_times))

plt.title("Zeitdifferenz zwischen den Artikeln")
plt.xlabel("Zeitdifferenz [min]")
plt.ylabel("Anzahl der Artikel [1]")

plt.hist(d_times, bins=12, linewidth=0.5, edgecolor="white", range=(0,60))
plt.show()