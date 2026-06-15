# Pruebas UI BOAM con Playwright

## Estructura

```text
tests_ui/
|-- conftest.py
|-- README.md
`-- evidencias/
    `-- .gitkeep
```

## Uso esperado en los tests

```python
import pytest


@pytest.mark.ui
def test_flujo_reserva(page, boam_base_url, screenshot_step):
    page.goto(boam_base_url)
    screenshot_step("pagina_inicial")

    page.fill("#nombre_cliente", "Cliente UI")
    screenshot_step("cliente_ingresado")
```

Cada llamada a `screenshot_step("nombre_descriptivo")` genera un PNG en
`tests_ui/evidencias` con nombre descriptivo, numero de paso y timestamp.

Ademas, al finalizar cada prueba se genera automaticamente un screenshot con
estado `passed` o `failed`.

## Ejecucion

```powershell
pytest -c pytest-ui.ini
```
