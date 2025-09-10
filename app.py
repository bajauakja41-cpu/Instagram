from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)

# Conexão com banco do Render
DB_URL = "postgresql://banco_de_dados_vbur_user:YxTha35htBXbCaVSXf11rpaLfGTFbLHJ@dpg-d30uip7fte5s73fsljf0-a.oregon-postgres.render.com/banco_de_dados_vbur"
engine = create_engine(DB_URL, echo=True)

# Cria tabela se não existir
def init_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    email TEXT NOT NULL,
                    senha TEXT NOT NULL
                )
            """))
            conn.commit()
    except SQLAlchemyError as e:
        print("Erro ao inicializar banco:", e)

# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        if email and senha:
            try:
                with engine.connect() as conn:
                    conn.execute(text("INSERT INTO usuarios (email, senha) VALUES (:email, :senha)"),
                                 {"email": email, "senha": senha})
                    conn.commit()
            except SQLAlchemyError as e:
                print("Erro ao salvar usuário:", e)

        return redirect(url_for("index"))

    return render_template("index.html")

# Login do administrador
@app.route("/painel/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == "adm12" and senha == "adm12":
            return redirect(url_for("painel"))
        else:
            error = "Usuário ou senha incorretos."

    return render_template("admin_login.html", error=error)

# Painel do administrador
@app.route("/painel")
def painel():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, email, senha FROM usuarios ORDER BY id DESC"))
            logins = result.fetchall()
    except SQLAlchemyError as e:
        print("Erro ao buscar usuários:", e)
        logins = []

    return render_template("painel.html", logins=logins)

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
