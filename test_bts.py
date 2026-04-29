"""
Tests para los modelos BTS Integrantes, Álbumes y Tours.
Usa una base de datos SQLite en memoria para no tocar la BD de producción.
Ejecutar con: pytest test_bts.py -v
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from main import app
from db import get_session


#BD en memoria para tests

@pytest.fixture(name="session")
def session_fixture():
    """Crea una BD SQLite en memoria limpia para cada test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Cliente de prueba que usa la sesión en memoria."""

    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


#TESTS INTEGRANTES

def test_crea_integrante(client: TestClient):
    response = client.post("/integrantes", json={
        "nombre": "Jimin",
        "edad": 28,
        "altura": 1.74
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Jimin"
    assert data["edad"] == 28
    assert data["altura"] == 1.74
    assert "id" in data


def test_ver_integrantes(client: TestClient):
    # Crear dos integrantes
    client.post("/integrantes", json={"nombre": "V", "edad": 27, "altura": 1.79})
    client.post("/integrantes", json={"nombre": "Jungkook", "edad": 26, "altura": 1.79})

    response = client.get("/integrantes")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_buscar_integrante_nombre(client: TestClient):
    client.post("/integrantes", json={"nombre": "RM", "edad": 29, "altura": 1.81})

    response = client.get("/integrantes/buscar/RM")
    assert response.status_code == 200
    assert response.json()[0]["nombre"] == "RM"


def test_buscar_integrante_nombre_no_existe(client: TestClient):
    response = client.get("/integrantes/buscar/Shakira")
    assert response.status_code == 404


def test_crea_integrante_altura_invalida(client: TestClient):
    response = client.post("/integrantes", json={
        "nombre": "Jin",
        "edad": 30,
        "altura": 10.0  # Altura imposible
    })
    assert response.status_code == 422

    #TESTS ÁLBUMES

    def test_crea_album(client: TestClient):
        response = client.post("/albumes", json={"nombre": "Map of the Soul: 7", "num_canciones": 20})
        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "Map of the Soul: 7"
        assert data["num_canciones"] == 20
        assert "id" in data

    def test_ver_albumes_vacio(client: TestClient):
        response = client.get("/albumes")
        assert response.status_code == 200
        assert response.json() == []

    def test_crea_y_ver_album(client: TestClient):
        client.post("/albumes", json={"nombre": "BE", "num_canciones": 8})

        response = client.get("/albumes")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["nombre"] == "BE"

    def test_buscar_album_id(client: TestClient):
        creado = client.post("/albumes", json={"nombre": "Butter", "num_canciones": 1}).json()

        response = client.get(f"/albumes/{creado['id']}")
        assert response.status_code == 200
        assert response.json()["nombre"] == "Butter"

    def test_buscar_album_id_no_existe(client: TestClient):
        response = client.get("/albumes/999")
        assert response.status_code == 404

    def test_editar_album(client: TestClient):
        creado = client.post("/albumes", json={"nombre": "Love Yourself: Her", "num_canciones": 9}).json()

        response = client.patch(f"/albumes/{creado['id']}", json={"num_canciones": 10})
        assert response.status_code == 200
        assert response.json()["num_canciones"] == 10

    def test_editar_album_no_existe(client: TestClient):
        response = client.patch("/albumes/999", json={"nombre": "Fantasma"})
        assert response.status_code == 404


# TESTS TOURS

def test_crea_tour(client: TestClient):
    response = client.post("/tours", json={
        "nombre": "Love Yourself World Tour",
        "ciudades_visitadas": "Seúl, Los Ángeles, Londres"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Love Yourself World Tour"
    assert "id" in data


def test_ver_tours_vacio(client: TestClient):
    response = client.get("/tours")
    assert response.status_code == 200
    assert response.json() == []


def test_crea_y_ver_tour(client: TestClient):
    client.post("/tours", json={
        "nombre": "Love Yourself World Tour",
        "ciudades_visitadas": "Seúl, Los Ángeles, Londres"
    })
    response = client.get("/tours")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_buscar_tours_en_ciudad(client: TestClient):
    client.post("/tours", json={
        "nombre": "Map of the Soul Tour",
        "ciudades_visitadas": "Berlín, Tokio, Buenos Aires"
    })
    response = client.get("/tours/buscar/Tokio")
    assert response.status_code == 200
    assert "Tokio" in response.json()[0]["ciudades_visitadas"]


def test_buscar_tours_ciudad_no_existe(client: TestClient):
    response = client.get("/tours/buscar/Marte")
    assert response.status_code == 404


def test_cancelar_tour(client: TestClient):
    creado = client.post("/tours", json={
        "nombre": "Yet to Come Concert",
        "ciudades_visitadas": "Busan"
    }).json()

    response = client.delete(f"/tours/{creado['id']}")
    assert response.status_code == 200
    assert response.json()["nombre"] == "Yet to Come Concert"

    # Verificar que ya no existe
    response2 = client.get("/tours")
    assert all(t["id"] != creado["id"] for t in response2.json())


def test_cancelar_tour_no_existe(client: TestClient):
    response = client.delete("/tours/999")
    assert response.status_code == 404
