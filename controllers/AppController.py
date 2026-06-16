from flask import render_template, request, redirect, url_for, session as flask_session
from main import app 
from models.Geral import Session
from models.Usuario import Usuario
from models.Livro import Livro

# ================= ROTA DE LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db_session = Session()
        try:
            txt_login = request.form.get("login")
            txt_senha = request.form.get("senha")
            
            # Procura o usuário no banco do XAMPP
            usuario = db_session.query(Usuario).filter(Usuario.login == txt_login, Usuario.senha == txt_senha).first()
            
            if usuario:
                flask_session["usuario_logado"] = usuario.nome # Salva na sessão da página
                return redirect(url_for("listar_livros"))
            else:
                return render_template("login.html", erro="Usuário ou senha inválidos!")
        finally:
            db_session.close() # FECHA A CONEXÃO
            
    return render_template("login.html", erro=None)

@app.route("/logout")
def logout():
    flask_session.pop("usuario_logado", None) # Limpa o login
    return redirect(url_for("login"))


# ================= CRUD DE LIVROS (SÓ ENTRA SE LOGADO) =================
@app.route("/livros")
def listar_livros():
    if "usuario_logado" not in flask_session:
        return redirect(url_for("login")) # Expulsa se não estiver logado
        
    db_session = Session()
    try:
        lista = db_session.query(Livro).all()
        return render_template("livros/lista.html", todos_os_livros=lista, nome_usuario=flask_session["usuario_logado"])
    finally:
        db_session.close() # FECHA A CONEXÃO

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
        db_session.close() # FECHA A CONEXÃO

@app.route("/livros/editar/<int:id>")
def editar_livro(id):
    if "usuario_logado" not in flask_session: return redirect(url_for("login"))
    db_session = Session()
    try:
        livro = db_session.query(Livro).filter(Livro.id == id).first()
        return render_template("livros/formulario.html", livro=livro)
    finally:
        db_session.close() # FECHA A CONEXÃO

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
        db_session.close() # FECHA A CONEXÃO

# ROTA PARA ABRIR A TELA DE CADASTRO DE USUÁRIO
@app.route("/registrar")
def novo_usuario_externo():
    return render_template("cadastro_usuario.html")

# ROTA PARA SALVAR O NOVO USUÁRIO NO BANCO DO XAMPP
@app.route("/registrar/salvar", methods=["POST"])
def salvar_usuario_externo():
    db_session = Session()
    try:
        nome = request.form.get("nome")
        login = request.form.get("login")
        senha = request.form.get("senha")
        
        # Cria o usuário e manda pro MySQL
        novo_usuario = Usuario(nome=nome, login=login, senha=senha)
        db_session.add(novo_usuario)
        db_session.commit()
        
        # Redireciona de volta para o login para ele estrear a conta!
        return redirect(url_for("login"))
    finally:
        db_session.close() # FECHA A CONEXÃO

from flask import jsonify
@app.route("/autor")
def endpoint_autor():
    dados_autor = {
        "nome_desenvolvedor": "Raquel Martins",
        "Matricula": "20252072500136", 
        "disciplina": "Desenvolvimento Web II - IFCE Sobral",
        "ano": "2026"
    }
    return jsonify(dados_autor)