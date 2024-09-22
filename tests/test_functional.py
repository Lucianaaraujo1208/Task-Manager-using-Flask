import pytest
from todo_project import app, db

@pytest.fixture
def setup_app():
    """Configura o ambiente de teste do Flask"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados em memória
    app.config['WTF_CSRF_ENABLED'] = False  # Desativa CSRF para testes de formulário

    with app.app_context():
        db.create_all()  # Inicializa o banco de dados
        yield app.test_client()  # Fornece o cliente de teste
        db.drop_all()  # Limpa o banco de dados após o teste

def test_user_registration_login_and_task_creation(setup_app):
    """Teste funcional: registro, login e criação de tarefa"""

    client = setup_app

    # Passo 1: Registrar novo usuário
    registration_response = client.post('/register', data={
        'username': 'user_teste',
        'password': 'TesteSenha123',
        'confirm_password': 'TesteSenha123'
    }, follow_redirects=True)
    
    assert registration_response.status_code == 200  # Verifica se o registro foi bem-sucedido
    assert b'Login' in registration_response.data  # Verifica se foi redirecionado para a página de login

    # Passo 2: Realizar login com o novo usuário
    login_response = client.post('/login', data={
        'username': 'user_teste',
        'password': 'TesteSenha123'
    }, follow_redirects=True)
    
    assert login_response.status_code == 200  # Verifica se o login foi bem-sucedido
    assert b'All Tasks' in login_response.data  # Verifica se a página de tarefas foi carregada

    # Passo 3: Criar uma nova tarefa
    create_task_response = client.post('/add_task', data={
        'task_name': 'Ler um livro'
    }, follow_redirects=True)
    
    assert create_task_response.status_code == 200  # Verifica se a criação da tarefa foi bem-sucedida
    assert b'Ler um livro' in create_task_response.data  # Verifica se a tarefa foi adicionada corretamente

    # Passo 4: Checar se a tarefa aparece na lista de tarefas
    task_list_response = client.get('/all_tasks', follow_redirects=True)
    
    assert task_list_response.status_code == 200  # Verifica se a página de tarefas foi carregada
    assert b'Ler um livro' in task_list_response.data  # Verifica se a tarefa criada está na lista
