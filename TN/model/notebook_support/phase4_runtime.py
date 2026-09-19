"""Small runtime helpers shared by the Phase 4 notebook cells."""

from __future__ import annotations

import sys
import types
from collections.abc import Mapping


def register_namespace(name: str, namespace: Mapping[str, object]) -> types.ModuleType:
    """Register a notebook namespace for later cells without repeated boilerplate."""
    module = types.ModuleType(name)
    module.__dict__.update(namespace)
    sys.modules[name] = module
    return module
