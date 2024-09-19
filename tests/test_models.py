import pytest
from todo_project import app, db
from todo_project.models import User, Task

def test_password_hashing():
    """Teste unitário para verificar a criptografia e verificação de senha"""
    user = User(username='testuser', password='testpassword')
    
    # Verificar se a senha é criptografada
    assert user.password != 'testpassword'
    
    # Verificar se a senha pode ser verificada corretamente
    assert user.check_password('testpassword')
    assert not user.check_password('wrongpassword')