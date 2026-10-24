import payment_store
from app import app


def setup_function():
    payment_store.clear_payments()


def test_health():
    client = app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json()['status'] == 'ok'


def test_crear_pago_y_metricas():
    client = app.test_client()
    resp = client.post('/pagos', json={'monto': 10.5, 'concepto': 'Test', 'cliente': 'Cliente A'})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body['estado'] == 'completado'
    assert body['monto'] == 10.5

    metrics = client.get('/metricas').get_json()
    assert metrics['total_pagos'] == 1
    assert metrics['monto_total'] == 10.5

    pagos = client.get('/pagos').get_json()
    assert len(pagos) == 1
    assert pagos[0]['concepto'] == 'Test'


def test_pago_invalido():
    client = app.test_client()
    assert client.post('/pagos', json={'concepto': 'x'}).status_code == 400
    assert client.post('/pagos', json={'monto': -1, 'concepto': 'x'}).status_code == 400
    assert client.post('/pagos', json={'monto': 'abc', 'concepto': 'x'}).status_code == 400


def test_index():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Plataforma de pagos' in resp.data
