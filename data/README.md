# Data

This directory contains the small source files required to reproduce the proposal's U.S. map and inspect the IM3 location layers.

| File | Role | Upstream source | Notes |
|---|---|---|---|
| `raw/im3_us_data_center_locations.gpkg` | Point, building, and campus location layers used for entity-resolution analysis | [IM3 Open Source Data Center Atlas](https://github.com/IMMM-SFA/datacenter-atlas) | The layers do not share a project-level primary key. Preserve layer type and original identifiers. |
| `raw/us_states_2025.geojson` | State boundaries used to render the 50-state map | [U.S. Census TIGERweb](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer) | The study excludes the District of Columbia and Puerto Rico. |

## Data handling

- `raw/` contains unmodified source files. Do not overwrite them with derived features or model outputs.
- Record source vintage and access date when refreshing either file.
- Store future processed tables in a separate `data/processed/` directory and document every transformation.
- Do not interpret a missing source record as evidence that no data center exists in a state.

## Reuse

The repository does not grant a new license for these third-party data. Consult the upstream providers for authoritative licensing, attribution, and redistribution requirements.
