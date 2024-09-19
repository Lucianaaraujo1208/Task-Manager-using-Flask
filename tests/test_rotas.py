import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

@pytest.fixture
def client():
    """Configura o cliente de teste e o banco de dados temporário."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()  # Cria todas as tabelas no banco de dados em memória
        yield client  # Retorna o cliente de teste para os testes utilizarem
        db.drop_all()  # Remove todas as tabelas após os testes

### Testando as rotas principais

def test_about_page(client):
    """Teste para verificar se a página 'about' carrega corretamente."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data  # Verifica se o texto 'About' está presente na resposta

def test_home_page(client):
    """Teste simples para verificar se a página inicial carrega corretamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'About' in response.data  # Verifica se o texto 'About' está na página

def test_login_page(client):
    """Teste para verificar se a página de login carrega corretamente."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data  # Verifica se o texto 'Login' está presente na página

def test_register_page(client):
    """Teste para verificar se a página de registro carrega corretamente."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data  # Verifica se o texto 'Register' está presente na página

def test_all_tasks_page_redirects_when_not_logged_in(client):
    """Teste para verificar se a página 'all_tasks' redireciona quando o usuário não está logado."""
    response = client.get('/all_tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data  # Verifica se a mensagem 'Please log in' aparece na resposta