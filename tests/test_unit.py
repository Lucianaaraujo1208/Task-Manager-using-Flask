import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

def test_user_password_hashing():
    """Teste unitário para verificar o hashing da senha de um usuário."""
    user = User(username='teste', email='teste@teste.com')
    user.set_password('senha123')
    
    assert user.password_hash is not None  # Verifica se o hash da senha foi gerado
    assert user.check_password('senha123')  # Verifica se a senha é validada corretamente
    assert not user.check_password('senhaerrada')  # Verifica se uma senha incorreta não passa