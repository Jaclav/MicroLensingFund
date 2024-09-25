import os
import random as r
import sys
import numpy as np
import glob


# python3 chi.py sim27_12
def getChi(name):
    with open(name, "r") as file:
        lines = file.readlines()
    for i in lines:
        if i[:5] == "chi2:":
            return float(i[6:-1])
    return 1000000


csv = open(sys.argv[1] + "/chi2.csv", "w")
os.chdir("dataPoleski")
data = glob.glob("*.dat")
data.sort()
dic = {}
for i in data:
    dic[i] = {}

# load data


def load(name, maxJ):
    mini = 1000000
    parallax = glob.glob("../" + sys.argv[1] + "/" + name + "/*.OUT")
    parallax.sort()
    print(parallax)
    for i in range(len(data)):
        for j in range(0, maxJ):
            print(parallax[i * maxJ + j])
            chi2 = getChi(parallax[i * maxJ + j])
            dic[data[i]][parallax[i * maxJ + j]] = chi2


load("nothing", 1)
load("parallax", 2)
load("xallarap", 10)

# difference needed to fit better xallarap than parallax
DIFF = 25
csv.write("name,better,parallax,parallaxPath,xallarap,xallarapPath,deltaChi\n")
for j in data:
    csv.write(j + ",")
    keys = list(dic[j].keys())

    # find lowest values for nothing, parallax, xallarap, paraxall

    nothingChi = dic[j][keys[0]]
    nothingName = keys[0]

    parallaxChi = 0
    parallaxName = ""
    if dic[j][keys[1]] < dic[j][keys[2]]:
        parallaxChi = dic[j][keys[1]]
        parallaxName = keys[1]
    else:
        parallaxChi = dic[j][keys[2]]
        parallaxName = keys[2]

    xallarapChi = 100000
    xallarapName = ""
    for i in range(3, 13):
        if xallarapChi > dic[j][keys[i]]:
            xallarapChi = dic[j][keys[i]]
            xallarapName = keys[i]

    chiName = ""
    chiValue = 0
    if nothingChi < parallaxChi and nothingChi < xallarapChi:
        chiName = nothingName
        chiValue = nothingChi
    if xallarapChi + DIFF < parallaxChi:
        chiName = xallarapName
        chiValue = xallarapChi
    else:
        chiName = parallaxName
        chiValue = parallaxChi

    csv.write(
        chiName[len(j) - 8 : chiName.find("/PAR")]
        + ","
        + str(parallaxChi)
        + ","
        + str(parallaxName)
        + ","
        + str(xallarapChi)
        + ","
        + str(xallarapName)
        + ","
        + str(parallaxChi - chiValue)
        + "\n"
    )
# awk -F"," '{print $NF, $2, $0}' sim27_12/chi2.csv | sort -g
