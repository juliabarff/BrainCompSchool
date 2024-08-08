from tinydb import TinyDB, Query
import os
import json
import uuid

LOCAL_FOLDER = (os.path.abspath(os.path.join(os.path.dirname(__file__))))
db = TinyDB(os.path.join(LOCAL_FOLDER, 'brain.json'))
db_user = TinyDB(os.path.join(LOCAL_FOLDER, 'users_brain.json'))

Article = Query()

"""

Gerenciando o banco de dados:

Estrutura do Artigo--
-- Titulo
-- Corpo
-- Data de cração/postagem

Estrutura Usuário
-- Nome
-- Senha
-- Email

"""

"""
levantamento de requisitos

determinamos a ordem de execução deles

começo das atividades tentar concluir os requisitos semanalmente

estudos das tecnologias necessarias pro desenvolvimento do projeto



"""

class User:
    db_user = TinyDB(os.path.join(LOCAL_FOLDER, 'users_brain.json'))

    @staticmethod
    def get_user_details(session_id):
        # Procura o usuário baseado na sessão e retorna seus detalhes
        user = ...  # Código para encontrar o usuário com base na sessão
        if user:
            return {
                'email': user.email,
                'name': user.name,
                'phone': user.phone,
                # Adicione outros detalhes conforme necessário
            }
        return None



    @classmethod
    def login(cls, form):
        User = Query()
        users = db_user.all()
        for user in users:
            if 'session_id' not in user:
                print(f"Updating user: {user['email']}")
                db_user.update({'session_id': ''}, User.email == user['email'])
        try:
            user_data = json.loads(form.decode('utf-8'))
            email = user_data.get('email')
            password = user_data.get('password')

            if not email or not password:
                return "error"

            # Verifica se o usuário com o e-mail e senha fornecidos existe
            user = db_user.search((User.email == email) & (User.password == password))

            if user:
                session_id = str(uuid.uuid4())
                db_user.update({'session_id': session_id}, User.email == email)
                return session_id  # Retorna o session_id
            else:
                return "!ok"
        except Exception as e:
            print(f"Error in login method: {e}")
            return "error"

    @classmethod
    def is_valid_session(cls, session_id):
        User = Query()
        print(f"Checking session_id: {session_id}")  # Adicione isto para depuração
        user = cls.db_user.search(User.session_id == session_id)
        print(f"User found: {user}")  # Adicione isto para depuração
        return bool(user)

    @classmethod
    def create(cls, user):
        User = Query()
        _user = json.loads(user.decode('utf-8'))
        if not db_user.search(User.email == _user.get("email")):
            db_user.insert(_user)
            return "ok"
        return {"message": "error"}
        # if db_user:
        #     if not (db_user.search(User.email==_user.get("email")):
        #     db_user.insert(_user)
        #         print("Usuário cadastrado!")
        #
        #     else:
        #         print("Usuário já existente")

    @classmethod
    def load_users(cls):
        return db_user.all()

    def get_user_by_session(cls, session_id):
        User = Query()
        user = db_user.search(User.session_id == session_id)
        return user


class Article:
    @classmethod
    def load_articles(cls):
        return db.all()

    @classmethod
    def insert(cls, data):
        article = json.loads(data.decode('utf-8'))

        db.insert(article)

    @classmethod
    def update_status(cls, title, new_status):
        article_query = Query()
        articles = db.search(article_query.title == title)
        if articles:
            db.update({'status': new_status}, article_query.title == title)
            updated_article = db.search(article_query.title == title)[0]
            return updated_article
        return None

    @classmethod
    def delete(cls):
        pass

