from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Pais(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(200))
    continente = db.Column(db.String(200))
    capital = db.Column(db.String(200))
    moeda = db.Column(db.String(200))

    def __init__(self, nome,continente,capital,moeda):
        self.nome = nome
        self.continente = continente
        self.capital = capital
        self.moeda = moeda
        