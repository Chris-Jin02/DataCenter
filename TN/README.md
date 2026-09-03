# Tennessee Data Center Research

> First-stage geographic focus: Tennessee

This project assembles Tennessee data-center records and supporting spatial-analysis artifacts for a TN-first research workflow. It is maintained separately from the broader national framework in [`../DCUS/`](../DCUS/).

## Contents

- [`Tennessee_spatial_analysis.md`](Tennessee_spatial_analysis.md): research questions, analytical workflow, spatial methods, and validation strategy.
- [`dataset/tennessee_public_data_centers.xlsx`](dataset/tennessee_public_data_centers.xlsx): current Tennessee facility dataset.
- [`dataset/Tennessee Data Center Dataset Update and Compatibility Specification.md`](dataset/Tennessee%20Data%20Center%20Dataset%20Update%20and%20Compatibility%20Specification.md): dataset maintenance and compatibility specification.
- [`Map/tennessee_dcmap.html`](Map/tennessee_dcmap.html): generated interactive Tennessee facility map.
- [`Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb`](Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb): reproducible map-generation notebook.
- [`Map/template/TN_dcmap_template.html`](Map/template/TN_dcmap_template.html): HTML map template used by the notebook.

## Map workflow

Run the map-generation notebook from `TN/Map/`. Its dataset path is relative to that directory:

```python
DATA_FILE = Path("../dataset/tennessee_public_data_centers.xlsx")
```

## Scope note

The Tennessee dataset and analysis are active research artifacts. Source coverage, facility status, coordinates, and derived metrics should be revalidated before model training or publication.
