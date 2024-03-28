import os
import random as r
import sys
import numpy as np
import glob


def getChi(name):
    with open(name, "r") as file:
        lines = file.readlines()
    for i in lines:
        if i[:5] == "chi2:":
            return float(i[6:-1])


plik = open("chi2table.csv", "w+")

os.chdir("dataPoleski")
data = glob.glob("*.dat")
data.sort()
dic = {}
for i in data:
    dic[i] = {}

nothings = glob.glob("../" + sys.argv[1] + "/nothing/*.OUT")
nothings.sort()
for i in range(len(data)):
    dic[data[i]][nothings[i]] = getChi(nothings[i])

parallax = glob.glob("../" + sys.argv[1] + "/parallax/*.OUT")
parallax.sort()
for i in range(len(data)):
    dic[data[i]][parallax[i * 2]] = getChi(parallax[i * 2])
    dic[data[i]][parallax[i * 2 + 1]] = getChi(parallax[i * 2 + 1])

xallarap = glob.glob("../" + sys.argv[1] + "/xallarap/*.OUT")
xallarap.sort()
for i in range(len(data)):
    for j in range(1, 10):
        dic[data[i]][xallarap[i * 10 + j]] = getChi(xallarap[i * 10 + j])

diff = 30
for j in data:
    print(j, end=",")
    mini = 100000
    miniName = "E"
    miniB = 100000
    miniNameBest = "E"
    for i in dic[j].keys():
        print(dic[j][i], end=",")
        if dic[j][i] < mini:
            miniName = i
            if dic[j][i] + diff < mini:
                miniB = dic[j][i]
                miniNameBest = i
            mini = dic[j][i]

    if miniNameBest == "E":
        miniNameBest = miniName
        miniB = mini
    print(
        miniName
        + ","
        + miniNameBest[len(j) - 5 : miniNameBest.find("/PAR")]
        + ","
        + str(miniB)
    )
