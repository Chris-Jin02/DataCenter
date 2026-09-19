# Phase 3: validation, model selection, and scoring registry

Phase 3A through 3H are complete. The frozen Phase 2 workbook remains unchanged (SHA-256: `112d6db67d7f4f9e74fa8edde3406937e1f8eb7145e9bc04a64e7030cf1d3e03`); its training inputs, field contract, and spatial partitions are the registered interface for the released model. Phase 3H froze `pls_logistic` as the Primary release specification; the release closeout records the selection evidence and handoff to Phase 4.

## Retention rules

The executable Phase 3 notebooks and their result workbooks are formal deliverables and must be retained together. Subsequent phases must not delete notebooks, their dependent source code, or final results; temporary caches, rendered previews, and one-off intermediate exports may be removed. The Phase 3 notebooks previously deleted under an earlier rule do not exist in the current workspace, Git history, or local editor history and cannot be restored verbatim. Any reconstructed notebook will be clearly labeled as reconstructed and will not be represented as the original execution record.

| Notebook | Scope | Retained outputs |
|---|---|---|
| [Phase 3 training, comparison, and visualization](code/phase3_model_training_comparison_visualization.ipynb) | Frozen-data checks, spatially validated supervised models, D1-only PCA/KMeans, regime-and-score comparison, and Matplotlib PNG visualizations | `phase3_training_comparison_visualization.xlsx` and two PNGs in `results/figures/` |
| [Phase 3 final model training](code/phase3_final_model_training.ipynb) | 21 features, spatial 3-fold validation, 20 Primary draws, Elastic Net / PLS / spline / constrained boosted-tree comparison, D1 unsupervised regimes, and multilocation scoring | `phase3_final_multilocation_scoring.xlsx`, `phase3_final_model_weights.json` containing all Primary-draw weights for four candidate models, and `phase3_final_score_map.png` |

| Result | Contents |
|---|---|
| [Input-contract audit](results/phase3a_input_contract.xlsx) | 60 / 74 / 73 scenarios, 21 permitted features, D1 eligibility, background sampling, linkage, and leakage checks |
| [Spatial-fold registry](results/phase3a_spatial_fold_registry.xlsx) | Three regional holdout folds, 200 km equal-area spatial-block folds, and stable fold IDs for the complete D1 grid and Presence records |
| [Primary transparent baseline](results/phase3b_primary_baseline.xlsx) | 5 km, 10:1, 20-draw L2-logistic baseline; fold-level metrics, coefficients, and run checks |
| [Scenario and model comparison](results/phase3c_model_comparison.xlsx) | Screened and contract logistic comparisons across Primary, Weighted, and Strict; within-training-fold collinearity representative selection |
| [5:1 background sensitivity](results/phase3d_background_sensitivity.xlsx) | Exact nested-prefix reconstruction, 720 5:1 spatial fits and run-level comparison with 10:1, plus evidence that 20:1 cannot be reconstructed |
| [Occupied-cell influence analysis](results/phase3d_spatial_influence.xlsx) | 3,840 leave-one-cell-out refits for 48 Primary occupied cells and multi-record same-cell location checks |
| [3D release-gate conclusion](results/phase3d_release_gate.xlsx) | Integrated conclusion on 5:1 background sensitivity, spatial influence, registered selection rules, and unmet dependencies |
| [D1 unsupervised environmental regimes](results/phase3e_unsupervised_regimes.xlsx) | PCA and KMeans regimes, stability, Presence enrichment, novelty flags, and complete assignments for 4,391 D1 cells |
| [Statewide supervised ranking](results/phase3f_supervised_statewide_predictions.xlsx) | 60 full-D1 benchmark `screened_logistic` fits, 0–100 Primary relative scores, draw uncertainty, scenario rank ranges, coefficients, and site mappings |
| [3G evidence reconciliation](results/phase3g_evidence_reconciliation.xlsx) | Row-level reconciliation of supervised scores and unsupervised regimes for 4,391 cells, five evidence states, within-regime score distributions, high-score composition, and review lists |
| [Phase 3 release closeout](results/phase3_release_closeout.md) | Final model-selection decision, release scope, hashes, and Phase 4 handoff |

The Phase 2 notebook interfaces were fixed and rerun with bundled Python. An IPython-independent display fallback preserves Jupyter display behavior, and feature-completeness checks now validate complete Presence and Domain rows for each of the 21 features. All assertions in both notebooks passed.

All 120 spatial-holdout fits in 3B converged, with no overlap between training and test spatial groups. Median test ranking percentiles are about 89% for both grand-region and block validation. This is an exploratory, transparent baseline using three Phase 2D pre-screened features; it must not be interpreted as construction probability, engineering feasibility, or a final site score.

Phase 3C completed 720 spatial-holdout model runs. The nonlinear baseline was not activated because the bundled runtime lacked a reproducible implementation; this limitation is recorded in the results.

Phase 3D conditionally passed. The 5:1 background sample was exactly reconstructed as 20,700 rows from frozen `selection_rank_within_stratum` values and 5:1 audit quotas; all 360 scenario/draw/stratum samples are nested prefixes of 10:1. All 720 5:1 fits converged without spatial-group leakage. All 3,840 leave-one-cell-out refits for 48 Primary occupied cells converged; the largest single held-out-percentile change was 0.014643, below the recorded 0.02 reference scale. The three-feature `screened_logistic` result is retained as a transparent development benchmark.

Deterministic cell IDs, metropolitan-boundary definitions, and complete 3/7/10 km feature tables for 20:1 remain unavailable. They are marked unavailable in the 3D release-gate workbook and cannot be treated as completed validation.

Phase 3E is complete. All 4,391 eligible D1 cells use only the frozen 21 numeric features for `log1p`, robust scaling, and PCA. `transmission_owner_count_25km` uses a standard-deviation fallback scale because its D1 interquartile range is zero, and this is recorded in the results. PCA retains six components explaining 82.6% of D1 variance. K=2 has the highest D1-only silhouette score (0.3619) among K=2–8 and passes a 20-run, 80% D1-resampling stability check. R1 has 3,281 cells (74.7%) and R2 has 1,110 (25.3%); the post hoc Primary Presence enrichment ratio for R2 is 3.2306, with a 95% bootstrap interval of 2.9010–3.5603. Regimes are not suitability grades.

Phase 3F is complete. The final comparison selected `pls_logistic` from Elastic Net, PLS-logistic, spline-logistic, and constrained boosted-stump candidates under the registered spatial-fold rule. The 21-feature Primary model is fitted for each of 20 deterministic 10:1 draws; the frozen weights and preprocessing parameters are retained in `phase3_final_model_weights.json`. The released Primary relative score is the 0–100 within-D1 percentile rank of the median prediction across those draws. The earlier three-feature `screened_logistic` fits remain benchmark evidence and are not the Phase 4 release model.

Phase 3G is complete. All 4,391 D1 cells are joined with 3E regimes, stability, Weighted Presence enrichment, and novelty, as well as supervised scores, draw uncertainty, and scenario diagnostics. The Primary supervised score remains the only numeric ranking; unsupervised results provide corroboration, exceptions, and review states only. R2 accounts for 25.3% of D1 but 50.9% of Primary ≥90 cells and 43.7% of Primary ≥75 cells.

Phase 3H is complete. The release decision froze `pls_logistic`, its 21-feature order, 20 Primary draw models, Phase 2 input hash, and score reference distribution. Phase 4 consumes this package without retraining or changing coefficients.
