import pytest
from todo_project import app, db
from todo_project.models import User, Task

@pytest.fixture
def client():
    """Configura o ambiente de teste com um banco de dados em memória."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

### Testando rotas principais

def test_about_page(client):
    """Teste para verificar se a página 'about' carrega corretamente."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data

def test_home_page(client):
    """Teste para verificar se a página inicial carrega corretamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data  # Verifique o texto correto para a página inicial

def test_login_page(client):
    """Teste para verificar se a página de login carrega corretamente."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_register_page(client):
    """Teste para verificar se a página de registro carrega corretamente."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_all_tasks_page_redirects_when_not_logged_in(client):
    """Teste para verificar se a página 'all_tasks' redireciona quando o usuário não está logado."""
    response = client.get('/all_tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data  # Verifique a mensagem correta de login

### Testando funcionalidades de autenticação

def test_user_registration(client):
    """Teste para verificar o registro de um novo usuário."""
    response = client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome testuser' in response.data  # Verifique a mensagem de boas-vindas ou similar

def test_user_login(client):
    """Teste para verificar o login de um usuário existente."""
    # Primeiro, registre um usuário
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    
    # Então, faça o login com o usuário registrado
    response = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data  # Verifique a mensagem de login bem-sucedido ou similar

def test_add_task(client):
    """Teste para adicionar uma nova tarefa."""
    # Primeiro, registre e faça login com um usuário
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    
    # Adicione uma nova tarefa
    response = client.post('/add_task', data=dict(
        title='Test Task',
        description='This is a test task.'
    ), follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Task added successfully' in response.data  # Verifique a mensagem de tarefa adicionada ou similar

def test_view_tasks(client):
    """Teste para visualizar as tarefas adicionadas."""
    # Primeiro, registre e faça login com um usuário
    client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    
    # Adicione uma nova tarefa
    client.post('/add_task', data=dict(
        title='Test Task',
        description='This is a test task.'
    ), follow_redirects=True)
    
    # Visualize as tarefas
    response = client.get('/all_tasks')
    assert response.status_code == 200
    assert b'Test Task' in response.data  # Verifique se a tarefa adicionada está na página de tarefas
