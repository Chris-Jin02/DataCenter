# DCUS and TN Repository Reorganization Design

## Objective

Reorganize the existing `Chris-Jin02/DataCenter` repository into a single repository with two peer project directories. Preserve the existing national research as `DCUS/` and publish the Tennessee-first work as `TN/` without rewriting Git history.

## Target Structure

```text
DataCenter/
├── .git/
├── .gitignore
├── README.md
├── docs/
│   └── superpowers/
│       ├── plans/
│       └── specs/
├── DCUS/
│   ├── README.md
│   ├── data/
│   ├── figures/
│   └── notebooks/
└── TN/
    ├── README.md
    ├── Tennessee_spatial_analysis.md
    ├── Map/
    │   ├── Tennessee_DC_Map_Generator_Template_Workflow.ipynb
    │   ├── tennessee_dcmap.html
    │   └── template/
    │       └── TN_dcmap_template.html
    └── dataset/
        ├── Tennessee Data Center Dataset Update and Compatibility Specification.md
        └── tennessee_public_data_centers.xlsx
```

The repository root becomes a portfolio-level entry point. `DCUS/` and `TN/` remain independently understandable research directories, while sharing one Git history and one GitHub remote.

## Existing National Project Migration

Move the currently tracked national-project files into `DCUS/` using Git-aware moves:

- `README.md` becomes `DCUS/README.md`.
- `data/` becomes `DCUS/data/`.
- `figures/` becomes `DCUS/figures/`.
- `notebooks/` becomes `DCUS/notebooks/`.

The national notebooks currently resolve data through paths relative to `notebooks/`, such as `../data/raw/...`. Because `data/` and `notebooks/` move together under `DCUS/`, those internal paths remain valid. Markdown image links in the national README also remain valid because `figures/` moves with the README.

## Tennessee Project Import

Copy the project content from the local source directory `outputs/Data center/TN/` into the repository's new `TN/` directory. Include the research analysis, map notebook, generated map, map template, dataset specification, and Excel dataset.

Do not import macOS metadata, notebook checkpoints, caches, temporary build directories, or files outside the Tennessee source directory. The auxiliary planning documents currently stored outside the Git repository are not part of this import because they reference an unimplemented earlier directory layout.

Create `TN/README.md` as the Tennessee project entry point. It will state the TN-first scope, describe the checked-in artifacts, and explain that the map-generation notebook expects to run from `TN/Map/`, where its existing `../dataset/tennessee_public_data_centers.xlsx` path remains valid.

## Repository Root Files

Replace the former national-project root README with a concise repository overview that:

- identifies Tennessee as the first-stage research focus;
- links to `TN/` as the active phase;
- links to `DCUS/` as the national framework and archived broader-scope foundation;
- explains that the two directories share a repository but have separate geographic scopes.

Keep `.gitignore` at the repository root so its rules apply to both projects. Extend it to ignore `.DS_Store` files at every depth while retaining its existing Python, notebook, virtual-environment, Firecrawl, and temporary-file exclusions.

## Git History and Credential Safety

Keep the existing `.git/` directory at the repository root. Do not move, copy, print, stage, or commit the deploy keys stored inside `.git/`. The remote remains `git@github.com:Chris-Jin02/DataCenter.git`, the branch remains `main`, and existing commit history is preserved.

The reorganization will be represented as one implementation commit after validation. No force push, history rewrite, submodule, nested Git repository, or second remote is introduced.

## Validation

Before committing:

1. Confirm the repository has the intended `DCUS/`, `TN/`, and `docs/` roots and no tracked `.DS_Store` files.
2. Confirm every file previously tracked in the national project is represented under `DCUS/`, except the root `.gitignore`, which remains shared.
3. Confirm the Tennessee import contains the expected Markdown, notebook, HTML, template, and Excel artifacts.
4. Parse all notebooks as JSON.
5. Open the Excel workbook as a ZIP container and verify its workbook structure is readable.
6. Confirm the TN map notebook's dataset path resolves correctly from `TN/Map/`.
7. Scan Markdown and notebooks for stale local paths introduced by the move.
8. Inspect `git diff --check` and the staged diff summary.

After the local commit, push `main` to the existing `origin` and verify the local branch is synchronized with `origin/main`.

## Out of Scope

- Rewriting the scientific content, datasets, maps, or notebooks.
- Combining the national and Tennessee datasets.
- Creating separate GitHub repositories for DCUS and TN.
- Rewriting, squashing, or force-pushing existing history.
- Publishing local temporary files, application materials, or credentials.
