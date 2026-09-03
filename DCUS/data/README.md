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

## External outcome-label sources not vendored here

The proposal references the following live sources for project discovery, event histories, final-decision evidence, or policy context. No new third-party snapshot from these providers is committed to this repository.

| Source | Intended use | Access |
|---|---|---|
| FracTracker Open U.S. Data Centers Tracker | Master candidate project inventory, status, project attributes, and source links | [Project page](https://fractracker.org/data-centers/), [public sheet](https://docs.google.com/spreadsheets/d/1JJ6kcVo-NjlAYtznwHOki2DVl4WWV6lhy-eXhFCdKKU/edit?gid=386766486#gid=386766486), [data dictionary](https://docs.google.com/spreadsheets/d/1KVab4niu8X_GGne3WyyH_CdTP9Bt4uJSe6iK0fu9C48/edit?usp=sharing) |
| Tracking American AI Data Center Buildout | Dated opposition, permit-denial, withdrawal, and related actions | [Site](https://datacentertracker.org/), [JSON export](https://datacentertracker.org/data/fights.json) |
| Data Center Watch | Confirmed and blocked-project leads | [Report](https://www.datacenterwatch.org/report) |
| Aterio | Commercial facility and development coverage check | [U.S. overview](https://www.aterio.io/insights/us-data-centers), [dataset](https://www.aterio.io/datasets/lst_us_data_centers) |
| Shovels.ai | Permit and construction-signal discovery | [API](https://www.shovels.ai/solutions/api), [data-center permit analysis](https://www.shovels.ai/blog/data-center-permits-decisions/) |
| UVA Data Center Policy Database | Jurisdiction-time policy context | [Database](https://www.datacenterpolicy.com/), [project page](https://dtdlab.virginia.edu/project/data-center-policies/) |
| dcmap.us Policy Tracker | Policy, moratorium, and local-document discovery | [Policy tracker](https://dcmap.us/insights/policy/) |

These sources generate candidate records and evidence leads, not automatic labels. A strict negative requires a dated final official denial that was not later overturned. Cancelled, withdrawn, suspended, delayed, and pending projects remain separate outcomes.

## Reuse

The repository does not grant a new license for these third-party data. DataCenterTracker declares CC BY 4.0 for its export and IM3 identifies ODbL terms. FracTracker's download and attribution guidance should be reconciled with its website terms before redistributing a complete snapshot. Commercial sources should not be copied into the repository without explicit research and redistribution rights.
