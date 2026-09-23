# Tennessee Data Center Dataset Compatibility Specification

## Purpose

Keep future data additions compatible with the existing workbook, map, and analysis workflow. Extend the dataset without renaming, deleting, reordering, or repurposing existing columns.

## Files and sheet roles

- `tennessee_public_data_centers.xlsx`: primary dataset.
- `Master`: one row per normalized facility or campus; primary map and analysis input.
- `Raw_Aligned`: one row per source record; preserves source-level evidence.
- `Candidate_Sites`: possible sites that are not confirmed Master facilities.
- `Moratoriums`: one row per Tennessee jurisdiction policy event from the Interconnected Capital moratorium tracker; displayed as a separate map policy layer, not a facility, site, or model input.
- `Change_Log`: records material additions and updates.
- `Map/TN_DC_Map_Generator.ipynb`: reads `Master`, `Candidate_Sites`, and `Moratoriums` and generates the HTML map.

Add new rows directly below the relevant Excel table so formatting and dropdown rules expand with the table.

## Shared rules

- Use exact state code `TN`.
- Keep IDs and ZIP codes as text.
- Use WGS84 decimal coordinates.
- Fill latitude and longitude together, or leave both blank.
- Use true blanks for unknown values; do not enter `N/A`, `TBD`, `unknown`, or `-` in numeric fields.
- Separate multiple values and URLs with ` | `.
- Every `evidence_urls` item must be an `http://` or `https://` URL.
- Preserve source IDs, evidence URLs, and existing permanent facility IDs.
- Do not merge uncertain duplicate candidates automatically.

## `Raw_Aligned`

Required fields:

```text
source
source_record_id
facility_name
state
status_normalized
facility_type
evidence_urls
```

The pair `(source, source_record_id)` must be unique. Source-native measurement text may remain in Raw fields. Coordinates must be numeric when present. `included_in_master` must be an Excel Boolean (`TRUE` or `FALSE`).

## `Master`

Required map fields:

```text
facility_id
facility_name
operator
state
latitude
longitude
facility_type
analysis_scope
status_normalized
```

`facility_id` must be unique and stable. Normalized measurement fields must contain numbers or blanks only. A row with no coordinates remains in the dataset but is not plotted.

Allowed values:

```text
status_normalized: operational | under_construction | proposed | expanding | cancelled
facility_type: data_center | interconnection_facility | crypto_mining
analysis_scope: core_data_center | crypto_mining
location_precision: exact | address_or_site | approximate_site | approximate | area_or_city
location_confidence: high | medium | low
```

Required type relationship:

```text
data_center -> core_data_center
interconnection_facility -> core_data_center
crypto_mining -> crypto_mining
```

## `Candidate_Sites`

Required fields:

```text
candidate_id
candidate_site_name
candidate_type
candidate_confidence
state
evidence_urls
```

`candidate_id` must be unique. `candidate_confidence` is `high`, `medium`, or `low`. Coordinates may both be blank; such candidates remain listed but are not plotted. A supplied `master_facility_id` must reference an existing Master record.

## `Moratoriums`

Required fields:

```text
moratorium_id
record_type
jurisdiction
state
jurisdiction_level
event_date
duration_text
status
scope
reason
source_name
source_url
tracker_url
tracker_last_updated
source_record_key
linked_facility_or_candidate_id
link_basis
verification_status
latitude
longitude
location_reference
location_precision
coordinate_source
location_semantics
```

`moratorium_id` and `source_record_key` must each be unique. `event_date` and `tracker_last_updated` are dates. Use `TN` as the state code. Preserve tracker text in the duration, scope, and reason fields; preserve source and tracker URLs exactly. A jurisdiction-wide policy record does not create or infer a facility relationship. Use `not_linked` and explain the reason in `link_basis` when a source does not establish a one-to-one connection to a `Master` or `Candidate_Sites` row. When evidence explicitly names a project or establishes a policy context, a linked Master ID is permitted only with a `link_basis` that labels the relationship as `named policy-trigger project` or `policy-context relationship`; neither label implies that a jurisdiction-wide action applies only to that project.

Moratorium coordinates are mandatory policy-reference points in WGS84 decimal degrees. `location_reference` identifies a jurisdiction government center or municipal-area proxy, `location_precision` is `address_or_site` or `area_or_city`, and `coordinate_source` is the auditable public map URL. `location_semantics` must state that the point is not a data-center site. Display these points only in the map's policy layer; do not use them as facility or candidate-site coordinates.

## Update workflow

1. Add the source record to `Raw_Aligned`.
2. Search existing Master and Candidate records before creating a new ID.
3. Update an existing Master row when evidence refers to the same facility; never replace its ID.
4. Add uncertain or unbuilt sites to `Candidate_Sites` instead of forcing them into Master.
5. Preserve provenance and record material changes in `Change_Log`.
6. Add policy-event records to `Moratoriums` rather than facility tabs when the source describes a jurisdiction action.
7. Run `TN_DC_Map_Generator.ipynb` and confirm the HTML map is generated and its filters work after any facility, candidate, or moratorium update.

When uncertain, preserve the current schema and evidence rather than increasing record count.
