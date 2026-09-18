# Phase 1 feature-completion report

Status date: 2026-09-08.

## Coverage

- Physical-site matrix: 75 rows, 40 columns, and no duplicate `facility_id` values.
- The 75 rows comprise 61 Master records and 14 independent, mappable Candidate sites not merged into Master.
- TNCAND-009 and TNCAND-010 use the same ORNL coordinates; TNCAND-009 represents the site-level matrix row, while both source records remain in the `Candidate_Sites` workbook sheet.
- Cluster labels apply only to the 60 `confirmed` Master records. Unconfirmed TNDC-006 is labeled `Excluded / not clustered`; Candidate sites are labeled `Candidate / not clustered`.

## Additions to the master workbook

- `Master`: 61 rows and 69 columns, with nearest-neighbor distance, cluster labels, and 26 external proxy variables added.
- `Candidate_Sites`: 16 rows and 49 columns, with `phase1_feature_status` documenting the completion method.
- Candidate status: 11 records calculated directly from their original coordinates, 2 Census address matches, 1 Census city representative point, 1 record sharing the TNCAND-009 site, and 1 record linked to TNDC-038. No feature rows are currently blank.

## External-field completeness

All 26 external fields have median and minimum coverage of 100.0%. CBP does not publish NAICS 51/54 industry rows for Meigs County, so TNDC-010 receives zero values marked `NO_PUBLISHED_ROW`; the same rule applies to other unpublished county-industry rows.

## Data sources

Official sources include HIFLD transmission lines, USGS NHD hydrography, Tennessee Statewide GIS major roads, NCES IPEDS 2024, Census CBP 2023, and Census TIGERweb county boundaries and address/city geocoding. See `source_catalog.csv` for full sources and limitations, `feature_data_dictionary.csv` for field definitions, and `feature_completeness.csv` for coverage.

All downloads were written to temporary directories; Phase 1 retains no external raw files.

## Use limitations

These variables support screening and description. Transmission-line distance does not indicate available capacity; hydrographic distance does not indicate water service or permits; degree completions do not indicate immediately available workers; and county employment does not represent a specific commuting area. Consistent statewide, site-level public data remain unavailable for substation capacity, electricity prices and interconnection queues, water capacity and water rights, and fiber routes and latency.
