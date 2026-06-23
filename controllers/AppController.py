from flask import render_template, request, redirect, url_for, session as flask_session
from flask import jsonify
from sqlalchemy import func
from main import app 
from models.Geral import Session
from models.Usuario import Usuario
from models.Livro import Livro

# ================= ROTA DE LOGIN (PÁGINA INICIAL) =================
@app.route("/", methods=["GET", "POST"])
def login():
    # Se o usuário já estiver logado, manda direto para o Dashboard
    if "usuario_logado" in flask_session:
        return redirect(url_for("exibir_dashboard"))

    if request.method == "POST":
        db_session = Session()
        try:
            txt_login = request.form.get("login")
            txt_senha = request.form.get("senha")
            
            usuario = db_session.query(Usuario).filter(Usuario.login == txt_login, Usuario.senha == txt_senha).first()
            
            if usuario:
                flask_session["usuario_logado"] = usuario.nome 
                # MUDANÇA AQUI: Agora, ao logar, vai direto para o Dashboard!
                return redirect(url_for("exibir_dashboard"))
            else:
                return render_template("login.html", erro="Usuário ou senha inválidos!")
        finally:
            db_session.close() 
            
    return render_template("login.html", erro=None)

@app.route("/logout")
def logout():
    flask_session.pop("usuario_logado", None) 
    return redirect(url_for("login"))


# ================= DASHBOARD DO SISTEMA =================
@app.route("/dashboard")
def exibir_dashboard():
    if "usuario_logado" not in flask_session:
        return redirect(url_for("login"))
        
    db_session = Session()
    try:
        total_livros = db_session.query(func.count(Livro.id)).scalar()
        total_usuarios = db_session.query(func.count(Usuario.id)).scalar()
        
        return render_template(
            "dashboard.html", 
            total_livros=total_livros, 
            total_usuarios=total_usuarios, 
            nome_usuario=flask_session["usuario_logado"]
        )
    finally:
        db_session.close()


# ================= CRUD DE LIVROS =================
@app.route("/livros")
def listar_livros():
    if "usuario_logado" not in flask_session:
        return redirect(url_for("login")) 
        
    db_session = Session()
    try:
        lista = db_session.query(Livro).all()
        return render_template("livros/lista.html", todos_os_livros=lista, nome_usuario=flask_session["usuario_logado"])
    finally:
        db_session.close() 

@app.route("/livros/novo")
def novo_livro():
    if "usuario_logado" not in flask_session: return redirect(url_for("login"))
    return render_template("livros/formulario.html", livro=None)

@app.route("/livros/salvar", methods=["POST"])
def salvar_livro():
    if "usuario_logado" not in flask_session: return redirect(url_for("login"))
    db_session = Session()
    try:
        id_livro = request.form.get("id")
        titulo = request.form.get("titulo")
        autor = request.form.get("autor")
        ano = request.form.get("ano")

        if id_livro: 
            livro = db_session.query(Livro).filter(Livro.id == id_livro).first()
            livro.titulo = titulo
            livro.autor = autor
            livro.ano = ano
        else: 
            livro = Livro(titulo=titulo, autor=autor, ano=ano)
            db_session.add(livro)

        db_session.commit() 
        return redirect(url_for("listar_livros"))
    finally:
        db_session.close() 

@app.route("/livros/editar/<int:id>")
def editar_livro(id):
    if "usuario_logado" not in flask_session: return redirect(url_for("login"))
    db_session = Session()
    try:
        livro = db_session.query(Livro).filter(Livro.id == id).first()
        return render_template("livros/formulario.html", livro=livro)
    finally:
        db_session.close() 

@app.route("/livros/deletar/<int:id>")
def deletar_livro(id):
    if "usuario_logado" not in flask_session: return redirect(url_for("login"))
    db_session = Session()
    try:
        livro = db_session.query(Livro).filter(Livro.id == id).first()
        db_session.delete(livro)
        db_session.commit()
        return redirect(url_for("listar_livros"))
    finally:
        db_session.close() 


# ================= TELA DE CADASTRO DE USUÁRIO =================
@app.route("/registrar")
def novo_usuario_externo():
    return render_template("cadastro_usuario.html")

@app.route("/registrar/salvar", methods=["POST"])
def salvar_usuario_externo():
    db_session = Session()
    try:
        nome = request.form.get("nome")
        login = request.form.get("login")
        senha = request.form.get("senha")
        
        novo_usuario = Usuario(nome=nome, login=login, senha=senha)
        db_session.add(novo_usuario)
        db_session.commit()
        
        return redirect(url_for("login"))
    finally:
        db_session.close() 


# ================= ENDPOINT DO AUTOR (API) =================
@app.route("/autor")
def endpoint_autor():
    dados_autor = {
        "nome_desenvolvedor": "Raquel Martins",
        "Matricula": "20252072500136", 
        "disciplina": "Desenvolvimento Web II - IFCE Sobral",
        "ano": "2026"
    }
    return jsonify(dados_autor)