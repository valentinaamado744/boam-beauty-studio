import pytest

import app as app_module


def test_test_database_is_isolated(app, test_db_path):
    assert app_module.DATABASE == str(test_db_path)
    assert test_db_path.exists()
    assert test_db_path.name == "boam_test.db"


def test_crear_base_datos_creates_reservas_table(db_connection):
    table = db_connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'reservas'
        """
    ).fetchone()

    assert table is not None


def test_index_returns_empty_reservations_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"No hay reservas registradas" in response.data


def test_add_reservation_persists_data(client, db_connection, sample_reservation):
    response = client.post("/agregar", data=sample_reservation, follow_redirects=True)

    assert response.status_code == 200

    reservation = db_connection.execute(
        "SELECT * FROM reservas WHERE nombre_cliente = ?",
        (sample_reservation["nombre_cliente"],),
    ).fetchone()

    assert reservation is not None
    assert reservation["telefono"] == sample_reservation["telefono"]
    assert reservation["servicio"] == sample_reservation["servicio"]
    assert reservation["fecha"] == sample_reservation["fecha"]
    assert reservation["hora"] == sample_reservation["hora"]
    assert sample_reservation["nombre_cliente"].encode() in response.data


def test_index_orders_reservations_by_date_and_time(client, create_reservation):
    create_reservation(nombre_cliente="Reserva Tarde", fecha="2026-06-22", hora="16:00")
    create_reservation(nombre_cliente="Reserva Temprana", fecha="2026-06-20", hora="09:00")

    response = client.get("/")
    body = response.data.decode()

    assert response.status_code == 200
    assert body.index("Reserva Temprana") < body.index("Reserva Tarde")


def test_delete_reservation_removes_data(client, db_connection, create_reservation):
    reservation_id = create_reservation(nombre_cliente="Reserva a eliminar")

    response = client.get(f"/eliminar/{reservation_id}", follow_redirects=True)

    assert response.status_code == 200

    reservation = db_connection.execute(
        "SELECT * FROM reservas WHERE id = ?",
        (reservation_id,),
    ).fetchone()

    assert reservation is None


@pytest.mark.parametrize(
    "invalid_field",
    [
        "nombre_cliente",
        "telefono",
        "fecha",
        "hora",
    ],
)
@pytest.mark.xfail(
    reason=(
        "La aplicacion actualmente no valida campos vacios en el servidor; "
        "SQLite permite strings vacios en columnas TEXT NOT NULL."
    )
)
def test_add_reservation_with_empty_required_field_is_not_stored(
    client,
    db_connection,
    sample_reservation,
    invalid_field,
):
    invalid_reservation = sample_reservation.copy()
    invalid_reservation[invalid_field] = ""

    response = client.post(
        "/agregar",
        data=invalid_reservation,
        follow_redirects=True,
    )

    stored_reservations = db_connection.execute(
        "SELECT COUNT(*) AS total FROM reservas"
    ).fetchone()

    assert response.status_code == 200
    assert stored_reservations["total"] == 0
