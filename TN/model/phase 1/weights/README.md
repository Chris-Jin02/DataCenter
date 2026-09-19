# Phase 1 presence weights

[Phase 1 overview](../README.md) · [Analysis notebook](../01_dc_geographic_clusters.ipynb)

The input feature matrix is [results/site_feature_matrix.csv](../results/site_feature_matrix.csv). The retained weight tables are [presence_weights.csv](presence_weights.csv) and [cohort_sensitivity_scenarios.csv](cohort_sensitivity_scenarios.csv).

Status date: 2026-09-11.

This directory contains sample weights for subsequent presence-background and PU models. A weight represents confidence in a record as presence evidence; it does not represent site suitability, project success, or construction probability.

## Scenarios

| Scenario | Site count | Master | Candidate | Total weight | Use |
|---|---:|---:|---:|---:|---|
| `primary` | 60 | 60 | 0 | 60.0 | Confirmed, mappable Master records only |
| `weighted` | 74 | 60 | 14 | 69.0 | Adds deduplicated Candidate records; high, medium, and low confidence use 0.75, 0.50, and 0.25 respectively |
| `strict` | 73 | 60 | 13 | 68.5 | Excludes the `area_or_city` coordinate from `weighted` |

All confirmed Master records have a weight of 1. TNDC-006 is excluded from every scenario. TNCAND-010 is represented by TNCAND-009 at the same physical site, and TNCAND-012 is supporting evidence for TNDC-038 rather than an independent point. TNCAND-006 uses a city representative point and appears only in `weighted`.

## Files

- `presence_weights.csv`: weights for every independent site under the three scenarios, with record role, Candidate confidence, and coordinate precision.
- `cohort_sensitivity_scenarios.csv`: site counts, composition, total weights, and inclusion rules for the three scenarios.

Run section 14 of `01_dc_geographic_clusters.ipynb` in the parent directory to regenerate these files from the current workbook and `results/site_feature_matrix.csv`.
