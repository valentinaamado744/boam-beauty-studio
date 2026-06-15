from datetime import datetime

import pytest


def _assert_active_element_is_invalid(page):
    is_invalid = page.evaluate("document.activeElement.checkValidity() === false")
    assert is_invalid


def _submit_form(page):
    page.locator("form").get_by_role("button", name="Registrar Reserva").click()


def _fill_required_fields(
    page,
    nombre_cliente="Cliente Validacion",
    telefono="3001234567",
    servicio="Corte de Cabello",
    fecha="2026-06-30",
    hora="10:00",
):
    if nombre_cliente is not None:
        page.fill("#nombre_cliente", nombre_cliente)
    if telefono is not None:
        page.fill("#telefono", telefono)
    if servicio is not None:
        page.select_option("#servicio", label=servicio)
    if fecha is not None:
        page.fill("#fecha", fecha)
    if hora is not None:
        page.fill("#hora", hora)


@pytest.mark.ui
def test_neg_001_validacion_html5_campos_obligatorios(
    page,
    boam_base_url,
    screenshot_step,
):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    page.goto(boam_base_url)
    _fill_required_fields(
        page,
        nombre_cliente="",
        telefono="3001234567",
        servicio="Corte de Cabello",
        fecha="2026-06-30",
        hora="10:00",
    )
    _submit_form(page)
    _assert_active_element_is_invalid(page)
    screenshot_step("nombre_requerido")

    page.goto(boam_base_url)
    _fill_required_fields(
        page,
        nombre_cliente=f"Cliente Telefono {timestamp}",
        telefono="",
        servicio="Corte de Cabello",
        fecha="2026-06-30",
        hora="10:00",
    )
    _submit_form(page)
    _assert_active_element_is_invalid(page)
    screenshot_step("telefono_requerido")

    page.goto(boam_base_url)
    _fill_required_fields(
        page,
        nombre_cliente=f"Cliente Servicio {timestamp}",
        telefono="3001234567",
        servicio=None,
        fecha="2026-06-30",
        hora="10:00",
    )
    _submit_form(page)
    _assert_active_element_is_invalid(page)
    screenshot_step("servicio_requerido")

    page.goto(boam_base_url)
    _fill_required_fields(
        page,
        nombre_cliente=f"Cliente Fecha {timestamp}",
        telefono="3001234567",
        servicio="Corte de Cabello",
        fecha="",
        hora="10:00",
    )
    _submit_form(page)
    _assert_active_element_is_invalid(page)
    screenshot_step("fecha_requerida")

    page.goto(boam_base_url)
    _fill_required_fields(
        page,
        nombre_cliente=f"Cliente Hora {timestamp}",
        telefono="3001234567",
        servicio="Corte de Cabello",
        fecha="2026-06-30",
        hora="",
    )
    _submit_form(page)
    _assert_active_element_is_invalid(page)
    screenshot_step("hora_requerida")
