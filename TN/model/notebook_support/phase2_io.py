"""Shared loading of the frozen Phase 2 workbook."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

PHASE2_RELATIVE = Path("TN/model/phase 2/dataset/phase2_model_dataset.xlsx")
PHASE2_OUTPUT_RELATIVE = Path("outputs/Data center/TN/model/phase 2/dataset/phase2_model_dataset.xlsx")


def resolve_phase2_workbook(root: Path | None = None) -> Path:
    """Return the maintained Phase 2 workbook, preferring the phase copy."""
    if root is None:
        try:
            from tn_common import find_project_root
        except ModuleNotFoundError:  # package import from repository-root runners
            from TN.model.notebook_support.tn_common import find_project_root
        root = find_project_root()
    project_root = root.resolve()
    candidates = (project_root / PHASE2_RELATIVE, project_root / PHASE2_OUTPUT_RELATIVE)
    for path in candidates:
        if path.is_file():
            return path
    searched = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Phase 2 workbook not found; searched: {searched}")


@dataclass(frozen=True)
class Phase2Tables:
    """Named Phase 2 sheets used by downstream notebooks."""

    path: Path
    sheets: dict[str, Any]

    @property
    def presence(self):
        return self.sheets["Presence_Sites"]

    @property
    def domain(self):
        return self.sheets["Domain_Cells"]

    @property
    def background(self):
        return self.sheets["Background_Samples"]

    @property
    def contract(self):
        return self.sheets["Phase3_Training_Contract"]


def load_phase2_workbook(root: Path | None = None) -> Phase2Tables:
    """Read all Phase 2 sheets once and expose the required sheets by name."""
    try:
        import pandas as pd
    except ModuleNotFoundError as exc:
        raise RuntimeError("Phase 2 workbook loading requires pandas and openpyxl") from exc
    path = resolve_phase2_workbook(root)
    sheets = pd.read_excel(path, sheet_name=None)
    required = {"Presence_Sites", "Domain_Cells", "Background_Samples", "Phase3_Training_Contract"}
    missing = sorted(required - set(sheets))
    if missing:
        raise ValueError(f"Phase 2 workbook is missing required sheets: {missing}")
    return Phase2Tables(path=path, sheets=sheets)
