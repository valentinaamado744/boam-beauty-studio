from datetime import datetime

import pytest


def _crear_reserva(page, nombre_cliente, fecha, hora):
    page.fill("#nombre_cliente", nombre_cliente)
    page.fill("#telefono", "3001234567")
    page.select_option("#servicio", label="Corte de Cabello")
    page.fill("#fecha", fecha)
    page.fill("#hora", hora)
    page.locator("form").get_by_role("button", name="Registrar Reserva").click()
    page.get_by_text(nombre_cliente).wait_for()


@pytest.mark.ui
def test_cp_003_ordenamiento_de_reservas(page, boam_base_url, screenshot_step):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    cliente_temprano = f"Cliente Temprano {timestamp}"
    cliente_tardio = f"Cliente Tardio {timestamp}"

    page.goto(boam_base_url)

    _crear_reserva(
        page=page,
        nombre_cliente=cliente_temprano,
        fecha="2026-06-20",
        hora="09:00",
    )
    screenshot_step("reserva_temprana_creada")

    _crear_reserva(
        page=page,
        nombre_cliente=cliente_tardio,
        fecha="2026-06-22",
        hora="16:00",
    )
    screenshot_step("reserva_tardia_creada")

    table_content = page.locator("table").inner_text()

    assert table_content.index(cliente_temprano) < table_content.index(cliente_tardio)
    screenshot_step("listado_ordenado")
