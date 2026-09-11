# Tennessee Data Center Geographic and Feature Clustering

Status date: 2026-09-08.

## Data structure

The source workbook remains in `TN/dataset/tennessee_public_data_centers.xlsx`; no raw workbook is copied into `model`.

- `Master`: 61 records and 61 unique `facility_id` values. The table includes 28 analysis fields for nearest-neighbor distance, cluster labels, and external context proxies.
- `Candidate_Sites`: 16 Candidate records with the same analysis fields and a `phase1_feature_status` field.
- Candidate handling: 11 records use existing coordinates; TNCAND-005 and TNCAND-017 use Census address matching; TNCAND-006 uses a Census Nashville-Davidson representative point; TNCAND-010 shares ORNL site features with TNCAND-009; and TNCAND-012 inherits the linked TNDC-038 location. All 16 Candidate records have analysis features.
- `results/site_feature_matrix.csv`: 75 unique analytical locations, comprising 61 Master locations and 14 Candidate locations not merged into Master. TNCAND-006 uses a city representative point and therefore carries market-level estimates.

## Notebook

`01_dc_geographic_clusters.ipynb` retains a geographic baseline for 60 confirmed Master records, runs expanded geographic clustering for 75 unique locations, clusters 21 numerical external-context fields, and reports sensitivity comparisons, group profiles, quantitative separation measures, and manual analysis. Run it from `model/phase 1`.

## Main findings

The geographic baseline uses DBSCAN with `eps=20 km` and `min_samples=3`. Of 60 confirmed locations, Memphis 11, Nashville 19, Chattanooga 4, and Knoxville/Lenoir City 7 belong to four groups; 19 locations are isolated or belong to small groups.

Using the same parameters for 75 unique locations yields five groups: Memphis 13, Jackson 3, Nashville 25, Chattanooga 5, and Knoxville 10. Nineteen locations remain isolated or in small groups. On the original 60 baseline locations, the expanded result has an Adjusted Rand Index of 0.92 and a clustered-pair Jaccard score of 0.93 relative to the baseline.

Feature clustering uses 21 numerical fields from 26 external fields; county names, FIPS, and three CBP disclosure flags are retained for interpretation but excluded from distance calculations. After `log1p` and `RobustScaler`, KMeans selects K=2 with silhouette 0.388. F1 contains 20 locations with smaller employment markets and less accessible infrastructure proxies; F2 contains 55 locations with higher metropolitan employment and talent-access proxies. These are environmental-similarity groups, not suitability grades.

All 26 external fields have complete coverage in the 75-row matrix. CBP does not publish NAICS 51/54 rows for Meigs County; TNDC-010 employment and establishment counts are recorded as 0 and distinguished with `NO_PUBLISHED_ROW` rather than a Census noise flag.

`results/interactive_clusters.html` is an offline single-file map with embedded SVG, Tennessee geometry, and all 75 locations. It supports geographic/feature mode switching, role filters, hover, click details, zoom, pan, and reset. The bottom of the map first presents the active mode's cluster guide and then the method and marker-shape explanation. Clicking a marker displays the site, city, record role, geographic and feature clusters, facility type, status, and coordinate precision; the event does not change cluster assignment or trigger map panning.

## Interpretation boundary

These fields support screening and group comparison. Transmission proximity does not establish remaining capacity or interconnection conditions; water proximity does not establish water capacity, rights, or permits; IPEDS completions do not establish immediately available labor; and CBP measures county workplace employment. Comparable statewide, site-level public data for substation capacity, tariffs, interconnection queues, water capacity and permits, and fiber routing or latency remain unavailable and are not imputed.
