"""
Shared validation helpers and structured parser loaders.

Provides standard failure handling, assertions, and robust JSON/YAML/TOML
loaders for all repository validation scripts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Container, Dict, List, Optional

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

try:
    import yaml
except ImportError:
    yaml = None


def fail(msg: str) -> None:
    """Print failure message and exit with non-zero exit code."""
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def load_json(path: Path) -> Any:
    """Load and parse JSON file."""
    if not path.exists():
        fail(f"JSON file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        fail(f"Failed to parse JSON file {path}: {e}")


def load_yaml(path: Path) -> Any:
    """Load and parse YAML file using PyYAML."""
    if yaml is None:
        fail("PyYAML is required for YAML parsing. Run via 'uv run ...' or install via 'uv sync'.")
    if not path.exists():
        fail(f"YAML file not found: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        fail(f"Failed to parse YAML file {path}: {e}")


def load_toml(path: Path) -> Dict[str, Any]:
    """Load and parse TOML file using standard tomllib / tomli."""
    if tomllib is None:
        fail("tomllib/tomli is required for TOML parsing. Run via 'uv run ...' or install via 'uv sync'.")
    if not path.exists():
        fail(f"TOML file not found: {path}")
    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except Exception as e:
        fail(f"Failed to parse TOML file {path}: {e}")


def assert_eq(actual: Any, expected: Any, msg: Optional[str] = None) -> None:
    """Assert actual equals expected."""
    if actual != expected:
        detail = msg or f"Expected {expected!r}, got {actual!r}"
        fail(detail)


def assert_in(item: Any, container: Container, msg: Optional[str] = None) -> None:
    """Assert item is in container."""
    if item not in container:
        detail = msg or f"Expected {item!r} in container"
        fail(detail)


def assert_true(condition: bool, msg: str) -> None:
    """Assert condition is True."""
    if not condition:
        fail(msg)
