import pytest

from app import app, reset_pagos


@pytest.fixture(autouse=True)
def limpiar_pagos():
    reset_pagos()
    yield
    reset_pagos()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_crear_pago_exitoso(client):
    r = client.post("/api/pagos", json={"monto": 25.5, "descripcion": "Suscripción"})
    assert r.status_code == 201
    body = r.get_json()
    assert body["estado"] == "completado"
    assert body["monto"] == 25.5
    assert body["descripcion"] == "Suscripción"
    assert "id" in body


def test_crear_pago_monto_invalido(client):
    r = client.post("/api/pagos", json={"monto": 0})
    assert r.status_code == 422
    assert r.get_json()["estado"] == "fallido"


def test_listar_pagos(client):
    client.post("/api/pagos", json={"monto": 10})
    client.post("/api/pagos", json={"monto": 5})
    r = client.get("/api/pagos")
    assert r.status_code == 200
    assert len(r.get_json()) == 2


def test_metricas(client):
    client.post("/api/pagos", json={"monto": 100})
    client.post("/api/pagos", json={"monto": 0})
    r = client.get("/api/metricas")
    assert r.status_code == 200
    m = r.get_json()
    assert m["total_pagos"] == 2
    assert m["pagos_completados"] == 1
    assert m["pagos_fallidos"] == 1
    assert m["volumen_completado"] == 100.0
    assert m["tasa_exito_porcentaje"] == 50.0


def test_index_html(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b"Plataforma de pagos" in r.data
