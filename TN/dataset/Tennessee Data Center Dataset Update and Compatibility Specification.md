# Tennessee Data Center Dataset Update and Compatibility Specification

## 1. Purpose

This specification defines how the Tennessee Data Center dataset must be updated, expanded, validated, and maintained.

The dataset is designed to support multiple downstream workflows without requiring repeated code changes, including:

- Interactive map generation
- Spatial analysis
- Statistical analysis
- Machine learning
- Deep learning
- Feature engineering
- Model evaluation
- Future dataset expansion

The highest priority is **schema stability and backward compatibility**.

Any AI agent, researcher, script, or automated process modifying the dataset MUST follow this specification.

---

# 2. Primary Compatibility Rule

The dataset MUST remain backward compatible with existing downstream scripts.

After the dataset is updated, the following workflow should continue to work without modifying the map-generation or model-loading code:

```text
Data.xlsx
    ↓
Master
    ↓
Existing preprocessing code
    ↓
Map / ML / DL pipeline
```

Therefore:

**DO NOT rename, delete, repurpose, or change the data type or semantic meaning of an existing core column.**

New columns MAY be added.

Existing columns MUST remain available.

---

# 3. Stable Input Interface

The default project structure is:

```text
project/
├── Data.xlsx
├── template.html
├── map_generator.ipynb
├── training/
└── outputs/
```

The primary dataset file should be:

```text
Data.xlsx
```

The primary analysis table MUST remain:

```text
Master
```

Downstream code should be able to rely on:

```python
DATA_FILE = Path("Data.xlsx")
DATA_SHEET = "Master"
```

Do not rename `Master` without an explicit schema migration.

---

# 4. Master Table Is the Stable Data Contract

The `Master` sheet is the canonical facility-level dataset.

Each row represents one deduplicated physical facility or physically coherent campus.

The `Master` table is the interface used by:

- Map generation
- ML preprocessing
- Feature engineering
- Spatial modeling
- Statistical analysis

Raw source records may change structure internally, but the Master interface MUST remain stable.

---

# 5. Core Columns Must Never Be Removed

The following columns are considered core compatibility fields:

```text
facility_id
facility_name
operator
operators
address
city
county
state
postal_code
latitude
longitude
location_precision
location_confidence
coordinate_source_record
coordinate_max_spread_km
coordinate_conflict_flag
status_normalized
status_values
status_conflict_flag
facility_type
facility_type_values
analysis_scope
capacity_mw
square_feet
property_acres
investment_usd
sources
source_count
record_count
source_record_ids
evidence_urls
last_updated
```

These columns MUST remain present even when some values are missing.

If no value is available, use a missing value.

Do NOT remove the column.

---

# 6. Existing Column Names Are Immutable

Do NOT rename columns.

For example, never change:

```text
capacity_mw
```

to:

```text
power
power_mw
capacity
it_capacity
```

Never change:

```text
latitude
longitude
```

to:

```text
lat
lon
```

The HTML generator may internally convert them to `lat` and `lon`, but the dataset schema must retain:

```text
latitude
longitude
```

---

# 7. Existing Column Semantics Are Immutable

A column must retain the same meaning across dataset versions.

For example:

```text
capacity_mw
```

must continue to represent documented facility/campus capacity in MW according to the established normalization rule.

Do not later reuse this column for:

- Estimated power
- Utility service capacity
- Transformer capacity
- Modeled capacity
- Average power demand

If a new concept is required, create a new column.

Example:

```text
capacity_mw
estimated_capacity_mw
utility_capacity_mw
```

Do not overwrite the original semantic meaning.

---

# 8. New Columns Are Allowed

New columns MAY be added when new information becomes available.

This is the preferred way to extend the dataset.

For example:

```text
water_use_mgd
electric_utility
substation_distance_km
fiber_distance_km
land_price_usd_acre
population_density
flood_risk
elevation_m
estimated_capacity_mw
```

Adding columns is preferred over modifying existing columns.

Existing map code and model-loading code should ignore unknown columns unless explicitly needed.

---

# 9. New Columns Should Be Added Without Breaking Existing Columns

When extending the dataset:

```text
OLD COLUMNS
+
NEW COLUMNS
```

is acceptable.

The following is NOT acceptable:

```text
OLD COLUMNS
→ renamed columns
→ changed units
→ changed categories
```

Schema evolution should be additive whenever possible.

---

# 10. Facility IDs Must Be Permanent

`facility_id` is the stable primary identifier.

Recommended format:

```text
TNDC-001
TNDC-002
TNDC-003
```

Once assigned, a `facility_id` MUST NOT change.

Do not renumber records after:

- Adding a facility
- Removing a facility
- Sorting the table
- Changing facility names
- Changing operators
- Updating lifecycle status

Example:

If the dataset currently ends at:

```text
TNDC-045
```

the next facility should normally receive:

```text
TNDC-046
```

Do not fill historical ID gaps unless there is a specific reason.

---

# 11. Facility ID Must Not Encode Model Labels

Do not encode:

- Lifecycle
- Facility type
- County
- Operator
- Capacity
- Training class

inside `facility_id`.

The ID must remain a neutral persistent identifier.

This prevents future ML pipelines from accidentally learning information from identifiers.

---

# 12. Row Order Must Not Carry Meaning

Downstream analysis MUST NOT depend on row position.

The first row, second row, or Excel row number must never represent facility identity.

Use:

```text
facility_id
```

for identity.

The dataset may be sorted differently in future versions without changing meaning.

---

# 13. Geographic Scope

Include physical facilities located in:

```text
Tennessee, United States
```

Required normalized state value:

```text
TN
```

Do not include a facility solely because:

- The operator is headquartered in Tennessee
- The company has an office in Tennessee
- A mailing address is in Tennessee

The physical infrastructure must be located in Tennessee.

---

# 14. Coordinate Contract

The following fields MUST remain numeric:

```text
latitude
longitude
```

Coordinate reference system:

```text
WGS84 / EPSG:4326
```

Example:

```text
latitude = 36.62078
longitude = -87.26220
```

Do not change the coordinate system inside the Master table.

Do not store projected coordinates in these fields.

If another CRS is needed, create new columns.

---

# 15. Missing Coordinate Rule

If no defensible coordinate is available:

```text
latitude = null
longitude = null
```

Do not fabricate coordinates.

Do not use:

- Tennessee centroid
- County centroid
- ZIP centroid
- City centroid

without explicitly recording the resulting precision.

Facilities without valid coordinates may remain in the dataset but will naturally be excluded from point-map rendering.

---

# 16. Location Precision Vocabulary

Use the existing normalized values:

```text
exact
address_or_site
approximate_site
approximate
area_or_city
```

Do not introduce spelling variations such as:

```text
Exact
exact_location
city
approx
site
```

without first updating the schema specification.

Stable categorical vocabularies are important for ML preprocessing.

---

# 17. Location Confidence Vocabulary

Recommended values:

```text
high
medium
low
```

Do not mix numeric and textual confidence formats in the same field.

For example, do not mix:

```text
high
0.8
80%
```

inside `location_confidence`.

If numeric confidence is later required, create:

```text
location_confidence_score
```

as a separate field.

---

# 18. Facility Type Contract

Allowed primary values:

```text
data_center
interconnection_facility
crypto_mining
```

Do not change these strings.

Do not use:

```text
Data Center
datacenter
dc
crypto
bitcoin
IX
```

inside the normalized field.

Source-specific terminology may be stored in:

```text
facility_type_values
```

---

# 19. Analysis Scope Contract

Maintain the following relationship:

```text
data_center
→ core_data_center

interconnection_facility
→ core_data_center

crypto_mining
→ crypto_mining
```

Therefore:

```text
Core Dataset
=
data_center
+
interconnection_facility
```

and:

```text
Expanded Dataset
=
core_data_center
+
crypto_mining
```

This distinction MUST remain stable so that existing analysis and future model experiments remain reproducible.

---

# 20. Lifecycle Vocabulary

Allowed normalized values:

```text
operational
under_construction
proposed
expanding
cancelled
```

Do not introduce capitalization or formatting variants.

Incorrect:

```text
Operational
Under Construction
construction
planned
active
```

Normalize source terminology into the existing controlled values.

Original source terminology can remain in:

```text
status_values
```

---

# 21. Do Not Recode Historical Categories Without Reason

If a new source uses different terminology, map it into the existing controlled vocabulary whenever possible.

Example:

```text
Source:
"planned"

Normalized:
proposed
```

Do NOT create a new category merely because a source uses a different word.

This is essential for keeping trained ML encoders compatible with future dataset versions.

---

# 22. Missing Values

Unknown values MUST remain missing.

Preferred semantic rule:

```text
unknown ≠ zero
```

Examples:

Unknown capacity:

```text
capacity_mw = null
```

Not:

```text
capacity_mw = 0
```

Unknown investment:

```text
investment_usd = null
```

Not:

```text
investment_usd = 0
```

Unknown square footage:

```text
square_feet = null
```

This distinction is critical for machine-learning preprocessing.

---

# 23. Do Not Use Placeholder Strings for Missing Numeric Data

Do not store the following inside numeric columns:

```text
Unknown
N/A
NA
None
-
TBD
Not available
```

Numeric columns should contain:

```text
number
```

or:

```text
null
```

This prevents dtype instability in Python and ML pipelines.

---

# 24. Numeric Units Must Remain Stable

The following units are fixed:

```text
capacity_mw → megawatts
square_feet → square feet
property_acres → acres
investment_usd → U.S. dollars
latitude → decimal degrees
longitude → decimal degrees
```

Do not mix units.

Example:

Do not sometimes store capacity in:

```text
kW
```

and sometimes in:

```text
MW
```

inside `capacity_mw`.

Convert all values to MW before storage.

---

# 25. Boolean Fields Must Remain Boolean-Compatible

Fields such as:

```text
coordinate_conflict_flag
status_conflict_flag
```

should use consistent Boolean semantics:

```text
True
False
```

or Excel-compatible Boolean values.

Do not mix:

```text
Yes
No
Y
N
1
0
True
False
```

within the same field.

---

# 26. Evidence Must Be Preserved

Every facility should retain provenance.

Important fields include:

```text
sources
source_count
record_count
source_record_ids
evidence_urls
coordinate_source_record
```

Do not remove provenance merely because a normalized value has already been created.

The dataset must remain auditable.

---

# 27. Evidence URL Format

Multiple URLs in:

```text
evidence_urls
```

should remain separated using:

```text
 | 
```

Example:

```text
https://source1.com | https://source2.com
```

The existing map-generation script expects this format and converts it into a URL list.

Do not switch to:

- JSON arrays
- commas
- semicolons
- newline-separated URLs

without updating the schema version and downstream parser.

---

# 28. Sources Field Format

The normalized source field should continue using:

```text
source_a | source_b | source_c
```

Example:

```text
compute_atlas | peeringdb
```

Maintain consistent source naming.

Avoid variants such as:

```text
PeeringDB
peering db
peeringdb.com
```

when the normalized source identifier is:

```text
peeringdb
```

---

# 29. Deduplication Must Preserve Master Identity

Before adding a facility, search for possible matches using:

- `facility_id`
- Facility name
- Operator
- Address
- Coordinates
- City
- County
- Campus
- Project name
- Evidence URLs

If the evidence describes an existing physical facility, update that Master entity.

Do not create a new facility merely because a new source was found.

---

# 30. Facility Updates Must Not Automatically Create New Rows

The following are normally updates to an existing facility:

- New capacity information
- New status information
- Operator change
- Facility rename
- New evidence URL
- Better coordinates
- Improved address
- Expansion announcement

Create a new Master entity only when evidence supports a distinct physical facility or independently identifiable site.

---

# 31. Existing Data Should Not Be Silently Overwritten

When new evidence conflicts with an existing value, evaluate the conflict.

Use the relevant conflict fields where appropriate:

```text
coordinate_conflict_flag
status_conflict_flag
```

Do not silently replace a credible value simply because a newer website provides a different number.

---

# 32. Raw Evidence and Master Data Must Remain Distinguishable

The preferred architecture is:

```text
Raw source records
        ↓
Normalization
        ↓
Entity resolution
        ↓
Master
        ↓
Map / ML / Analysis
```

Raw source records preserve source-specific information.

`Master` contains normalized, deduplicated facility entities.

Do not directly treat unreviewed raw rows as independent training observations.

---

# 33. Map Compatibility Requirements

The existing map pipeline depends on the following fields:

```text
facility_id
facility_name
operator
address
city
county
state
postal_code
latitude
longitude
location_precision
location_confidence
status_normalized
facility_type
analysis_scope
capacity_mw
square_feet
property_acres
investment_usd
sources
source_count
last_updated
evidence_urls
```

Future dataset updates MUST preserve these fields.

Additional columns are allowed.

The map generator should not require modification when new facilities are added.

---

# 34. Training Compatibility Requirements

ML/DL workflows should consume stable raw variables from `Master`.

Future data updates MUST NOT unexpectedly change:

- Field names
- Units
- Category definitions
- Missing-value semantics
- ID semantics
- Coordinate system
- Boolean encoding

These changes could silently invalidate trained preprocessing pipelines.

---

# 35. Separate Raw Features From Derived Features

Observed variables and model-derived variables should not be mixed without clear naming.

Examples of observed variables:

```text
capacity_mw
property_acres
latitude
longitude
county
operator
```

Examples of derived variables:

```text
distance_to_substation_km
distance_to_fiber_km
population_density_5km
nearest_highway_km
grid_density
cluster_label
```

Derived features should use separate clearly named columns or separate feature tables.

---

# 36. Do Not Store Model Predictions as Ground Truth

Predicted values must never overwrite observed dataset fields.

Incorrect:

```text
capacity_mw = model_prediction
```

Correct:

```text
capacity_mw
predicted_capacity_mw
```

Similarly:

```text
facility_type
predicted_facility_type
```

must remain separate.

---

# 37. Prevent Target Leakage

Features generated for ML must not contain information that directly reveals the target unless intentionally part of the experimental design.

Examples of potentially dangerous features include:

- Labels derived from the target itself
- Post-construction variables used to predict construction
- Future status information used to predict historical status
- Facility IDs encoding category information

Feature generation should record the temporal relationship between predictors and prediction targets when necessary.

---

# 38. Dataset Versioning

Additive version tracking is recommended.

Suggested fields or metadata:

```text
schema_version
dataset_version
```

Example:

```text
schema_version = 1.0
dataset_version = 2026-09-03
```

`schema_version` changes only when the structural contract changes.

`dataset_version` may change whenever records are updated.

---

# 39. Schema Version Rules

Examples:

Adding a new optional column:

```text
schema_version:
1.0 → 1.1
```

Changing the meaning of an existing field:

```text
requires a major migration
1.x → 2.0
```

Renaming or deleting existing columns should be avoided.

If unavoidable, create a migration layer so older code can still obtain the previous fields.

---

# 40. Backward-Compatible Schema Evolution

Preferred:

```text
Version 1:
A B C

Version 2:
A B C D

Version 3:
A B C D E
```

Avoid:

```text
Version 1:
A B C

Version 2:
A renamed_B C

Version 3:
A C
```

Dataset evolution should be additive.

---

# 41. Change Log

Every material dataset update should ideally record:

```text
date
facility_id
action
field_changed
old_value
new_value
evidence
reason
```

Recommended actions:

```text
ADD
UPDATE
MERGE
EXCLUDE
CORRECT
```

This may be maintained in a separate sheet such as:

```text
Change_Log
```

The map and training pipeline do not need to consume this sheet.

---

# 42. New Facility Workflow

For every candidate facility:

1. Verify that it represents physical infrastructure.
2. Verify that it is located in Tennessee.
3. Collect public evidence.
4. Search the existing Master dataset.
5. Evaluate duplicate candidates.
6. Determine facility type.
7. Determine analysis scope.
8. Determine lifecycle status.
9. Determine operator.
10. Determine the best supported location.
11. Assign location precision.
12. Extract numeric values only when supported.
13. Preserve provenance.
14. Assign a new permanent `facility_id`.
15. Append the new Master entity without modifying existing IDs.

---

# 43. Existing Facility Update Workflow

For new evidence about an existing facility:

1. Match the evidence to the existing `facility_id`.
2. Determine which fields are genuinely updated.
3. Preserve prior provenance.
4. Resolve conflicts conservatively.
5. Update the normalized Master values.
6. Keep the same `facility_id`.
7. Update `last_updated`.
8. Do not modify unrelated fields.

---

# 44. AI Agent Output Contract

An AI supplementing the dataset should propose structured changes rather than silently rewriting the dataset.

Recommended output:

```text
action:
facility_id:
facility_name:

field_updates:
  field_name:
    old_value:
    proposed_value:
    evidence:
    confidence:

new_evidence_urls:
duplicate_candidates:
review_required:
review_note:
```

Allowed actions:

```text
ADD
UPDATE
MERGE_CANDIDATE
REVIEW
EXCLUDE
```

An AI should not automatically perform uncertain merges.

---

# 45. Compatibility Validation Before Saving

Before an updated dataset is accepted, validate:

```text
Master sheet exists
```

Required columns exist.

`facility_id` is unique.

No existing `facility_id` was unintentionally changed.

Latitude and longitude are numeric.

Coordinates remain EPSG:4326.

Normalized category values follow the controlled vocabulary.

Numeric columns do not contain text placeholders.

Unknown numeric values remain null.

Existing units remain unchanged.

Evidence URLs retain the expected separator.

No required column was deleted.

New columns do not overwrite existing semantics.

---

# 46. Map Regression Test

After updating `Data.xlsx`, run the existing map-generation notebook without changing its code.

The update passes the map compatibility test only if:

```text
Data.xlsx
+
template.html
+
existing map notebook
```

successfully generates the HTML.

Check that:

- All valid-coordinate facilities appear
- Crypto filtering works
- Lifecycle filtering works
- Operator filtering works
- MW filtering works
- Search works
- Popups render
- Evidence links render
- Tennessee boundary renders

The dataset should be corrected before modifying the map generator merely to accommodate inconsistent data.

---

# 47. ML Regression Test

Before using a new dataset version for training, verify:

- Required feature columns still exist.
- Existing categorical values remain valid.
- Numeric dtypes remain numeric.
- Missing-value behavior remains consistent.
- IDs remain stable.
- No target field has been unintentionally modified.
- No new field creates obvious target leakage.
- Existing preprocessing code can load the dataset.

The preferred behavior is:

```text
old training pipeline
+
new Data.xlsx
=
successful preprocessing
```

---

# 48. New Categories Require Explicit Review

Do not automatically create new values for:

```text
facility_type
analysis_scope
status_normalized
location_precision
location_confidence
```

If existing vocabularies cannot represent a new real-world case, flag:

```text
SCHEMA_REVIEW_REQUIRED
```

before introducing the new category.

This prevents unexpected ML encoding failures.

---

# 49. New Feature Policy

New research features are encouraged, but they should be added without breaking the Master contract.

Preferred pattern:

```text
Master
+
new optional columns
```

or:

```text
Master
+
separate Feature_Table
```

For large derived feature sets, a separate table keyed by:

```text
facility_id
```

is preferable.

Example:

```text
ML_Features

facility_id
distance_to_substation_km
distance_to_highway_km
population_density
water_stress
elevation
...
```

This keeps source observations separate from modeling features.

---

# 50. Join Key for Future Tables

Any additional facility-level table should use:

```text
facility_id
```

as the primary join key.

Example:

```text
Master
      facility_id
           ↓
ML_Features
           ↓
Environmental_Features
           ↓
Infrastructure_Features
```

Do not join tables primarily using facility name because names may change.

---

# 51. Temporal Data

If historical or longitudinal analysis is added later, do not overwrite historical observations.

Prefer a separate table such as:

```text
Facility_History
```

with:

```text
facility_id
observation_date
status
capacity_mw
operator
source
```

The `Master` table should continue to represent the current normalized facility view.

---

# 52. Exclusion Policy

Records that are excluded from the Master dataset should not necessarily be deleted from the project.

Potentially useful rejected records may remain in:

```text
Excluded_Support
```

with a reason.

Examples:

```text
duplicate
outside_tennessee
office_only
insufficient_evidence
not_data_center
supporting_infrastructure_only
```

This prevents future AI agents from repeatedly rediscovering and re-adding rejected records.

---

# 53. AI Must Prefer Compatibility Over Convenience

An AI MUST NOT change the schema merely because another structure would be easier for the current task.

Before modifying any existing field, ask:

```text
Will this break an existing map, preprocessing script, model, or join?
```

If yes, prefer adding a new field or compatibility layer instead.

---

# 54. Strict Prohibited Actions

An AI MUST NOT:

- Rename existing core columns.
- Delete existing core columns.
- Reassign existing facility IDs.
- Reuse deleted facility IDs for new facilities.
- Change units inside existing numeric columns.
- Mix strings into numeric columns.
- Replace missing numeric values with zero.
- Fabricate coordinates.
- Fabricate MW values.
- Fabricate URLs.
- Fabricate operators.
- Create uncontrolled category spellings.
- Merge uncertain entities automatically.
- Overwrite observed values with model predictions.
- Store projected coordinates in latitude/longitude.
- Modify existing field semantics without schema migration.
- Add new normalized categories without review.

---

# 55. Recommended Validation Logic for AI Agents

Before returning an updated dataset, an AI should conceptually verify:

```python
assert "Master" exists

assert facility_id is unique

assert required_columns exist

assert latitude is numeric or null
assert longitude is numeric or null

assert facility_type in allowed_facility_types
assert analysis_scope in allowed_analysis_scopes
assert status_normalized in allowed_statuses
assert location_precision in allowed_location_precision_values

assert capacity_mw is numeric or null
assert square_feet is numeric or null
assert property_acres is numeric or null
assert investment_usd is numeric or null
```

The validation should fail rather than silently coercing clearly invalid records.

---

# 56. Controlled Vocabulary

## `facility_type`

```text
data_center
interconnection_facility
crypto_mining
```

## `analysis_scope`

```text
core_data_center
crypto_mining
```

## `status_normalized`

```text
operational
under_construction
proposed
expanding
cancelled
```

## `location_precision`

```text
exact
address_or_site
approximate_site
approximate
area_or_city
```

## `location_confidence`

```text
high
medium
low
```

These vocabularies must remain stable unless an explicit schema revision is approved.

---

# 57. Compatibility Priority

When making future updates, use the following priority:

```text
1. Data correctness
2. Provenance
3. Backward compatibility
4. Stable semantics
5. Reproducibility
6. ML readiness
7. Dataset completeness
8. Record count
```

Never increase dataset size at the expense of schema stability or evidence quality.

---

# 58. Governing Rule

The dataset must behave as a long-lived research data interface, not as a one-time spreadsheet.

Every update should satisfy:

```text
New evidence
    ↓
Data update
    ↓
Same schema contract
    ↓
Existing map still works
    ↓
Existing preprocessing still works
    ↓
Future models can use the expanded data
```

The preferred rule is:

**extend the dataset, do not break the dataset.**

When uncertain, preserve the existing schema and add information rather than modifying established interfaces.