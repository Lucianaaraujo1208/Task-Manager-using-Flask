import pytest
from todo_project import app, db
from todo_project.models import User, Task

# test_sum.py

def test_sum():
    assert 1 + 2 == 3, "Soma de 1 + 2 deveria ser 3"