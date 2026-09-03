# DCUS and TN Repository Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the existing DataCenter repository into peer `DCUS/` and `TN/` projects, preserve history, and publish the Tennessee-first structure to the existing GitHub remote.

**Architecture:** Keep the existing `.git/` directory and `origin` at the repository root. Move the tracked national artifacts together under `DCUS/`, import only the curated Tennessee artifacts under `TN/`, and use a new root README as the portfolio entry point.

**Tech Stack:** Git, Markdown, Jupyter Notebook JSON, HTML, Microsoft Excel `.xlsx`

**Spec:** `docs/superpowers/specs/2026-09-03-dcus-tn-repository-reorganization-design.md`

## Global Constraints

- Preserve the existing `main` branch, commit history, and `git@github.com:Chris-Jin02/DataCenter.git` remote.
- Do not move, copy, print, stage, or commit files stored inside `.git/`, including deploy keys.
- Do not import `.DS_Store`, notebook checkpoints, caches, temporary files, application materials, or non-TN output directories.
- Do not rewrite scientific content or change the national notebooks' internal data relationships.
- Do not force-push or rewrite Git history.

---

### Task 1: Move the National Project into `DCUS/`

**Files:**
- Move: `README.md` to `DCUS/README.md`
- Move: `data/` to `DCUS/data/`
- Move: `figures/` to `DCUS/figures/`
- Move: `notebooks/` to `DCUS/notebooks/`
- Modify: `.gitignore`
- Create: `README.md`

**Interfaces:**
- Consumes: The tracked national project at repository root and the approved design spec.
- Produces: A self-contained `DCUS/` project plus a repository-level entry point.

- [ ] **Step 1: Capture the pre-move tracked-file inventory**

Run:

```bash
git ls-files README.md data figures notebooks | sort
git status --short --branch
```

Expected: the national README, data, figures, and two notebooks are listed; the working tree contains only approved planning-document changes.

- [ ] **Step 2: Move the national artifacts with Git history awareness**

Run:

```bash
mkdir DCUS
git mv README.md data figures notebooks DCUS/
```

Expected: Git reports the national files as renames under `DCUS/`; `.git/`, `.gitignore`, and `docs/` remain at repository root.

- [ ] **Step 3: Create the new repository README**

Use `apply_patch` to create `README.md` with this content:

````markdown
# Data Center Siting Research

This repository now follows a **Tennessee-first** research strategy. The active first-stage work focuses on building and analyzing a verified Tennessee data-center inventory, while the national framework remains available as a broader research foundation.

## Projects

### [TN — Tennessee Data Center Research](TN/)

The active first-stage project: Tennessee facility data, spatial-analysis design, and reproducible mapping artifacts.

### [DCUS — U.S. Data Center Siting](DCUS/)

The national research framework: U.S. site inventory, feature schema, feasibility rules, modeling benchmarks, and supporting visualizations.

## Repository layout

```text
.
├── TN/      # Active Tennessee-first project
├── DCUS/    # National research framework
└── docs/    # Repository design and implementation records
```

The projects share one Git history but retain separate geographic scopes and project documentation.
````

- [ ] **Step 4: Extend the shared ignore rules**

Use `apply_patch` to add `.DS_Store` to the root `.gitignore` without removing existing patterns.

- [ ] **Step 5: Verify the DCUS move**

Run:

```bash
test -f DCUS/README.md
test -f DCUS/data/raw/im3_us_data_center_locations.gpkg
test -f DCUS/data/raw/us_states_2025.geojson
test -f DCUS/notebooks/01_us_site_inventory_and_feature_schema.ipynb
test -f DCUS/notebooks/02_modeling_and_benchmark_design.ipynb
test -f DCUS/figures/us-site-distribution.svg
rg -n '\.\./data/raw/' DCUS/notebooks
rg -n 'figures/' DCUS/README.md
```

Expected: all `test` commands succeed; notebook data references and README figure references remain relative to files that moved together.

### Task 2: Import the Tennessee-First Project

**Files:**
- Create: `TN/README.md`
- Create: `TN/Tennessee_spatial_analysis.md`
- Create: `TN/Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb`
- Create: `TN/Map/tennessee_dcmap.html`
- Create: `TN/Map/template/TN_dcmap_template.html`
- Create: `TN/dataset/Tennessee Data Center Dataset Update and Compatibility Specification.md`
- Create: `TN/dataset/tennessee_public_data_centers.xlsx`

**Interfaces:**
- Consumes: Curated source artifacts from `/Users/steve/Project/UTK/outputs/Data center/TN/`.
- Produces: A GitHub-ready `TN/` project whose map notebook resolves the dataset through `../dataset/tennessee_public_data_centers.xlsx`.

- [ ] **Step 1: Create the TN directory structure**

Run:

```bash
mkdir -p TN/Map/template TN/dataset
```

- [ ] **Step 2: Copy the exact curated Tennessee artifacts**

Copy these source files to their corresponding destinations without copying directory metadata or hidden files:

```text
/Users/steve/Project/UTK/outputs/Data center/TN/Tennessee_spatial_analysis.md
/Users/steve/Project/UTK/outputs/Data center/TN/Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb
/Users/steve/Project/UTK/outputs/Data center/TN/Map/tennessee_dcmap.html
/Users/steve/Project/UTK/outputs/Data center/TN/Map/template/TN_dcmap_template.html
/Users/steve/Project/UTK/outputs/Data center/TN/dataset/Tennessee Data Center Dataset Update and Compatibility Specification.md
/Users/steve/Project/UTK/outputs/Data center/TN/dataset/tennessee_public_data_centers.xlsx
```

Use direct `cp` commands for these six existing artifacts because the notebook, HTML, and Excel files are generated or binary assets that must be preserved byte-for-byte.

- [ ] **Step 3: Verify byte-for-byte import integrity**

Run:

```bash
shasum -a 256 '/Users/steve/Project/UTK/outputs/Data center/TN/Tennessee_spatial_analysis.md' TN/Tennessee_spatial_analysis.md
shasum -a 256 '/Users/steve/Project/UTK/outputs/Data center/TN/Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb' TN/Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb
shasum -a 256 '/Users/steve/Project/UTK/outputs/Data center/TN/Map/tennessee_dcmap.html' TN/Map/tennessee_dcmap.html
shasum -a 256 '/Users/steve/Project/UTK/outputs/Data center/TN/Map/template/TN_dcmap_template.html' TN/Map/template/TN_dcmap_template.html
shasum -a 256 '/Users/steve/Project/UTK/outputs/Data center/TN/dataset/Tennessee Data Center Dataset Update and Compatibility Specification.md' 'TN/dataset/Tennessee Data Center Dataset Update and Compatibility Specification.md'
shasum -a 256 '/Users/steve/Project/UTK/outputs/Data center/TN/dataset/tennessee_public_data_centers.xlsx' TN/dataset/tennessee_public_data_centers.xlsx
```

Expected: each consecutive source/destination pair prints the same SHA-256 digest.

- [ ] **Step 4: Create the Tennessee project README**

Use `apply_patch` to create `TN/README.md` with this content:

````markdown
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
````

- [ ] **Step 5: Stage and inspect only intended TN files**

Run:

```bash
git add TN
git status --short
git ls-files TN | sort
git ls-files | rg '(^|/)\.DS_Store$'
```

Expected: exactly seven TN files are staged, including the new README; the `.DS_Store` query returns no results.

### Task 3: Validate, Commit, Push, and Confirm Synchronization

**Files:**
- Validate: `README.md`, `.gitignore`, `DCUS/**`, `TN/**`, `docs/**`
- Commit: all approved repository-reorganization changes
- Push: local `main` to `origin/main`

**Interfaces:**
- Consumes: Completed DCUS move, TN import, root documentation, and planning records.
- Produces: A validated Git commit published to the existing GitHub repository.

- [ ] **Step 1: Parse every Jupyter notebook as JSON**

Run:

```bash
python3 -m json.tool DCUS/notebooks/01_us_site_inventory_and_feature_schema.ipynb >/dev/null
python3 -m json.tool DCUS/notebooks/02_modeling_and_benchmark_design.ipynb >/dev/null
python3 -m json.tool TN/Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb >/dev/null
```

Expected: all three commands exit successfully.

- [ ] **Step 2: Validate the Tennessee Excel container and map dependency**

Run:

```bash
unzip -t TN/dataset/tennessee_public_data_centers.xlsx
test -f TN/Map/../dataset/tennessee_public_data_centers.xlsx
rg -n 'DATA_FILE = Path\("\.\./dataset/tennessee_public_data_centers\.xlsx"\)' TN/Map/Tennessee_DC_Map_Generator_Template_Workflow.ipynb
```

Expected: the Excel archive test reports no errors; the dataset exists at the notebook's relative path; the notebook contains the expected reference.

- [ ] **Step 3: Check repository hygiene and stale paths**

Run:

```bash
git diff --check
git ls-files | rg '(^|/)(\.DS_Store|__pycache__|\.ipynb_checkpoints)(/|$)'
rg -n 'outputs/Data center/TN|tmp/DataCenter' README.md DCUS TN --glob '*.md' --glob '*.ipynb'
```

Expected: `git diff --check` succeeds; no tracked metadata or cache paths are returned; no imported project documentation contains stale local source paths.

- [ ] **Step 4: Review the complete staged change**

Run:

```bash
git add .gitignore README.md DCUS TN docs
git status --short
git diff --cached --stat
git diff --cached --summary
```

Expected: existing national files appear as renames into `DCUS/`, Tennessee files appear as additions, and no file outside `.gitignore`, `README.md`, `DCUS/`, `TN/`, or `docs/` is staged.

- [ ] **Step 5: Commit the implementation**

Run:

```bash
git commit -m "refactor: organize DCUS and TN research projects"
```

Expected: one implementation commit is created on `main` after the earlier design and plan commits.

- [ ] **Step 6: Push the existing main branch**

Run:

```bash
git push origin main
```

Expected: Git reports that local `main` was pushed to `origin/main` without force.

- [ ] **Step 7: Verify final local and remote state**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
git log -3 --oneline --decorate
```

Expected: the worktree is clean, `main` is not ahead or behind `origin/main`, and `HEAD` equals `origin/main`.
