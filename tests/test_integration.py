"""Integration tests for cloc-python."""

import json
import subprocess
import sys
from pathlib import Path


def run_cloc_python(*args: str) -> subprocess.CompletedProcess[str]:
    """Run cloc-python with the given arguments."""

    return subprocess.run(
        [sys.executable, "-m", "cloc_python", *args],
        capture_output=True,
        text=True,
    )


def test_cloc_python_version():
    """Test that cloc-python outputs version information."""

    result = run_cloc_python("--version")
    assert result.returncode == 0
    assert "2.08" in result.stdout


def test_cloc_python_counts_test_files():
    """Test that cloc-python counts lines in test fixture files."""

    fixtures_dir = Path(__file__).parent / "fixtures"

    result = run_cloc_python(str(fixtures_dir))

    assert result.returncode == 0

    output = result.stdout + result.stderr
    assert "Python" in output
    assert "JavaScript" in output


def test_cloc_python_json_output():
    """Test that cloc-python can output JSON."""

    fixtures_dir = Path(__file__).parent / "fixtures"
    test_file = fixtures_dir / "test_json.py"

    result = run_cloc_python(str(test_file), "--json")

    assert result.returncode == 0
    output = result.stdout + result.stderr

    converted_json = json.loads(output)
    assert converted_json is not None

    converted_json = dict(converted_json)
    assert "Python" in converted_json
    assert "nFiles" in converted_json["Python"]
    assert converted_json["Python"]["nFiles"] == 1
    assert converted_json["Python"]["blank"] == 0
    assert converted_json["Python"]["comment"] == 1
    assert converted_json["Python"]["code"] == 1
    assert "SUM" in converted_json
    assert converted_json["SUM"]["nFiles"] == 1
    assert converted_json["SUM"]["blank"] == 0
    assert converted_json["SUM"]["comment"] == 1
    assert converted_json["SUM"]["code"] == 1


def test_cloc_python_nonexistent_path():
    """Test that cloc-python handles nonexistent paths gracefully."""

    result = run_cloc_python("/nonexistent/path/that/does/not/exist")

    assert result.returncode == 0


def test_cloc_python_with_by_file():
    """Test that cloc-python --by-file works."""

    fixtures_dir = Path(__file__).parent / "fixtures"
    result = run_cloc_python(str(fixtures_dir), "--by-file")

    assert result.returncode == 0
    output = result.stdout + result.stderr

    # Should show the filename in the output
    assert "File" in output
    assert "blank" in output
    assert "comment" in output
    assert "code" in output
    assert "test_by_file.py" in output


def test_cloc_python_help():
    """Test that cloc-python help output works."""
    result = run_cloc_python("--help")

    assert result.returncode == 0
    output = result.stdout + result.stderr

    assert "Usage:" in output or "usage:" in output
    assert "cloc" in output.lower()
