# Principal Factor: U.S. Data Center Siting

Research proposal for constructing an observable, reproducible feature set and benchmark design for U.S. data center siting. The repository aligns its first-version variables and hard exclusions with the IM3 Open Source Data Center Atlas and CERF Data Centers.

## Status and scope

This repository is a **dataset and modeling proposal**, not a report of fitted-model performance. It covers the 50 U.S. states and focuses on power, water/cooling, network access, land/construction, and cost/market conditions. No synthetic accuracy results are reported.

## Repository structure

```text
.
├── README.md
├── notebooks/
│   ├── 01_us_site_inventory_and_feature_schema.ipynb
│   └── 02_modeling_and_benchmark_design.ipynb
└── data/
    ├── README.md
    └── raw/
        ├── im3_us_data_center_locations.gpkg
        └── us_states_2025.geojson
```

The numbered notebooks separate data definition from model design:

1. `01_us_site_inventory_and_feature_schema.ipynb` documents entity resolution, the U.S. state map, 15 core features, and H1–H13 hard constraints.
2. `02_modeling_and_benchmark_design.ipynb` specifies machine-learning and deep-learning candidates and a strict 2 × 2 benchmark: single-model versus factor-wise late fusion, each evaluated as regression and ordinal classification.

## Site inventory

The IM3 Atlas contains parallel `point`, `building`, and `campus` layers without a shared project key. The proposal therefore constructs mutually exclusive `site_id` entities instead of adding layer counts. Under the default spatial and identity boundaries, the inventory contains 951 inferred independent sites: 132 explicit campuses, 731 building-inferred sites, and 88 standalone points. These values are entity-resolution estimates, not an official census.

## Core modeling design

- **Regression target:** `y_score`, a continuous recommendation score with higher values preferred.
- **Ordinal target:** `y_grade ∈ {1,…,K}`, where grade 1 is best and `K=3/4/5` is selected within training folds.
- **Architectures:** one model trained on all 15 features versus five factor models combined using out-of-fold late fusion.
- **Validation:** nested spatial cross-validation plus one locked geographic test set.
- **Hard constraints:** H1–H13 are applied before scoring and are not compensatory model features.

## Reproducibility

The only executable cell in the data notebook uses the Python standard library (`pathlib` and `sqlite3`) and expects the notebook to run from `notebooks/`. Its relative path resolves the included GeoPackage at `../data/raw/im3_us_data_center_locations.gpkg`. The notebook's reported entity-resolution counts document a broader geospatial procedure and should not be confused with the simple source-layer `COUNT(DISTINCT id)` demonstration.

## Data provenance

See [`data/README.md`](data/README.md) for source, role, and reuse notes. Principal upstream sources include the [IM3 Data Center Atlas](https://github.com/IMMM-SFA/datacenter-atlas), [CERF Data Centers](https://github.com/IMMM-SFA/cerf_data_centers), FCC Broadband Data Collection, USGS Public Supply Service Areas, HIFLD/GeoPlatform, NLCD, and Census TIGERweb.

## Limitations

- Site counts depend on explicit entity-resolution boundaries and require sampled manual review.
- Distance to infrastructure does not establish spare electric, water, or network capacity.
- Several project-specific features require permits, utility opinions, or local tax and parcel records.
- A valid supervised model still requires defensible outcome or expert labels collected independently of model inputs.

No license is asserted for third-party source data in this repository. Users should review the original providers' terms before redistribution or derivative use.
