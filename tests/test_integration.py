import pytest
from todo_project import app, db
from todo_project.models import User

@pytest.fixture
def client():
    """Configura o cliente de teste e o banco de dados em memória."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_user_registration(client):
    """Teste simples para verificar a criação e recuperação de um novo usuário."""
    # Enviar dados para a rota de registro
    response = client.post('/register', data={
        'username': 'testuser',
        'password': 'testpassword',
        'confirm_password': 'testpassword'
    }, follow_redirects=True)

    # Verificar se a resposta é a esperada (por exemplo, redirecionamento para a página de login)
    assert response.status_code == 200
    assert b'Login' in response.data

    # Verificar se o usuário foi adicionado ao banco de dados
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'