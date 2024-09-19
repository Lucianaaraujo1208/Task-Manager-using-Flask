# test_routes.py

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

def test_about_page(client):
    """Teste funcional para verificar se a página 'About' carrega corretamente."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_home_page(client):
    """Teste funcional para verificar se a página inicial carrega corretamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'About' in response.data

def test_login_page(client):
    """Teste funcional para verificar se a página de login carrega corretamente."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_page(client):
    """Teste funcional para verificar se a página de registro carrega corretamente."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_all_tasks_page_redirects_when_not_logged_in(client):
    """Teste funcional para verificar se a página de tarefas redireciona quando o usuário não está logado."""
    response = client.get('/all_tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data