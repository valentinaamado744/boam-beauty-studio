# Entorno de pruebas BOAM

## Estructura recomendada

```text
BOAM/
|-- app.py
|-- boam.db
|-- pytest.ini
|-- requirements.txt
|-- static/
|-- templates/
`-- tests/
    |-- conftest.py
    |-- test_app.py
    `-- README.md
```

## Base de datos de pruebas

Las pruebas no usan `boam.db`. La fixture `app` reemplaza `app.DATABASE` con un archivo SQLite temporal llamado `boam_test.db`, creado dentro de `tmp_path` por Pytest para cada prueba. Esto mantiene aislados los datos de produccion y evita que una prueba contamine a otra.

## Fixtures principales

- `app`: configura Flask en modo `TESTING`, cambia la ruta de SQLite y crea el esquema.
- `client`: expone el cliente HTTP de Flask para probar rutas sin levantar servidor.
- `db_connection`: abre una conexion SQLite a la base temporal de la prueba.
- `sample_reservation`: entrega datos validos para crear una reserva.
- `create_reservation`: inserta reservas directamente para preparar escenarios.

## Instalacion

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecucion

```powershell
pytest
pytest -v
pytest --cov=app --cov-report=term-missing
```

## Buenas practicas aplicadas

- Pruebas separadas de la aplicacion principal.
- SQLite temporal por prueba.
- Fixtures reutilizables y pequenas.
- Cliente de Flask en memoria, sin servidor real.
- Cobertura configurada desde `pytest.ini`.
