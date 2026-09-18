# Tennessee Data Center Research

> Current geographic focus: Tennessee

## Modeling progress

Updated September 14, 2026: [Phase 2](model/phase%202/README.md) is frozen and [Phase 3A](model/phase%203/README.md) has registered the model-input contract and spatial validation folds. Phase 3 model training has not started. The frozen Phase 2 cohorts are Primary 60, Weighted 74, and Strict 73; these modeling cohorts are distinct from inventory counts below. Earlier Proposal cohort counts and immediate-next-step text reflect an older planning snapshot.

This project maintains a public Tennessee data-center inventory, an interactive facility map, and a state-level spatial-analysis framework. The Tennessee workflow is kept separate from the broader national research materials in [`../DCUS/`](../DCUS/).

## Current Snapshot

Snapshot checked: September 8, 2026.

- **61 Master records**: 50 core data-center or interconnection records and 11 crypto-mining records.
- **16 Candidate records**: tracked separately from confirmed Master records.
- **75 unique analysis locations**: 61 Master locations plus 14 independent Candidate locations after linked and shared sites are reconciled.

Unknown values remain blank rather than being estimated. Candidate sites do not change confirmed-facility counts.

## Interactive Map

[Open the Tennessee data-center map](Map/tennessee_dcmap.html).

![Tennessee data center map](Map/tennessee_dcmap_preview.png)

*The image is a static preview. Use the interactive HTML map for the latest records, filters, facility details, and evidence links.*

See [`Map/README.md`](Map/README.md) for source attribution, the map legend, control instructions, and interpretation notes.

## Directory Contents

```text
TN/
├── README.md
├── Proposal/
│   └── Tennessee_spatial_analysis.md
├── dataset/
│   ├── tennessee_public_data_centers.xlsx
│   └── Tennessee Data Center Dataset Update and Compatibility Specification.md
├── model/
│   └── phase 1/
│       ├── 01_dc_geographic_clusters.ipynb
│       └── README.md
├── presentation/
│   ├── Tennessee_Data_Center_Current_Analysis.pptx
│   └── README.md
└── Map/
    ├── README.md
    ├── tennessee_dcmap.html
    ├── tennessee_dcmap_preview.png
    ├── TN_DC_Map_Generator.ipynb
    └── template/
        └── TN_dcmap_template.html
```

### Research and analysis

- [`Proposal/Tennessee_spatial_analysis.md`](Proposal/Tennessee_spatial_analysis.md) defines the research questions, analytical scope, spatial methods, and validation strategy.

### Dataset

- [`dataset/tennessee_public_data_centers.xlsx`](dataset/tennessee_public_data_centers.xlsx) contains the normalized Master inventory, candidate sites, source-aligned records, audits, and change history.
- [`dataset/Tennessee Data Center Dataset Update and Compatibility Specification.md`](dataset/Tennessee%20Data%20Center%20Dataset%20Update%20and%20Compatibility%20Specification.md) defines the schema and update rules.

### Analysis and presentation

- [`model/phase 1/README.md`](model/phase%201/README.md) documents the current geographic and feature-space analysis, data sources, and interpretation boundaries.
- [`presentation/README.md`](presentation/README.md) describes the updated 18-slide presentation and its data alignment.

### Map

- [`Map/README.md`](Map/README.md) provides source attribution, the legend, controls, and interpretation guidance.
- [`Map/tennessee_dcmap.html`](Map/tennessee_dcmap.html) is the generated interactive map.
- [`Map/TN_DC_Map_Generator.ipynb`](Map/TN_DC_Map_Generator.ipynb) generates the map from the workbook.
- [`Map/template/TN_dcmap_template.html`](Map/template/TN_dcmap_template.html) contains the map interface, styles, and filtering logic.
- [`Map/tennessee_dcmap_preview.png`](Map/tennessee_dcmap_preview.png) is the static repository preview.

## Updating the Map

Update the workbook first, preserve source URLs and stable IDs, and record material changes in `Change_Log`. Run `TN_DC_Map_Generator.ipynb` from `TN/Map/` to regenerate `tennessee_dcmap.html`.

## Scope

These files are active research artifacts based on publicly identifiable records. Coverage is not guaranteed to be complete. Facility status, ownership, capacity, and coordinates should be checked against the recorded evidence before publication or detailed spatial analysis.
