import os
os.environ['MYSQL_USER'] = 'root'
os.environ['MYSQL_PASSWD'] = 'mypass'
os.environ['MYSQL_HOST'] = 'mariadbtest'
#os.environ['MYSQL_HOST'] = '127.0.0.1'
import pytest
from web import app

def test_healthcheck():
    response = app.test_client().get('/healthcheck')
    assert response.status_code == 200
    assert response.data == b'{"status": "Healthy"}'

def test_createUser():
    payload = "{\n\"id\":223446,\"firstName\":\"Herman\",\"lastName\":\"Chen\",\"nationality\":\"Singapore\"\n}"
    headers = {'Content-Type': 'application/json'}
    response = app.test_client().post('/', headers=headers, data = payload)
    print(response.data)
    assert response.status_code == 200
    assert response.data == b'{"id": 223446, "firstName": "Herman", "lastName": "Chen", "nationality": "Singapore"}'

def test_getStudent():
    payload = "{\n\"id\":223446\n}"
    headers = {'Content-Type': 'application/json'}
    response = app.test_client().get('/', headers=headers, data = payload)
    assert response.status_code == 200
    assert response.data == b'{"id": 223446, "firstName": "Herman", "lastName": "Chen", "nationality": "Singapore"}'

def test_updateStudent():
    payload = "{\n\"id\":223446,\"lastName\":\"Chan\"\n}"
    headers = {'Content-Type': 'application/json'}
    response = app.test_client().put('/', headers=headers, data = payload)
    assert response.status_code == 200
    assert response.data == b'{"id": 223446, "firstName": "Herman", "lastName": "Chan", "nationality": "Singapore"}'

def test_deleteStudent():
    payload = "{\n\"id\":223446\n}"
    headers = {'Content-Type': 'application/json'}
    response = app.test_client().delete('/', headers=headers, data = payload)
    assert response.status_code == 200
    assert response.data == b'{"status": "User removed"}'

def test_getStudent():
    payload = "{\n\"id\":223446\n}"
    headers = {'Content-Type': 'application/json'}
    response = app.test_client().get('/', headers=headers, data = payload)
    assert response.status_code == 404
    assert response.data == b'{"status": "Not Found"}'
