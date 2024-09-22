import unittest
from flask import Flask
from flask_login import LoginManager, login_user, logout_user
from todo_project import db
from todo_project.models import User
from todo_project.forms import UpdateUserPassword

class TestPasswordUpdate(unittest.TestCase):

    def setUp(self):
        # Configuração do aplicativo Flask com banco de dados SQLite na memória
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'test_secret_key'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Desabilitar CSRF para os testes
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        # Inicializar as extensões
        self.login_manager = LoginManager(self.app)
        db.init_app(self.app)

        # Criar o contexto do aplicativo
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Criar um usuário de teste
        self.user = User(username='testuser', password='oldpassword')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_update(self):
        # Simular login do usuário
        with self.app.test_request_context():
            login_user(self.user)

            # Preencher o formulário de alteração de senha
            form = UpdateUserPassword(old_password='oldpassword', new_password='newsecurepassword')

            # Verificar se o formulário é válido
            self.assertTrue(form.validate())

            # Simular o processo de atualização de senha
            self.user.password = form.new_password.data
            db.session.commit()

            # Verificar se a senha foi atualizada corretamente
            updated_user = User.query.filter_by(username='testuser').first()
            self.assertEqual(updated_user.password, 'newsecurepassword')

            # Logout do usuário
            logout_user()

if __name__ == '__main__':
    unittest.main()