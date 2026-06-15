from datetime import datetime

import pytest


@pytest.mark.ui
def test_cp_001_crear_reserva(page, boam_base_url, screenshot_step):
    nombre_cliente = f"Cliente Playwright {datetime.now().strftime('%Y%m%d%H%M%S')}"

    page.goto(boam_base_url)
    screenshot_step("home_page")

    page.fill("#nombre_cliente", nombre_cliente)
    page.fill("#telefono", "3001234567")
    page.select_option("#servicio", label="Corte de Cabello")
    page.fill("#fecha", "2026-06-30")
    page.fill("#hora", "10:00")
    screenshot_step("formulario_completado")

    page.locator("form").get_by_role("button", name="Registrar Reserva").click()

    page.get_by_text(nombre_cliente).wait_for()
    assert page.get_by_text(nombre_cliente).is_visible()
    screenshot_step("reserva_creada")
