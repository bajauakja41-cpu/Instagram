import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔹 Use a variável de ambiente do Render ou essa URL fixa (apenas para testes locais)
db_url = os.getenv(
    "DATABASE_URL",
    "postgresql://banco_de_dados_vbur_user:YxTha35htBXbCaVSXf11rpaLfGTFbLHJ@dpg-d30uip7fte5s73fsljf0-a.oregon-postgres.render.com/banco_de_dados_vbur"
)

# Render às vezes usa o prefixo antigo postgres:// → corrigimos
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelo
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    email = request.form["email"]
    senha = request.form["senha"]

    novo = Usuario(email=email, senha=senha)
    db.session.add(novo)
    db.session.commit()

    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # cria tabelas no Postgres automaticamente
    app.run(host="0.0.0.0", port=5000, debug=True)
