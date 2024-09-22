import pytest
from todo_project import app, db

@pytest.fixture
def client():
    # Configurações de teste do Flask
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados em memória para testes
    app.config['WTF_CSRF_ENABLED'] = False  # Desabilitar CSRF para facilitar testes de formulário

    with app.app_context():
        db.create_all()  # Criar tabelas no banco de dados de teste
        client = app.test_client()  # Cria um cliente de teste para simular requisições HTTP
        yield client
        db.drop_all()  # Limpar o banco de dados após cada teste

def test_functional_workflow(client):
    """Teste funcional para registro, login e criação de tarefa"""

    # Passo 1: Registrar novo usuário
    response = client.post('/register', data={
        'username': 'functionaluser',
        'password': 'Func@1234',
        'confirm_password': 'Func@1234'
    }, follow_redirects=True)
    assert response.status_code == 200  # Verifica se a resposta foi bem-sucedida
    assert b'Login' in response.data  # Verifica se a página de login aparece após registro

    # Passo 2: Realizar login com o novo usuário
    response = client.post('/login', data={
        'username': 'functionaluser',
        'password': 'Func@1234'
    }, follow_redirects=True)
    assert response.status_code == 200  # Verifica se a resposta foi bem-sucedida
    assert b'All Tasks' in response.data  # Verifica se a página de tarefas aparece após o login

    # Passo 3: Criar uma nova tarefa
    response = client.post('/add_task', data={
        'task_name': 'Comprar leite'
    }, follow_redirects=True)
    assert response.status_code == 200  # Verifica se a resposta foi bem-sucedida

    # Passo 4: Checar se a tarefa aparece na lista de tarefas
    response = client.get('/all_tasks', follow_redirects=True)  # Seguir redirecionamentos
    assert response.status_code == 200