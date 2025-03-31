import urllib.request
from flask import render_template, request, redirect, url_for

# Importando o Model
from models.database import db, Pais
import urllib
import json

cidades = []
paislist = [
    {
        "nome": "Brasil",
        "capital": "Brasília",
        "continente": "América do Sul",
        "moeda": "Real Brasileiro",
    }
]


def init_app(app):
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/paises", methods=["GET", "POST"])
    def paises():
        pais = paislist[0]
        if request.method == "POST":
            if request.form.get("cidade"):
                cidades.append(request.form.get("cidade"))
        return render_template("paises.html", pais=pais, cidades=cidades)

    @app.route("/cadpaises", methods=["GET", "POST"])
    def cadpaises():
        if request.method == "POST":
            # Verificando se todos os campos foram preenchidos
            if (
                request.form.get("nome")
                and request.form.get("capital")
                and request.form.get("continente")
                and request.form.get("moeda")
            ):

                # Adicionando o país na lista
                paislist.append(
                    {
                        "nome": request.form.get("nome"),
                        "capital": request.form.get("capital"),
                        "continente": request.form.get("continente"),
                        "moeda": request.form.get("moeda"),
                    }
                )
        return render_template("cadpaises.html", paislist=paislist)

    @app.route("/apipaises", methods=["GET", "POST"])
    def apipaises():
        url = "https://restcountries.com/v3.1/all"
        res = urllib.request.urlopen(url)
        data = res.read()
        paisesjson = json.loads(data)
        return render_template("apipaises.html", paisesjson=paisesjson)

    @app.route("/bancopaises", methods=["GET", "POST"])
    @app.route("/bancopaises/delete/<int:id>")
    def bancopaises(id=None):
        if id:
            pais = Pais.query.get(id)
            db.session.delete(pais)
            db.session.commit()
            return redirect(url_for("bancopaises"))

        if request.method == "POST":
            newpais = Pais(
                request.form["nome"],
                request.form["capital"],
                request.form["continente"],
                request.form["moeda"],
            )
            db.session.add(newpais)
            db.session.commit()
            return redirect(url_for("bancopaises"))
        else:
            page = request.args.get("page", 1, type=int)
            per_page = 3
            pais_page = Pais.query.paginate(page=page, per_page=per_page)
            return render_template("bancopaises.html", paisescadastrados=pais_page)

    @app.route("/edit/<int:id>", methods=["GET", "POST"])
    def edit(id):
        p = Pais.query.get(id)

        if request.method == "POST":
            p.nome = request.form["nome"]
            p.capital = request.form["capital"]
            p.continente = request.form["continente"]
            p.moeda = request.form["moeda"]
            db.session.commit()
            return redirect(url_for("bancopaises"))
        return render_template("edit.html", p=p)
