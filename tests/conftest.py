import sqlite3

import pytest

import app as app_module


@pytest.fixture()
def test_db_path(tmp_path):
    return tmp_path / "boam_test.db"


@pytest.fixture()
def app(test_db_path, monkeypatch):
    monkeypatch.setattr(app_module, "DATABASE", str(test_db_path))
    app_module.app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
    )
    app_module.crear_base_datos()

    yield app_module.app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db_connection(app, test_db_path):
    connection = sqlite3.connect(test_db_path)
    connection.row_factory = sqlite3.Row
    yield connection
    connection.close()


@pytest.fixture()
def sample_reservation():
    return {
        "nombre_cliente": "Valentina Perez",
        "telefono": "3001234567",
        "servicio": "Corte de Cabello",
        "fecha": "2026-06-20",
        "hora": "10:30",
    }


@pytest.fixture()
def create_reservation(db_connection):
    def _create_reservation(**overrides):
        data = {
            "nombre_cliente": "Cliente QA",
            "telefono": "3010000000",
            "servicio": "Manicure",
            "fecha": "2026-06-21",
            "hora": "14:00",
        }
        data.update(overrides)

        cursor = db_connection.execute(
            """
            INSERT INTO reservas (
                nombre_cliente,
                telefono,
                servicio,
                fecha,
                hora
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                data["nombre_cliente"],
                data["telefono"],
                data["servicio"],
                data["fecha"],
                data["hora"],
            ),
        )
        db_connection.commit()
        return cursor.lastrowid

    return _create_reservation
