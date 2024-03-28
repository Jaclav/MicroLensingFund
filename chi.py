import os
import random as r
import sys
import numpy as np
import glob

csv = open(sys.argv[1] + "/chi2.csv", "w")


# python3 chi.py sim27_12
def getChi(name):
    with open(name, "r") as file:
        lines = file.readlines()
    for i in lines:
        if i[:5] == "chi2:":
            return float(i[6:-1])


os.chdir("dataPoleski")
data = glob.glob("*.dat")
data.sort()
dic = {}
for i in data:
    dic[i] = {}

# load data

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
    for j in range(0, 10):
        dic[data[i]][xallarap[i * 10 + j]] = getChi(xallarap[i * 10 + j])

paraxal = glob.glob("../" + sys.argv[1] + "/PARAXALL/*.OUT")
paraxal.sort()
for i in range(len(data)):
    for j in range(0, 20):
        dic[data[i]][paraxal[i * 20 + j]] = getChi(paraxal[i * 20 + j])

# difference needed to fit better xallarap than parallax
DIFF = 80
csv.write("name,better,parallax,parallaxPath,xallarap,xallarapPath,deltaChi\n")
for j in data:
    csv.write(j + ",")
    mini = 100000
    miniName = "E"
    miniB = 100000
    miniNameBest = "E"
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

    paraxalChi = 100000
    paraxalName = ""
    for i in range(14, 32):
        if dic[j][keys[i]] == None:
            continue
        if paraxalChi > dic[j][keys[i]]:
            paraxalChi = dic[j][keys[i]]
            paraxalName = keys[i]

    # which is the lowest, parallax or xallarap or paraxal

    chiName = ""
    chiValue = 0
    if nothingChi < parallaxChi and nothingChi < xallarapChi:
        chiName = nothingName
        chiValue = nothingChi
    if xallarapChi + DIFF < parallaxChi:
        chiName = xallarapName
        chiValue = xallarapChi
    # if paraxalChi + DIFF < parallaxChi and paraxalChi + DIFF < xallarapChi:
    #     chiName = paraxalName
    #     chiValue = paraxalChi
    else:
        chiName = parallaxName
        chiValue = parallaxChi

    csv.write(
        # str(nothingChi)
        # + ","
        chiName[len(j) - 5 : chiName.find("/PAR")]
        + ","
        + str(parallaxChi)
        + ","
        + str(parallaxName)
        + ","
        + str(xallarapChi)
        + ","
        + str(xallarapName)
        + ","
        # + chiName
        # + ","
        # + str(chiValue)
        # + ","
        + str(parallaxChi - xallarapChi)
        + "\n"
    )
#awk -F"," '{print $NF, $2, $0}' sim27_12/chi2.csv | sort -g
