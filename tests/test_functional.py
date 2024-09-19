import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

def test_login_user(client):
    """Teste funcional para verificar o login de um usuário."""
    with app.app_context():
        # Cria um usuário para teste
        user = User(username='usuario_teste', email='teste@teste.com')
        user.set_password('senha123')
        db.session.add(user)
        db.session.commit()

        # Simula o login
        response = client.post('/login', data={
            'email': 'teste@teste.com',
            'password': 'senha123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Login successful' in response.data  # Verifica a mensagem de sucesso