from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Conexão com banco do Render
DB_URL = "postgresql://banco_de_dados_vbur_user:YxTha35htBXbCaVSXf11rpaLfGTFbLHJ@dpg-d30uip7fte5s73fsljf0-a.oregon-postgres.render.com/banco_de_dados_vbur"
engine = create_engine(DB_URL, echo=True)

# 🔹 Criar tabela se não existir
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM usuarios WHERE email = :email AND senha = :senha"),
                {"email": email, "senha": senha}
            ).fetchone()

        if result:
            return redirect(url_for("painel"))
        else:
            error = "Usuário ou senha incorretos."

    return render_template("index.html", error=error)

@app.route("/painel")
def painel():
    return render_template("painel.html")

if __name__ == "__main__":
    app.run(debug=True)
