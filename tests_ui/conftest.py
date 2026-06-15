from datetime import datetime
from pathlib import Path
import re

import pytest


BASE_URL = "http://127.0.0.1:5000"
EVIDENCE_DIR = Path(__file__).parent / "evidencias"


def _safe_name(value):
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value.strip().lower())
    return value.strip("_") or "screenshot"


@pytest.fixture(scope="session", autouse=True)
def ensure_evidence_dir():
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1366,
            "height": 768,
        },
        "record_video_dir": None,
    }


@pytest.fixture()
def boam_base_url():
    return BASE_URL


@pytest.fixture()
def evidence_test_dir(request):
    test_name = _safe_name(request.node.name)
    execution_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = EVIDENCE_DIR / test_name / execution_timestamp
    path.mkdir(parents=True, exist_ok=True)
    return path


@pytest.fixture()
def screenshot_step(page, request, evidence_test_dir):
    test_name = _safe_name(request.node.name)
    step_counter = {"value": 0}
    screenshots = getattr(request.node, "screenshots", [])
    setattr(request.node, "screenshots", screenshots)

    def _capture(step_name, full_page=True):
        step_counter["value"] += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = (
            f"{test_name}_"
            f"paso_{step_counter['value']:02d}_"
            f"{_safe_name(step_name)}_"
            f"{timestamp}.png"
        )
        path = evidence_test_dir / file_name
        page.screenshot(path=str(path), full_page=full_page)
        screenshots.append(file_name)
        return path

    return _capture


@pytest.fixture(autouse=True)
def automatic_screenshots(page, request, evidence_test_dir):
    test_name = _safe_name(request.node.name)
    start_datetime = datetime.now()
    start_timestamp = start_datetime.strftime("%Y%m%d_%H%M%S")
    screenshots = getattr(request.node, "screenshots", [])
    setattr(request.node, "screenshots", screenshots)

    yield

    status = "passed"
    report = getattr(request.node, "rep_call", None)
    if report:
        if getattr(report, "wasxfail", None):
            status = "xfailed"
        elif report.failed:
            status = "failed"

    file_name = f"{test_name}_resultado_{status}_{start_timestamp}.png"
    page.screenshot(path=str(evidence_test_dir / file_name), full_page=True)
    screenshots.append(file_name)

    evidence = [
        f"# Evidencia: {request.node.name}",
        "",
        f"- Test: `{request.node.name}`",
        f"- Fecha y hora: {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Resultado: `{status}`",
        "",
        "## Screenshots",
        "",
    ]
    evidence.extend(f"- `{screenshot}`" for screenshot in screenshots)
    (evidence_test_dir / "evidencia.md").write_text(
        "\n".join(evidence) + "\n",
        encoding="utf-8",
    )


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
