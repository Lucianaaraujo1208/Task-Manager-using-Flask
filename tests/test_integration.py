# test_password_hashing.py

import pytest
from werkzeug.security import generate_password_hash, check_password_hash

def test_password_hashing():
    """Teste unitário simples para verificar a criptografia e verificação de senha"""
    password = 'testpassword'
    hashed_password = generate_password_hash(password)

    # Verifica se o hash da senha não é igual à senha em texto claro
    assert hashed_password != password

    # Verifica se a senha pode ser validada corretamente
    assert check_password_hash(hashed_password, password)
    assert not check_password_hash(hashed_password, 'wrongpassword')