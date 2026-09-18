# Phase 1: Tennessee data-center geographic clustering, feature clustering, and manual analysis

Status date: 2026-09-11.

## Current data structure

The source master workbook is stored at `TN/dataset/tennessee_public_data_centers.xlsx` and is not duplicated in `model`. It retains its original 13 worksheets.

- `Master`: 61 records, 69 columns, and 61 unique `facility_id` values. Twenty-eight Phase 1 fields were appended, including nearest-neighbor distance, cluster labels, and 26 external environmental proxies.
- `Candidate_Sites`: 16 records, 49 columns, and 16 unique Candidate IDs. It includes `phase1_feature_status` and the same 28 Phase 1 fields.
- Candidate processing: 11 records were calculated from original coordinates; TNCAND-005 and TNCAND-017 use Census address matches; TNCAND-006 uses a Census Nashville-Davidson city representative point; TNCAND-010 shares ORNL physical-site features with TNCAND-009; and TNCAND-012 inherits features from linked TNDC-038. All 16 Candidate records have Phase 1 features.
- `results/site_feature_matrix.csv`: 75 unique analysis-site rows: 61 Master records plus 14 Candidate sites not merged into Master. TNCAND-006 uses a city representative point, so its features are market-level estimates. The full Candidate source records remain in `Candidate_Sites`.

## Modeling cohorts and weights

Phase 1 closeout froze the sample definitions for subsequent presence-background and PU models. The expanded 75-row matrix remains available for descriptive maps and environmental grouping; formal modeling scenarios exclude unconfirmed Master records and handle Candidate records as separate sensitivity scenarios.

- `primary`: 60 confirmed, mappable, unique Master sites; total weight 60.0.
- `weighted`: 60 Master records plus 14 deduplicated Candidate sites, for 74 locations and total weight 69.0. High, medium, and low Candidate evidence confidence correspond to weights of 0.75, 0.50, and 0.25.
- `strict`: 73 locations and total weight 68.5 after excluding TNCAND-006, which has an `area_or_city` coordinate, from `weighted`.

TNDC-006 is a low-confidence unconfirmed Master record and is excluded from every modeling scenario. TNCAND-010 shares the ORNL physical site represented by TNCAND-009; TNCAND-012 is linked supporting evidence for TNDC-038 and is not an independent point. A weight represents confidence in a record as presence evidence, not suitability or construction probability.

## Notebook

- `01_dc_geographic_clusters.ipynb`: preserves the geographic-clustering baseline for 60 `confirmed` Master records; runs extended geographic clustering for 75 unique locations; performs feature-space clustering using 21 numeric external environmental fields; and produces sensitivity comparisons, group profiles, quantified feature-separation contributions, manual analysis, and frozen modeling cohorts.

All 18 code cells in the notebook have been executed with no error output. Re-run it from the `model/phase 1` directory.

## Main results

The primary DBSCAN specification is `eps=20 km, min_samples=3`. Of 60 confirmed sites, 41 fall into four clusters: Memphis 11, Nashville 19, Chattanooga 4, and Knoxville/Lenoir City 7. The remaining 19 are isolated points or groups smaller than three samples.

With the same DBSCAN parameters applied to 75 unique locations, 56 locations fall into five geographic clusters: Memphis 13, Jackson 3, Nashville 25, Chattanooga 5, and Knoxville 10; another 19 are isolated or in small groups. Comparing only the original 60 baseline locations, the expanded result has an Adjusted Rand Index of 0.92 and a clustered-pair Jaccard score of 0.93 against the baseline.

Feature clustering uses 21 numeric variables from 26 external fields. County name, FIPS, and three CBP disclosure flags are retained for interpretation but excluded from distance calculations. Numeric variables receive `log1p` and `RobustScaler` transformations. KMeans selects K=2 from K=2–8 by the highest silhouette score (0.388). F1 contains 20 smaller-market or comparatively less infrastructure-accessible locations; F2 contains 55 metropolitan locations with greater access to employment and talent. These are environmental-similarity groups, not suitability grades.

All 26 external fields have 100% coverage in the 75-row analysis matrix. CBP does not publish NAICS 51/54 industry rows for Meigs County, so employment and establishment counts for TNDC-010 are zero and marked `NO_PUBLISHED_ROW`, distinguishing them from Census suppression flags.

`results/interactive_clusters.html` is a self-contained offline file using embedded SVG, state boundaries, and all 75 unique locations; it does not depend on a CDN, map tiles, or external CSV files. It supports switching between geographic and feature clustering, record-role filtering, hover, click, scroll zoom, dragging, and pan reset. Candidate records use triangles and unconfirmed Master records use crosses. The bottom of the map first shows an overview of each geographic or feature group for the selected mode, followed by DBSCAN, feature-processing, and marker-shape notes. Clicking a point shows its name, location, record role, both group labels, facility type, status, and coordinate precision. Click handling prevents map-panning logic from taking over and does not alter cluster membership.

## Output files

- Geographic-clustering baseline: `cluster_assignments.csv`, `cluster_summary.csv`, `parameter_sweep.csv`, `stability_summary.csv`, `coordinate_jitter_simulations.csv`
- Extended geographic clustering: `expanded_cluster_assignments.csv`, `expanded_cluster_summary.csv`, `geographic_cohort_comparison.csv`
- Feature clustering: `feature_cluster_diagnostics.csv`, `feature_cluster_summary.csv`, `feature_cluster_profiles.csv`, `feature_cluster_importance.csv`
- Features: `site_feature_matrix.csv`, `feature_data_dictionary.csv`, `feature_completeness.csv`
- Modeling cohorts: `primary_presence_cohort.csv`, `cohort_exclusion_audit.csv`
- Interpretation and sources: `feature_completion_report.md`, `source_catalog.csv`
- Figures: 19 PNGs in `results/figures`
- Interactive map: `interactive_clusters.html`

Weight files are stored separately in `weights/`:

- `presence_weights.csv`: weights for 74 independent modeling sites under `primary`, `weighted`, and `strict`.
- `cohort_sensitivity_scenarios.csv`: site counts, composition, total weights, and coordinate rules for all scenarios.
- `weights/README.md`: weight semantics, treatment of special records, and regeneration instructions.

## Interpretation limits

The existing fields support site screening and group comparison. Proximity to transmission lines does not indicate spare capacity or interconnection conditions; proximity to hydrography does not indicate water capacity, water rights, or permits; IPEDS degree completions do not indicate immediately available labor; and CBP is county-level workplace employment data. Comparable statewide, site-level public data remain unavailable for substation capacity, specific electricity prices and interconnection queues, water capacity and permits, and fiber routes and latency; no subjective imputation was performed.
