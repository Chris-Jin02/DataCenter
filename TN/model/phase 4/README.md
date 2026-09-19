# Phase 4 release

Status: released as `TN-DC-1.0.0` after 4E verification.

## Frozen inputs

- Phase 2 workbook SHA-256: `112d6db67d7f4f9e74fa8edde3406937e1f8eb7145e9bc04a64e7030cf1d3e03`
- Selected model: Primary-only `pls_logistic`, 21 features, 20 retained draw models
- Phase 3 scoring workbook SHA-256: `10bea5146ae63953030e1713d0dc155d1266633ef004b5a0b675d3ecb802f09e`

## Retained code and outputs

- [Phase 4 release, scoring, ranking, and maps](phase4_release_and_products.ipynb)
- `../notebook_support/phase4/build_candidate_workbook.mjs` and `../notebook_support/phase4/verify_candidate_workbook.mjs`: called directly from Python cells in the Phase 4 notebook using the bundled Node runtime; no project-local `node_modules` is retained
- `TN/model/notebook_support/candidate_workbook_schema.json`: shared candidate CSV/XLSX field labels and types consumed by both Node support scripts
- `results/TN-DC-1.0.0_statewide_scores.csv`: D0/D1 score table
- `results/TN-DC-1.0.0_candidate_ranking.xlsx` and CSV: 14-record external Candidate ranking
- `results/TN-DC-1.0.0_score_map.png` and `TN-DC-1.0.0_uncertainty_novelty_map.png`: released maps
- `results/TN-DC-1.0.0_release_verification.md`: 4E release-gate record
- versioned model card, score dictionary, batch template, and decision-user guide

The 16 source Candidate records yield 14 ranked rows after the documented
shared-site and linked-evidence reconciliation; no source record is silently
dropped.

## Limits and handoff

Scores are empirical D1-relative rankings. They do not establish utility capacity, interconnection, fiber, land control, permitting, water, schedule, cost, or project approval. Candidate scores remain external to Primary training and accuracy evidence. Phase 5 begins with project-level diligence for Priority 1 and selected Priority 2 locations.
