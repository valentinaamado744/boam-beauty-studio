# BOAM Beauty Studio

Aplicación web desarrollada con Flask para la gestión de reservas de un estudio de belleza.

## Tecnologías utilizadas

* Python 3.14
* Flask
* SQLite
* Bootstrap
* Pytest
* Playwright

---

# Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/valentinaamado744/boam-beauty-studio.git
cd boam-beauty-studio
```

## 2. Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash
python -m venv venv
source venv/bin/activate
```

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Instalar navegadores Playwright

```bash
python -m playwright install
```

---

# Ejecución de la aplicación

```bash
python app.py
```

La aplicación estará disponible en:

http://127.0.0.1:5000

---

# Ejecución de pruebas Backend

Ejecutar todas las pruebas:

```bash
python -m pytest -v
```

Ejecutar con cobertura:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

# Ejecución de pruebas Frontend

Asegurarse de que la aplicación Flask esté en ejecución.

Ejecutar todas las pruebas UI:

```bash
python -m pytest -c pytest-ui.ini tests_ui -v
```

Ejecutar un caso específico:

```bash
python -m pytest -c pytest-ui.ini tests_ui/test_crear_reserva.py -v
```

---

# Evidencias automáticas

Las pruebas Playwright generan automáticamente:

* Capturas de pantalla paso a paso.
* Captura final del resultado.
* Archivo evidencia.md.
* Carpeta independiente por ejecución.

Ubicación:

```text
tests_ui/evidencias/
```

---

# Resultados obtenidos

## Backend

* 6 pruebas PASSED
* 4 pruebas XFAILED
* Cobertura: 95%

## Frontend

* CP-001 Crear reserva
* CP-002 Eliminar reserva
* CP-003 Ordenamiento de reservas
* NEG-001 Validación HTML5

Todos los casos ejecutados satisfactoriamente.

---

# Autor

Valentina Amado
