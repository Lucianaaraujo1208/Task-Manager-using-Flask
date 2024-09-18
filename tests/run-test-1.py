import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task

# run-test-1

def test_about_page(client):
    """Teste para verificar se a página 'about' carrega corretamente."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data  # Verifica se o conteúdo esperado está presente