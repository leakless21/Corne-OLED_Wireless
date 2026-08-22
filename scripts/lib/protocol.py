"""
Semantic Protocol v1 Specification Loader & Mapping Helpers.

Provides typed access to protocol/semantic-v1.yaml and bidirectional mapping
helpers between semantic signals and host/firmware representations.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

try:
    from .validation import fail, load_yaml
except ImportError:
    try:
        from lib.validation import fail, load_yaml
    except ImportError:
        from scripts.lib.validation import fail, load_yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROTOCOL_PATH = REPO_ROOT / "protocol" / "semantic-v1.yaml"


@dataclass
class SemanticSignal:
    key: str
    modifiers: List[str] = field(default_factory=list)

    @property
    def canonical_str(self) -> str:
        if not self.modifiers:
            return self.key
        mods = "+".join(m.capitalize() for m in self.modifiers)
        return f"{mods}+{self.key}"

    def to_zmk(self) -> str:
        """Convert to ZMK keycode expression (e.g., '&kp LC(LS(F13))')."""
        if not self.modifiers:
            return f"&kp {self.key}"

        mod_map = {
            "ctrl": "LC",
            "shift": "LS",
            "alt": "LA",
            "gui": "LG",
        }
        zmk_mods = [mod_map[m.lower()] for m in self.modifiers if m.lower() in mod_map]
        expr = self.key
        for m in reversed(zmk_mods):
            expr = f"{m}({expr})"
        return f"&kp {expr}"

    def to_glazewm(self) -> str:
        """Convert to GlazeWM binding string (e.g., 'ctrl+shift+f13')."""
        parts = [m.lower() for m in self.modifiers] + [self.key.lower()]
        return "+".join(parts)

    def to_ahk_trigger(self) -> str:
        """Convert to AutoHotkey v2 trigger string (e.g., '^+F13::')."""
        prefix = ""
        for m in self.modifiers:
            if m.lower() == "ctrl":
                prefix += "^"
            elif m.lower() == "shift":
                prefix += "+"
            elif m.lower() == "alt":
                prefix += "!"
            elif m.lower() == "gui":
                prefix += "#"
        return f"{prefix}{self.key}::"


@dataclass
class SemanticAction:
    id: str
    signal: SemanticSignal
    category: str
    description: str
    host_implementations: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProtocolManifest:
    version: int
    name: str
    actions: Dict[str, SemanticAction]

    def action(self, action_id: str) -> SemanticAction:
        if action_id not in self.actions:
            raise KeyError(f"Action '{action_id}' not found in protocol")
        return self.actions[action_id]

    def all_zmk_signals(self) -> Set[str]:
        return {a.signal.to_zmk() for a in self.actions.values()}

    def all_glazewm_signals(self) -> Set[str]:
        return {a.signal.to_glazewm() for a in self.actions.values()}


def load_protocol(path: Optional[Path] = None) -> ProtocolManifest:
    p = path or PROTOCOL_PATH
    data = load_yaml(p)
    if not isinstance(data, dict):
        fail(f"Invalid protocol YAML root in {p}")

    version = data.get("version", 1)
    name = data.get("name", "Semantic Protocol")
    actions_raw = data.get("actions", {})

    actions = {}
    for action_id, info in actions_raw.items():
        sig_info = info.get("signal", {})
        key = sig_info.get("key", "")
        modifiers = sig_info.get("modifiers", [])
        signal = SemanticSignal(key=key, modifiers=modifiers)

        action = SemanticAction(
            id=action_id,
            signal=signal,
            category=info.get("category", "general"),
            description=info.get("description", ""),
            host_implementations=info.get("host_implementations", {}),
        )
        actions[action_id] = action

    return ProtocolManifest(version=version, name=name, actions=actions)
