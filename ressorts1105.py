import matplotlib.pyplot as plt
import numpy as np

data = [5, 45, 5, 8, 13, 7, 5, 12]
data = sorted(data, reverse=True)
labels = ["Meinung","Lokales","Kultur","Wirtschaft","Politik","Sport","Meine Welt","Panorama"]
colors = [
    "#03045e",
    "#023e8a",
    "#0077b6",
    "#0096c7",
    "#00b4d8",
    "#48cae4",
    "#90e0ef",
    "#ade8f4"
]

plt.pie(data, labels=labels, colors=colors, startangle=90, counterclock=False)
plt.show()