# Phase 2 Tennessee modeling dataset

[Project overview](../../README.md) · [Previous: Phase 1](../phase%201/README.md) · [Next: Phase 3](../phase%203/README.md)

## Purpose

Phase 2 converts the Phase 1 inventory into a presence-background modeling dataset. It defines a documented statewide candidate domain, evaluates grid and background-sampling sensitivity, and supplies common spatial features for observed sites and candidate cells. It does not estimate construction probability, power capacity, permitting success, or commercial feasibility.

## Final files

- [dataset/phase2_model_dataset.xlsx](dataset/phase2_model_dataset.xlsx): final modeling tables and audit evidence.
- [Phase2_candidate_domain_background.ipynb](Phase2_candidate_domain_background.ipynb): validates strict D1, scale selection, and D2 sampling.
- [Phase2_grid_feature_matrix.ipynb](Phase2_grid_feature_matrix.ipynb): validates the Phase 2C feature join, presents the Phase 2D screening outputs, and checks the Phase 3 handoff contract.

Both notebooks use the [shared support modules](../notebook_support/), including `phase2_io.py`. Review the [project execution-layout notes](../../README.md#notebook-execution-layout) before rerunning them. The phase directory stores the validation notebooks and frozen workbook. The final workbook retains source URLs, filters, calculation definitions, limitations, and aggregate sensitivity results.

## Cohorts

| Scenario | Included sites | Presence-weight total | Rule |
|---|---:|---:|---|
| `primary` | 60 | 60.0 | Confirmed, mappable Master records |
| `weighted` | 74 | 69.0 | Primary plus distinct Candidate locations, weighted by evidence confidence |
| `strict` | 73 | 68.5 | Weighted excluding the `area_or_city` coordinate |

`TNDC-006` is audit-only. `TNCAND-010` shares the physical ORNL location represented by `TNCAND-009`; `TNCAND-012` remains supporting evidence for `TNDC-038`.

## Candidate domain

The primary spatial unit is a 5 km × 5 km equal-area cell clipped to Tennessee land.

- `D0`: Tennessee land cells.
- `D1 v2`: land remaining after the hard-constraint mask and a minimum connected available area test.
- `D2`: repeated, stratified availability samples from D1 v2.

`D1 v2` adapts the documented IM3 exclusion categories to this statewide, mixed-facility inventory. It is an analytical availability rule, not a legal ruling on any parcel.

### D1 v2 hard constraints

The workflow creates a single union mask at 250 m analysis resolution. A cell is `eligible` only if its largest rook-connected unmasked component is at least **0.10 km²** (approximately one million square feet). It is `excluded` if no such component remains; `unresolved` records a source-geometry boundary mismatch and is never sampled.

The hard mask includes:

- slope above 16 percent, from USGS 3DEP slope output;
- selected perennial NHD waterbody categories (`39004`, `39009`–`39012`, `43615`, `43621`);
- PAD-US GAP Status 1 or 2 protected land;
- Tennessee DFIRM polygons explicitly marked `FLOODWAY`;
- NTAD/DoD DISDI military installations, ranges, and training areas.

The rule differs from the previous `mean_slope_deg < 15` screen. The old D1 fields remain as `d1_feasible_v1` or context variables, while `d1_feasible` now represents D1 v2. The workbook carries per-cell fractions for each hard constraint, the non-additive union fraction, available area, largest available component, and stable exclusion reason.

The military layer is public regional mapping and is explicitly incomplete/non-cadastral; it receives no arbitrary buffer. PAD-US GAP 3/4, intermittent or unknown-hydroperiod water, and non-floodway flood zones remain review context rather than being silently converted into hard exclusions.

Current results: 4,502 D0 cells; 4,391 D1-eligible cells; 110 excluded cells; one unresolved boundary-mismatch cell. All Primary, Weighted, and Strict cohort records remain in D1 v2.

## Grid-scale comparison

The same hard-mask specification was evaluated at 3, 5, 7, and 10 km equal-area grids. The final workbook retains aggregate results in `Grid_Scale_Diagnostics`, not four redundant candidate-domain tables.

| Grid size | Resolved D0 cells used in diagnostic | D1 cells | Primary records mapped to D1 |
|---|---:|---:|---:|
| 3 km | 12,443 | 11,973 | 59 |
| 5 km | 4,501 | 4,391 | 60 |
| 7 km | 2,381 | 2,328 | 60 |
| 10 km | 1,205 | 1,179 | 59 |

Five kilometres is the primary scale because it retains all 60 Primary records while preserving substantially more spatial variation and D1 sampling support than 7 km. Three and ten kilometres each lose one boundary-sensitive Primary mapping in this fixed-anchor diagnostic. This is a Phase 2 design selection, not evidence of superior predictive accuracy; Phase 3 must still conduct spatial validation and scale sensitivity.

The `Domain_Cells` table retains 4,502 five-kilometre D0 cells: 4,501 resolved cells represented in the scale diagnostic plus one `unresolved` boundary-mismatch cell. That unresolved cell is not D1-eligible and is never sampled. `Grid_Scale_Diagnostics.d0_count_scope` records this counting basis row by row.

## D2 background sampling

For every scenario, D2 excludes every known occupied presence cell, even if that record is not included in the current scenario. Sampling is stratified by Tennessee grand region (`west`, `middle`, `east`) and a 50 km metro-distance proxy (`metro_50km`, `nonmetro`). Background locations are availability samples, not failed projects.

For scenario `s`, stratum `h`, and requested ratio `r`:

```text
P[s,h] = count of scenario-included D1 sites in stratum h
N[h]   = eligible D1 cells in h minus every occupied presence cell
q[s,r,h] = r × P[s,h]
n[s,r,h] = min(q[s,r,h], N[h])
```

Samples are drawn without replacement inside each stratum and draw. They are not borrowed across strata and are not drawn with replacement. If `n = N < q`, the entire stratum becomes a documented census stratum (`sampling_probability = 1`, frame weight = 1). If `N = 0` while `P > 0`, the audit records `zero_eligible_conflict` and produces no artificial background rows.

Twenty deterministic draws use seeds 4701–4720. Within a draw and stratum, the random order is shared by the 5:1, 10:1, and 20:1 sensitivity designs, so smaller ratios are nested prefixes of larger ratios.

### Ratio comparison

| Ratio | Result under D1 v2 | Interpretation |
|---:|---|---|
| 5:1 | All scenario/stratum quotas met | Low-cost sensitivity design |
| 10:1 | All scenario/stratum quotas met | Selected primary design |
| 20:1 | 120 census-shortfall audit rows across 20 draws | Two small strata cannot meet the requested quota |

The 10:1 choice is operational: it is the largest tested ratio without a shortfall under D1 v2. Phase 2 cannot prove that 10:1 improves predictive accuracy over 5:1 or 20:1. In Phase 3, select the smallest ratio that is non-inferior under identical spatial folds and nested draws.

The primary 10:1 output contains 600 Primary, 740 Weighted, and 730 Strict background cells per draw; 41,400 rows total. `Background_Sampling_Audit` preserves all three-ratio diagnostics, quotas, probabilities, frame weights, census status, and shortfall status. `Background_Samples` retains the final 10:1 sample plus its `cell_id` join key; feature values are inherited from `Domain_Cells` rather than copied redundantly.

## Phase 2C features

`Presence_Sites` uses recorded coordinates. `Domain_Cells` uses grid centroids. `Background_Samples` joins its feature vector to `Domain_Cells` by `cell_id`.

The 21 numeric proxies cover transmission proximity/voltage/owner diversity, road and Interstate proximity, hydrographic proximity, institutions and CIP 11/14 completions within 50 and 100 km, and county employment/establishment context. Definitions, units, calculations, zero/missing conventions, and limitations appear in `Feature_Dictionary`; coverage and ranges appear in `Feature_Quality`.

These variables do not establish spare capacity, interconnection approval, water allocation, flood safety, land control, permits, fiber quality, labor availability, or commercial demand.

## Phase 2D feature screening

Phase 2D is a preliminary feature-screening step, not a final causal or predictive-importance claim. It uses the 21 Phase 2C features across all three Presence scenarios and all 20 final D2 10:1 draws per scenario.

For each feature, the workbook reports a weighted univariate Mann–Whitney AUC, then evaluates multivariable contribution through permutation loss of weighted AUC in three region-held-out folds (train on two Tennessee grand regions; test on the third). The final table reports the median and 5th–95th percentile across repetitions, the share of positive permutation losses, and the number of scenarios with positive median loss.

Highly correlated features are grouped when their absolute Spearman correlation is at least 0.80 across D1-eligible cells. Only the best-ranked member of a group can be marked as a Phase 3 priority; other members remain documented as `review_for_collinearity` rather than being silently discarded.

The preliminary Phase 3 priority features are:

- `dist_major_road_km` — lower distance is associated with Presence; median permutation AUC loss 0.0116 and 88.9% positive losses.
- `dist_transmission_any_km` — lower distance is associated with Presence; median permutation AUC loss 0.0075 and 79.4% positive losses.
- `dist_surface_water_flowline_km` — higher distance is associated with Presence in this dataset; median permutation AUC loss 0.0027 and 72.2% positive losses.

`Feature_Screening` contains the ranked results. `Phase2D_Methods` records the analysis population, validation approach, permutation rule, collinearity rule, and limitations. Phase 3 must re-evaluate feature selection within its final spatial cross-validation and model-comparison protocol.

## Phase 3 handoff contract

`Phase3_Training_Contract` freezes the permitted use of every training-relevant field. It requires a derived `is_presence` outcome, allows exactly one Presence evidence-weight field per scenario, and reserves `background_weight` for a separately specified design-weighted sensitivity analysis. Sampling fields, identifiers, raw coordinates, D1-definition fields, and D2 stratification fields are not ordinary predictors.

The 21 numeric proxies retain their Phase 2D disposition: three primary candidates, ten secondary candidates, and eight features requiring one representative per collinearity group. The primary Phase 3 candidates are major-road distance, any-transmission distance, and surface-water-flowline distance. This is a starting contract for spatial model comparison, not a final causal or importance claim.

`Phase2_Closeout` is the final checklist for cohort definitions, D1 v2, D2 design, feature completeness, screening, validation, and interpretation limits. Phase 3 must preserve spatially separated validation; repeat feature selection within its training folds; compare model families; evaluate 5:1 and 20:1 as D2 sensitivities; and avoid presenting outputs as construction probabilities or engineering feasibility guarantees.

## Sources and checks

`Source_Catalog` records the official source for the state boundary, USGS 3DEP, NHD, PAD-US, Tennessee DFIRM, NTAD Military Bases, HIFLD transmission, Tennessee roads, NCES IPEDS, Census CBP, and TIGERweb counties. The D1 rationale cites the IM3-associated [OSTI projected-data record](https://www.osti.gov/biblio/2571680); it is methodological inspiration, not a claim that this workbook reproduces an IM3 national siting model.

The validation notebooks assert D1 counts and statuses, Presence retention, scale selection evidence, D2 row counts, no Presence leakage, no within-draw duplicates, ratio-10 quota completion, ratio-20 shortfall handling, and complete Phase 2C feature joins.
