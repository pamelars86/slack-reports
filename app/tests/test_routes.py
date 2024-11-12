import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'API is up and running!' in rv.data

def test_fetch_messages(client, mocker):
    mocker.patch('app.tasks.fetch_messages_task.delay', return_value=mocker.Mock(id='1234567890abcdef'))
    rv = client.post('/fetch-messages', json={
        'channel_id': 'ABC123',
        'start_date': '2024-01-01',
        'end_date': '2024-01-31'
    })
    assert rv.status_code == 202
    assert rv.json['task_id'] == '1234567890abcdef'

def test_top_repliers(client, mocker):
    mocker.patch('app.tasks.calculate_top_repliers_task.delay', return_value=mocker.Mock(id='1234567890abcdef'))
    rv = client.post('/top-repliers', json={
        'channel_id': 'ABC123',
        'start_date': '2024-01-01',
        'end_date': '2024-01-31',
        'top_n': 10
    })
    assert rv.status_code == 202
    assert rv.json['task_id'] == '1234567890abcdef'