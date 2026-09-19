"""Shared plotting, path, and metric helpers used by Tennessee notebooks.

All static analytical figures use Matplotlib and the same project theme.
Interactive map products remain HTML because users need to pan, filter, and
inspect individual sites.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable, Sequence

import matplotlib.pyplot as plt
import numpy as np


PALETTE = {
    "blue": "#2563eb",
    "green": "#16a34a",
    "amber": "#f59e0b",
    "red": "#dc2626",
    "purple": "#7c3aed",
    "cyan": "#0891b2",
    "muted": "#6b7280",
}


def find_project_root(start: Path | None = None) -> Path:
    """Find the repository root from a notebook or its current directory."""
    current = (start or Path.cwd()).resolve()
    for parent in (current, *current.parents):
        if (parent / "outputs" / "Data center" / "TN").is_dir():
            return parent
    raise FileNotFoundError("Could not find the project root containing outputs/Data center/TN")


def apply_plot_theme() -> None:
    """Apply the single visual language used by every static project figure."""
    plt.rcParams.update({
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": "#d1d5db",
        "grid.linewidth": 0.7,
        "font.family": "DejaVu Sans",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
    })


def finish_figure(figure, path: Path | None = None):
    """Apply compact layout, optionally save PNG, and show the figure once."""
    figure.tight_layout()
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.show()


def horizontal_bars(
    title: str,
    labels: Sequence[object],
    values: Sequence[float],
    *,
    unit: str = "",
    note: str = "",
    color: str = PALETTE["blue"],
    width: int = 760,
    height: int = 300,
) -> object:
    """Render a labelled horizontal bar chart with the project Matplotlib theme."""
    apply_plot_theme()
    figure, axis = plt.subplots(figsize=(width / 100, height / 100))
    positions = np.arange(len(labels))
    bars = axis.barh(positions, values, color=color)
    axis.set_yticks(positions, [str(label) for label in labels])
    axis.invert_yaxis()
    axis.set_title(title, loc="left", pad=18)
    if note:
        axis.text(0, 1.01, note, transform=axis.transAxes, color="#4b5563", fontsize=9, va="bottom")
    axis.grid(axis="x"); axis.grid(axis="y", visible=False)
    for bar, value in zip(bars, values):
        axis.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f" {float(value):,.0f}{unit}", va="center", fontsize=9)
    return finish_figure(figure)


def paired_bars(
    title: str,
    labels: Sequence[object],
    first: Sequence[float],
    second: Sequence[float],
    first_label: str,
    second_label: str,
    note: str = "",
    *,
    first_color: str = PALETTE["blue"],
    second_color: str = PALETTE["green"],
    value_format: str = ".0f",
    width: int = 760,
    height: int = 340,
) -> object:
    """Render two values per row with grouped horizontal bars."""
    apply_plot_theme()
    figure, axis = plt.subplots(figsize=(width / 100, height / 100))
    positions = np.arange(len(labels))
    offset = 0.19
    first_bars = axis.barh(positions - offset, first, height=0.34, color=first_color, label=first_label)
    second_bars = axis.barh(positions + offset, second, height=0.34, color=second_color, label=second_label)
    axis.set_yticks(positions, [str(label) for label in labels])
    axis.invert_yaxis()
    axis.set_title(title, loc="left", pad=18)
    if note:
        axis.text(0, 1.01, note, transform=axis.transAxes, color="#4b5563", fontsize=9, va="bottom")
    axis.legend(loc="lower right", frameon=False)
    axis.grid(axis="x"); axis.grid(axis="y", visible=False)
    for left_bar, right_bar, a, b in zip(first_bars, second_bars, first, second):
        axis.text(max(left_bar.get_width(), right_bar.get_width()), right_bar.get_y() + right_bar.get_height() / 2,
                  f" {format(float(a), value_format)} / {format(float(b), value_format)}", va="center", fontsize=9)
    return finish_figure(figure)


def point_map(
    frame,
    *,
    longitude: str,
    latitude: str,
    value: str,
    title: str,
    note: str = "",
    path: Path | None = None,
    excluded=None,
    novelty=None,
):
    """Render a consistently styled point map for a statewide grid product."""
    apply_plot_theme()
    figure, axis = plt.subplots(figsize=(12, 4.2))
    if excluded is not None and len(excluded):
        axis.scatter(excluded[longitude], excluded[latitude], s=5, c="#9ca3af", alpha=.55, label="D0 excluded or unresolved")
    points = axis.scatter(frame[longitude], frame[latitude], c=frame[value], s=13, cmap="YlOrRd", alpha=.82, linewidths=0)
    if novelty is not None and len(novelty):
        axis.scatter(novelty[longitude], novelty[latitude], s=22, facecolors="none", edgecolors="#111827", linewidths=.6, label="Novelty flag")
    colourbar = figure.colorbar(points, ax=axis, pad=.02)
    colourbar.set_label(value.replace("_", " "))
    axis.set(xlabel="Longitude", ylabel="Latitude")
    axis.set_title(title, pad=28)
    if note:
        axis.text(0, 1.02, note, transform=axis.transAxes, color="#4b5563", fontsize=9, va="bottom")
    if excluded is not None or novelty is not None:
        axis.legend(loc="lower right", frameon=True, fontsize=8)
    axis.set_aspect(1.25)
    return finish_figure(figure, path)


def sigmoid(value):
    """Numerically stable logistic transform used by the Phase 3 models."""
    return 1.0 / (1.0 + np.exp(-np.clip(value, -35, 35)))


def weighted_auc(y: Iterable[float], score: Iterable[float], sample_weight: Iterable[float]) -> float:
    """Weighted AUC with half credit for tied scores."""
    order = np.argsort(score, kind="mergesort")
    y, score, weight = np.asarray(y)[order], np.asarray(score)[order], np.asarray(sample_weight)[order]
    positive, negative = weight[y == 1].sum(), weight[y == 0].sum()
    if not positive or not negative:
        return float("nan")
    below_negative = concordant = 0.0
    start = 0
    while start < len(y):
        end = start + 1
        while end < len(y) and score[end] == score[start]:
            end += 1
        positive_weight = weight[start:end][y[start:end] == 1].sum()
        negative_weight = weight[start:end][y[start:end] == 0].sum()
        concordant += positive_weight * (below_negative + 0.5 * negative_weight)
        below_negative += negative_weight
        start = end
    return float(concordant / (positive * negative))
