# Tennessee Data Center Research

This project provides a reproducible statewide screening and ranking workflow for Tennessee data-center locations. It combines a public facility inventory, spatial features, a constrained candidate domain, spatial validation, and a released scoring package. The resulting score ranks observed feature affinity within the modeled domain; it is not a construction forecast, engineering approval, or substitute for project diligence.

## Current release

The current release is **TN-DC-1.0.0**. It uses a partial-least-squares logistic model (`pls_logistic`) trained on the frozen 21-feature contract and 20 retained Primary-cohort background draws. The release score is the median prediction across those draws, converted to a 0-100 percentile against all eligible statewide cells.

- **Inventory:** 61 Master records and 16 Candidate records.
- **Analytical locations:** 75 unique locations after reconciling linked and shared sites.
- **Primary modeling cohort:** 60 confirmed, mappable Master locations.
- **Candidate domain:** 4,502 statewide 5 km by 5 km cells; 4,391 eligible D1 cells, 110 excluded cells, and 1 unresolved boundary-mismatch cell.
- **Selected specification:** PLS-logistic with 21 standardized predictors and median predictions across 20 draws.
- **Spatial AUC:** 0.812 in East Tennessee, 0.870 in Middle Tennessee, and 0.761 in West Tennessee.

Candidate records are scored externally. They are not training observations and do not provide accuracy evidence.

![Released statewide score map](model/phase%204/results/TN-DC-1.0.0_score_map.png)

![Uncertainty and novelty map](model/phase%204/results/TN-DC-1.0.0_uncertainty_novelty_map.png)

## Phase 1 - inventory and exploratory analysis

Phase 1 established the analytical site population and reconciled source records into a traceable inventory. It joined 26 external fields to all 75 analytical locations; 21 numeric fields supported later feature-space work. The fields cover transmission and road proximity, hydrography, education, and county employment context. They are proxies and do not measure spare power capacity, water rights, fiber performance, or permitting status.

Geographic clustering used DBSCAN with a 20 km neighborhood radius and a minimum of three locations. The confirmed baseline placed 41 of 60 facilities in four groups around Memphis, Nashville, Chattanooga, and Knoxville/Lenoir City. The expanded 75-location view produced five groups: Memphis (13), Jackson (3), Nashville (25), Chattanooga (5), and Knoxville (10), with 19 dispersed locations. Restricting the comparison to the original 60 baseline locations gave an adjusted Rand index of 0.92 and a clustered-pair Jaccard score of 0.93.

Feature-space clustering applied log transformation and robust scaling before K-means. Across K values from 2 to 8, K=2 gave the highest silhouette score of 0.388. These groups describe environmental context for comparison; they are not site grades.

![Confirmed-facility geographic clusters](model/phase%201/results/figures/05_primary_clusters.png)

![Feature-space environmental contexts](model/phase%201/results/figures/16_feature_clusters_geography.png)

## Phase 2 - candidate domain and training data

Phase 2 transformed the inventory into a presence-background dataset. The D1 domain applies slope, selected perennial waterbody, protected-land, floodway, and military-installation constraints. A cell must also retain a largest rook-connected unmasked component of at least 0.10 km2. This is an analytical availability rule, not a decision about parcel legality or commercial feasibility.

The workflow compared 3, 5, 7, and 10 km grids. The 5 km grid retained all 60 Primary facilities while preserving more statewide variation than larger grids. Background samples were stratified by Tennessee grand region and a 50 km metro-distance proxy. Twenty deterministic draws were created for each cohort and ratio; the 10:1 design was selected for the Primary analysis because every stratum met its quota.

Known occupied cells were excluded from the background frame, including locations omitted from a specific cohort. Coordinates, identifiers, hard-constraint fields, and sampling strata are not ordinary model predictors.

## Phase 3 - spatial validation and statewide scoring

Phase 3 registered spatial folds before model comparison. It evaluated grand-region holdouts, 200 km equal-area blocks, repeated background draws, and leave-one-occupied-cell-out checks. The comparison included Elastic Net, PLS-logistic, spline logistic, and constrained boosted-stump specifications, alongside a transparent three-feature logistic baseline.

The selected PLS-logistic model constructs components from the 21 standardized features, then distinguishes Primary locations from stratified background cells. The score for each eligible D1 cell is the median prediction across the 20 models. Draw-level percentiles and interquartile ranges are retained to show sensitivity to background selection. D1-only PCA/K-means regimes provide context and novelty flags; they do not change the numeric rank.

![Phase 3 statewide empirical-affinity score](model/phase%203/results/figures/phase3_final_score_map.png)

## Phase 4 - release and decision products

Phase 4 packaged the final workflow as TN-DC-1.0.0. Release verification reconciled 4,502 statewide cells to 4,391 eligible D1 cells and 111 excluded or unresolved rows. Batch and one-row scoring produced the same result for an identical feature vector.

The release includes statewide scores, a score dictionary, model card, batch-input template, candidate-ranking CSV and workbook, decision guide, and map products. Scores of 90-100 are Priority 1; scores from 75 to below 90 are Priority 2; scores from 50 to below 75 are a watchlist. These bands order diligence work. They do not replace utility capacity and interconnection, fiber diversity, land control, permitting, water, schedule, or cost review.

![Candidate screening dashboard](model/phase%204/results/TN-DC-1.0.0_candidate_dashboard.png)

## Interactive map

[Open the Tennessee data-center map](https://chris-jin02.github.io/DataCenter/Config/).

![Tennessee data-center map](Map/tennessee_dcmap_preview.png)

The image is a static preview. The interactive map contains the latest records, filters, facility details, and evidence links. See [`Map/README.md`](Map/README.md) for source attribution, the map legend, controls, and interpretation notes.

## Repository structure

```text
TN/
├── Map/
│   ├── README.md
│   ├── TN_DC_Map_Generator.ipynb
│   ├── template/TN_dcmap_template.html
│   └── tennessee_dcmap.html
├── Proposal/Tennessee_spatial_analysis.md
├── dataset/
│   ├── tennessee_public_data_centers.xlsx
│   └── Tennessee Data Center Dataset Update and Compatibility Specification.md
├── model/
│   ├── notebook_support/
│   ├── phase 1/
│   ├── phase 2/
│   ├── phase 3/
│   └── phase 4/
└── tests/
```

## Key files

- [`Proposal/Tennessee_spatial_analysis.md`](Proposal/Tennessee_spatial_analysis.md) defines the research questions, analytical scope, spatial methods, and validation strategy.
- [`dataset/tennessee_public_data_centers.xlsx`](dataset/tennessee_public_data_centers.xlsx) contains the normalized Master inventory, candidate sites, audits, and change history.
- [`model/phase 1/README.md`](model/phase%201/README.md) documents geographic and feature-space analysis.
- [`model/phase 2/README.md`](model/phase%202/README.md) documents the candidate domain and modeling dataset.
- [`model/phase 3/README.md`](model/phase%203/README.md) documents the validation design, model comparison, and scoring workflow.
- [`model/phase 4/README.md`](model/phase%204/README.md) describes the release package and decision products.
- [`model/phase 4/results/TN-DC-1.0.0_model_card.md`](model/phase%204/results/TN-DC-1.0.0_model_card.md) defines score semantics, model limits, and intended use.

## Updating the map

Update the workbook first, preserve source URLs and stable IDs, and record material changes in `Change_Log`. Run `TN_DC_Map_Generator.ipynb` from `TN/Map/` to regenerate `tennessee_dcmap.html`.

## Scope and limitations

The files are active research artifacts based on publicly identifiable records. Coverage is not guaranteed to be complete. Facility status, ownership, capacity, and coordinates should be checked against recorded evidence before publication or detailed spatial analysis. The model does not estimate utility capacity, interconnection approval, fiber service, land control, water availability, permitting, cost, schedule, or project approval.
