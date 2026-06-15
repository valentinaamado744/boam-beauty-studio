from datetime import datetime

import pytest


@pytest.mark.ui
def test_cp_002_eliminar_reserva(page, boam_base_url, screenshot_step):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_cliente = f"Cliente Eliminar {timestamp}"

    page.goto(boam_base_url)

    page.fill("#nombre_cliente", nombre_cliente)
    page.fill("#telefono", "3001234567")
    page.select_option("#servicio", label="Corte de Cabello")
    page.fill("#fecha", "2026-06-30")
    page.fill("#hora", "10:00")
    page.locator("form").get_by_role("button", name="Registrar Reserva").click()

    page.get_by_text(nombre_cliente).wait_for()
    screenshot_step("reserva_existente")

    reservation_row = page.locator("tr").filter(has_text=nombre_cliente)
    page.once("dialog", lambda dialog: dialog.accept())
    reservation_row.get_by_role("link", name="Eliminar").click()
    screenshot_step("click_eliminar")

    page.get_by_text(nombre_cliente).wait_for(state="hidden")
    assert page.get_by_text(nombre_cliente).count() == 0
    screenshot_step("reserva_eliminada")
