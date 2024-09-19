# test_integration.py

import pytest
from todo_project import app, db
from todo_project.models import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_user_registration(client):
    """Teste de integração para verificar o registro e a criação de um novo usuário"""
    # Enviar dados para a rota de registro
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpassword',
        'confirm_password': 'newpassword'
    }, follow_redirects=True)

    # Verificar se a resposta é a esperada
    assert response.status_code == 200
    assert b'Login' in response.data

    # Verificar se o usuário foi adicionado ao banco de dados
    user = User.query.filter_by(username='newuser').first()
    assert user is not None
    assert user.check_password('newpassword')