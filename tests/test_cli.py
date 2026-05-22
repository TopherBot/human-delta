import subprocess
import sys
from pathlib import Path


def run_cli(*args: str) -> str:
    """Helper to invoke the installed ``human-delta`` entry‑point.

    The test suite runs against the source checkout, so we call the module
    directly via ``python -m src.human_delta.cli``.
    """
    cmd = [sys.executable, "-m", "src.human_delta.cli", *args]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def test_future_output():
    # 60 seconds from now should be "in 1 minute" (rounded up)
    future = "2099-01-01T00:00:00Z"
    out = run_cli(future)
    assert out.startswith("in ")


def test_past_output():
    past = "2000-01-01T00:00:00Z"
    out = run_cli(past)
    assert out.endswith("ago")


def test_two_dates():
    out = run_cli("2024-01-01", "2024-01-02")
    assert out == "in 1 day" or out == "1 day ago"  # depends on ordering
