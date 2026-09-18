# Score dictionary

`final_score` is a D1-relative empirical-affinity percentile, not a probability of construction, capacity, or permit success.

| Field | Unit | Definition |
|---|---|---|
| `final_raw_score` | logit | Median selected-model score across 20 Primary draws |
| `final_score` | 0–100 | Percentile against the frozen 4,391-cell D1 reference |
| `score_p05`, `score_p95`, `score_iqr` | 0–100 | Distribution across the 20 draw-level D1-relative scores |
| `grid_regime`, `regime_distance`, `novelty_flag` | category / distance / boolean | D1-only PCA/KMeans context; not a suitability grade |

## Frozen input features

| Field | Unit | Definition |
|---|---|---|
| `dist_transmission_any_km` | km | Distance to nearest transmission line |
| `dist_transmission_100kv_km` | km | Distance to nearest line rated at least 100 kV |
| `dist_transmission_230kv_km` | km | Distance to nearest line rated at least 230 kV |
| `max_voltage_within_25km_kv` | kV | Maximum valid line voltage within 25 km |
| `transmission_owner_count_25km` | count | Distinct published transmission owners within 25 km |
| `dist_major_road_km` | km | Distance to nearest major road |
| `dist_interstate_km` | km | Distance to nearest Interstate |
| `dist_surface_water_flowline_km` | km | Distance to nearest NHD flowline |
| `named_flowlines_within_25km` | count | Distinct NHD flowline features within 25 km |
| `degree_institutions_50km` | count | IPEDS institutions within 50 km |
| `cip11_completions_50km` | count | CIP 11 completions within 50 km |
| `cip14_completions_50km` | count | CIP 14 completions within 50 km |
| `degree_institutions_100km` | count | IPEDS institutions within 100 km |
| `cip11_completions_100km` | count | CIP 11 completions within 100 km |
| `cip14_completions_100km` | count | CIP 14 completions within 100 km |
| `county_total_employment` | jobs | County total private employment |
| `county_total_establishments` | count | County total private establishments |
| `information_sector_employment` | jobs | County Information-sector employment |
| `information_sector_establishments` | count | County Information-sector establishments |
| `professional_scientific_employment` | jobs | County Professional, Scientific, and Technical Services employment |
| `professional_scientific_establishments` | count | County Professional, Scientific, and Technical Services establishments |
