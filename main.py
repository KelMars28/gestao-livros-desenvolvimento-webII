from flask import Flask
from models.Geral import Base, engine

app = Flask(__name__)
# Chave secreta necessária para ativar o recurso de 'session' (criptografia do login)
app.secret_key = "dev-secret-key-production"

# Força o Python a ler os modelos de tabelas antes de mandar criar no XAMPP
from models.Usuario import Usuario
from models.Livro import Livro

# Cria as tabelas 'usuarios' e 'livros' no seu phpMyAdmin automaticamente
Base.metadata.create_all(engine)

# Importa as rotas do controlador
from controllers.AppController import *

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)