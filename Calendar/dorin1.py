from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app) # cross origin

@app.route("/site.html",methods=['GET','POST','PUT'])
def get_orar():


    data = request.json
    x = json.loads(data)
    #print(x["grupa"]) #doar dictionar ai voie in jscript

    url = "https://www.cs.ubbcluj.ro/files/orar/2020-1/tabelar/I1.html"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    table_all = soup.find_all("table")

    citit = x["grupa"] #citit = input("Numarul grupei(ex: 211/1): ")

    gr, subgr = citit.split("/")
    gr = int(gr)-211
    subgr = int(subgr)

    gr = 0
    subgr = 1

    table = table_all[gr]

    k = 0
    lista = {}
    rows = table.find_all("tr")
    for row in rows[1:]:
        zi = row.find_all("td")[0].text.strip()
        ora = row.find_all("td")[1].text.strip()
        frecv = row.find_all("td")[2].text.strip()
        form = row.find_all("td")[4].text.strip()
        tip = row.find_all("td")[5].text.strip()
        disc = row.find_all("td")[6].text.strip()
        prof = row.find_all("td")[7].text.strip()

        if frecv == "":
            frecv = 0
        elif frecv == "sapt. 1":
            frecv = 1
        elif frecv == "sapt. 2":
            frecv = 2

        if form[-2:] == "/1":
            form = 1
        elif form[-2:] == "/2":
            form = 2
        else:
            form = subgr

        #prof = prof.split(" ", 1)[1]

        if form == subgr:
             # nu am mai pus formatia
            lista[k] = {"zi":zi,"ora":ora,"frecv":frecv,"tip":tip,"disc":disc,"prof":prof}
            k += 1

    #for el in lista:
        #print(el)
    return lista

app.run(debug = True)