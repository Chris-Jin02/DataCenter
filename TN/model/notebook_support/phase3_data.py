"""Reusable Phase 3 data preparation and ranking helpers."""

from __future__ import annotations

from typing import Sequence
import math


def empirical_percentile(values: Sequence[float]):
    """Return average-tie empirical percentiles on the 0–100 scale."""
    values = list(values)
    valid = [(index, value) for index, value in enumerate(values) if not (isinstance(value, float) and math.isnan(value))]
    n = len(valid)
    if not n:
        return [float("nan")] * len(values)
    ordered = sorted(valid, key=lambda item: item[1])
    ranks = [float("nan")] * len(values)
    start = 0
    while start < n:
        end = start + 1
        while end < n and ordered[end][1] == ordered[start][1]:
            end += 1
        rank = (start + 1 + end) / 2
        for position in range(start, end):
            ranks[ordered[position][0]] = 100.0 * rank / n
        start = end
    return ranks


def log_standardize(train, apply, features):
    """Fit log1p standardization on train and apply the same transform."""
    import numpy as np

    train_x = np.log1p(train[features].to_numpy(float))
    apply_x = np.log1p(apply[features].to_numpy(float))
    mean = train_x.mean(axis=0)
    scale = train_x.std(axis=0, ddof=0)
    scale[scale == 0] = 1.0
    return (train_x - mean) / scale, (apply_x - mean) / scale, mean, scale


def make_training_table(sites, domain, background, scenario, draw, features):
    """Assemble one presence/background training table for a draw."""
    weight_col = f"{scenario}_weight"
    presence = sites.loc[
        sites[weight_col].fillna(0).gt(0),
        ["site_id", "cell_id", "grand_region", weight_col, *features],
    ].copy()
    presence = presence.rename(columns={weight_col: "sample_weight"})
    presence["label"] = 1
    bg = background.loc[
        (background["scenario"] == scenario) & (background["draw"] == draw),
        ["cell_id", "grand_region"],
    ].merge(domain[["cell_id", *features]], on="cell_id", validate="one_to_one")
    bg["site_id"] = None
    bg["sample_weight"] = 1.0
    bg["label"] = 0
    result = __import__("pandas").concat([presence, bg[presence.columns]], ignore_index=True)
    assert not result["cell_id"].isna().any()
    assert result[list(features)].notna().all().all()
    return result
