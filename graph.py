import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.offsetbox import (TextArea, DrawingArea, OffsetImage,
                                  AnnotationBbox)

teams = {}
total_weeks = 0
with open('eu-results.txt') as f:
    reading_teams = True
    for line in f:
        line = line[:-1]
        if reading_teams:
            if line == "":
                reading_teams = False
            else:
                teams[line.lower()] = [0]
        else:
            if line == "":
                total_weeks = total_weeks + 1
            else:
                first_team, first_score, second_score, second_team = line.split(' ')
                if first_score > second_score:
                    winner = first_team.lower()
                    loser = second_team.lower()
                else:
                    winner = second_team.lower()
                    loser = first_team.lower()
                teams[winner].append(int(teams[winner][-1]) + 1)
                teams[loser].append(teams[loser][-1])

team_names = list(teams.keys())# [mpimg.imread('logos/%s.png' % key) for key in teams]
wins = [teams[key][-1] for key in teams]

rows = total_weeks
cols = len(team_names)
fig, ax = plt.subplots()

for i in range(cols):
    arr_img = plt.imread('logos/%s.png' % team_names[i], format='png')

    imagebox = OffsetImage(arr_img, zoom=0.1)
    imagebox.image.axes = ax

    ab = AnnotationBbox(imagebox, (0, 0),
                        xybox=(20 + i * 40., wins[i] * 15.),
                        xycoords='data',
                        boxcoords="offset points",
                        pad=0.5)

    ax.add_artist(ab)

# fig = plt.figure(figsize = (cols / 3 + 1, rows / 3))
# plt.subplot2grid((cols/4, rows/4), 0, rowspan=1, colspan=1)
# fig.add_subplot(rows, cols, )


# for ind, win in enumerate(wins):
#     ax[total_weeks - win][ind].imshow(logos[ind])

# for i in range(len(logos)):
#     img = logos[i]
#     fig.add_subplot(rows, columns, i+1)
#     plt.imshow(img)
ax.set_xlim(0, cols)
ax.set_ylim(0, rows)
plt.show()
