import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

def test_register_new_user(client):
    """Teste de integração para registrar um novo usuário."""
    with app.app_context():
        # Verifica que o banco de dados inicialmente não tem nenhum usuário
        assert User.query.count() == 0

        # Simula um registro de usuário
        response = client.post('/register', data={
            'username': 'usuario_teste',
            'email': 'teste@teste.com',
            'password': 'senha123',
            'confirm_password': 'senha123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Account created' in response.data  # Verifica a mensagem de sucesso
        
        # Verifica que o usuário foi adicionado ao banco de dados
        assert User.query.count() == 1