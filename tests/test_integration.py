import pytest
from todo_project import app, db
from todo_project.models import User

@pytest.fixture
def client():
    """Configurar o cliente de teste e o banco de dados em memória."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_user_creation(client):
    """Teste para verificar a criação e leitura de um usuário."""
    # Criar um usuário diretamente no banco de dados
    user = User(username='testuser', password='testpassword')
    db.session.add(user)
    db.session.commit()

    # Recupera o usuário do banco de dados
    retrieved_user = User.query.filter_by(username='testuser').first()

    # Verifica se o usuário foi criado e recuperado corretamente
    assert retrieved_user is not None
    assert retrieved_user.username == 'testuser'