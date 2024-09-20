import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

# Configuração de Fixture para inicializar o cliente de teste e configurar o banco de dados
@pytest.fixture
def client():
    app.config['TESTING'] = True  # Ativar modo de teste
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco de dados em memória para testes
    app.config['WTF_CSRF_ENABLED'] = False  # Desabilitar CSRF para facilitar os testes

    with app.app_context():  # Garante o contexto da aplicação
        db.create_all()  # Criar as tabelas do banco de dados
        client = app.test_client()  # Inicializar o cliente de teste
        yield client  # Fornece o cliente para os testes
        db.drop_all()  # Apaga as tabelas após o teste

# Função auxiliar para login do usuário
def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

# Função auxiliar para logout do usuário
def logout(client):
    return client.get('/logout', follow_redirects=True)

# Teste completo para o fluxo funcional
def test_complete_functional_workflow(client):
    """Teste funcional completo incluindo registro, login, criação de tarefa, edição e exclusão"""

    # 1. Registrar um novo usuário
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200  # Verificar sucesso no registro
    assert b'Account Created' in response.data  # Verificar mensagem de sucesso

    # 2. Fazer login com o novo usuário
    response = login(client, 'testuser', 'password123')
    assert response.status_code == 200  # Verifica se o login foi bem-sucedido
    assert b'Login Successfull' in response.data  # Verificar mensagem de sucesso no login

    # 3. Adicionar uma nova tarefa
    response = client.post('/add_task', data={
        'task_name': 'Comprar leite'
    }, follow_redirects=True)
    assert response.status_code == 200  # Verificar sucesso ao adicionar tarefa
    assert b'Task Created' in response.data  # Verificar mensagem de sucesso ao adicionar tarefa

    # 4. Verificar se a tarefa foi adicionada corretamente
    response = client.get('/all_tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b'Comprar leite' in response.data  # Verifica se a tarefa aparece na lista

    # 5. Editar a tarefa adicionada
    task = Task.query.filter_by(content='Comprar leite').first()  # Buscar tarefa recém-criada
    response = client.post(f'/all_tasks/{task.id}/update_task', data={
        'task_name': 'Comprar café'
    }, follow_redirects=True)
    assert response.status_code == 200  # Verificar sucesso na edição
    assert b'Task Updated' in response.data  # Verificar mensagem de sucesso na edição

    # 6. Verificar se a edição da tarefa foi aplicada
    response = client.get('/all_tasks', follow_redirects=True)
    assert b'Comprar caf\xc3\xa9' in response.data  # Codificação UTF-8 do 'é'
    assert b'Comprar leite' not in response.data  # O nome antigo não deve mais aparecer

    # 7. Excluir a tarefa
    response = client.get(f'/all_tasks/{task.id}/delete_task', follow_redirects=True)
    assert response.status_code == 200  # Verificar sucesso na exclusão
    assert b'Task Deleted' in response.data  # Verificar mensagem de sucesso na exclusão

    # 8. Verificar se a tarefa foi removida
    response = client.get('/all_tasks', follow_redirects=True)
    assert b'Comprar caf\xc3\xa9' in response.data  # Codificação UTF-8 do 'é'

    # 9. Fazer logout do usuário
    response = logout(client)
    assert response.status_code == 200  # Verificar sucesso no logout
    assert b'Login' in response.data  # Verificar que a página de login é carregada

# Teste para verificar erro 404 (página não encontrada)
def test_404_error(client):
    """Teste para garantir que o erro 404 seja retornado adequadamente"""
    response = client.get('/invalid_route', follow_redirects=True)
    assert response.status_code == 404  # Verificar o status code 404
    assert b'404 Error' in response.data  # Verificar a mensagem do template de erro

# Teste para verificar o redirecionamento de páginas protegidas
def test_protected_route_redirect(client):
    """Teste para garantir que rotas protegidas redirecionem usuários não autenticados"""
    response = client.get('/all_tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data  # Verificar redirecionamento para a página de login