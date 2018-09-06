import os
import json
import numpy as np
import cv2
import utils

teams = {}
max_wins = 0
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
            if line != "":
                first_team, first_score, second_score, second_team = line.split(' ')
                if first_score > second_score:
                    winner = first_team.lower()
                    loser = second_team.lower()
                else:
                    winner = second_team.lower()
                    loser = first_team.lower()
                teams[winner].append(int(teams[winner][-1]) + 1)
                teams[loser].append(teams[loser][-1])
                max_wins = max(max_wins, teams[winner][-1])

team_names = list(teams.keys())

rows = max_wins+1
total_teams = len(team_names)

teams_in_row = [[] for i in range(rows)]
for team_name in teams:
    teams_in_row[teams[team_name][1]].append(team_name)

icon_size = 50
space_between = 5
max_height = rows * (icon_size + space_between) + 100
total_width = icon_size * total_teams + space_between * (total_teams + 1)

def required_width(number_of_teams):
    return icon_size * number_of_teams + space_between * (number_of_teams - 1)

img = utils.create_base_img(max_height, total_width + 130, rows, icon_size, space_between)

for row_number in range(rows):
    number_of_teams = len(teams_in_row[row_number])
    if number_of_teams == 0:
        continue
    next_location = 100 + (total_width - required_width(number_of_teams)) // 2

    for team_name in teams_in_row[row_number]:
        logo = utils.read_transparent_png('logos/%s.png' % team_name)
        logo = cv2.resize(logo, (icon_size, icon_size))

        y = max_height - 90 - row_number * (icon_size + space_between)
        img[y:y+icon_size, next_location:next_location+icon_size] = logo

        next_location = next_location + icon_size + space_between

cv2.imshow('standings', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
