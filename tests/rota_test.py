import pytest
from todo_project import app, db
from todo_project.models import User, Task

def test_all_tasks_page_redirects_when_not_logged_in(client):
    response = client.get('/all_tasks', follow_redirects=True)
    assert response.status_code == 200
    assert b'Please log in' in response.data