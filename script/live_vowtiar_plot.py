import numpy as np
from matplotlib import style
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
import os

demo_path = sys.argv

# print(demo_path[1], "demo_path")

INPUT_FILE= "script/out.npy"

INPUT_FILE =  os.path.join(demo_path[1], INPUT_FILE)


# style.use("fivethirtyeight")

D_id_color = {'A': u'orchid', 'B': u'darkcyan', 'C': u'grey', 'D': u'dodgerblue', 'E': u'turquoise', 'F': u'darkviolet'}

vowel_color = {'/a/': u'orchid',
               '/i/': u'darkcyan', 
               '/u/': u'dodgerblue'}

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

s = 256
def animate(i):

    formants = np.load(INPUT_FILE)

    area_mat = np.concatenate((formants, np.ones((3, 1))), axis=1)
    area = np.abs(np.linalg.det(area_mat) / 2)

    ax1.clear()
    ax1.set_xlim([100, 1000])
    ax1.set_ylim([600, 3000])

    t1 = plt.Polygon(formants, color="#4D4D4D", fill=False, lw=4)
    plt.gca().add_patch(t1)
    plt.title(f"Vowel Triangle Area: {int(area)}", fontsize=12)

    ax1.scatter(formants[0, 0], formants[0, 1], color=vowel_color['/a/'], s=s)
    ax1.scatter(formants[1, 0], formants[1, 1], color=vowel_color['/i/'], s=s)
    ax1.scatter(formants[2, 0], formants[2, 1], color=vowel_color['/u/'], s=s)

    markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in vowel_color.values()]
    plt.legend(markers, vowel_color.keys(), numpoints=1)

ani = animation.FuncAnimation(fig, animate, interval=500)
markers = [plt.Line2D([0,0],[0,0],color=color, marker='o', linestyle='') for color in vowel_color.values()]
plt.legend(markers, vowel_color.keys(), numpoints=1)
plt.show()
