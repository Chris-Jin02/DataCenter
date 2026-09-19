# Tennessee data-center siting ranking and scoring workflow

**Status date:** 2026-09-19
**Current execution point:** Phase 4 released as `TN-DC-1.0.0`; Phase 5 is deferred
**Frozen Phase 2 source:** `phase2_model_dataset.xlsx`  
**Frozen source SHA-256:** `112d6db67d7f4f9e74fa8edde3406937e1f8eb7145e9bc04a64e7030cf1d3e03`

## 1. Project objective and final decision product

The objective is to train and validate a model that helps rank and score potential Tennessee data-center locations. The model uses the features selected and frozen through Phase 2. Supervised learning provides the primary statewide ranking. Unsupervised learning describes recurring infrastructure and market environments and tests whether the supervised high-ranking cells occur in stable, interpretable regimes that are enriched for observed sites.

The final product is a decision-support package for screening locations inside the Tennessee D1 candidate domain. It will contain:

1. a reproducible 0–100 relative empirical affinity score for every eligible D1 cell;
2. a rank and review-priority band for every eligible cell and mapped candidate site;
3. an unsupervised regime assignment and regime-enrichment result;
4. agreement, uncertainty, scenario-stability, and out-of-distribution flags;
5. the hard-constraint status and unresolved engineering or commercial checks; and
6. a model card explaining the data, model version, validation results, limits, and update rules.

The score is a relative ranking within the versioned Tennessee D1 domain. It is not a construction probability and does not establish available electric capacity, interconnection approval, fiber quality, water allocation, land control, permitting success, community acceptance, or commercial feasibility.

The released Phase 1–4 logic is:

```text
Audited site evidence
        -> frozen candidate domain and selected features
        -> spatially validated supervised ranking
        -> statewide unsupervised environment regimes
        -> supervised/unsupervised evidence comparison
        -> cell and candidate scoring with uncertainty flags
        -> versioned release and verification

Project-level engineering and commercial review is the deferred Phase 5
follow-on and is not a prerequisite for the Phase 1–4 release.
```

## 2. Frozen analytical foundation

### 2.1 Presence scenarios

The following definitions are the only approved Phase 3 scenario interfaces:

| Scenario | Included sites | Presence-weight total | Occupied 5 km cells | Use |
|---|---:|---:|---:|---|
| `primary` | 60 | 60.0 | 48 | Confirmed, mappable Master records; anchor model and main interpretation |
| `weighted` | 74 | 69.0 | 56 | Primary plus 14 distinct Candidate locations weighted by evidence confidence |
| `strict` | 73 | 68.5 | 56 | Weighted excluding the area-or-city coordinate | Coordinate-quality sensitivity |

`TNDC-006` is audit-only. `TNCAND-010` shares the physical ORNL location represented by `TNCAND-009`, and `TNCAND-012` is supporting evidence for `TNDC-038`; neither creates a duplicate presence point. Presence weights measure confidence that a record can be used as evidence. They are not suitability weights.

### 2.2 Candidate domain

The primary scoring unit is a 5 km × 5 km equal-area cell clipped to Tennessee land.

| Domain status | Cells | Meaning |
|---|---:|---|
| D0 | 4,502 | Tennessee land cells in the frozen grid |
| D1 eligible | 4,391 | Cells that pass the D1 v2 analytical availability rule |
| D1 excluded | 110 | Cells without the required available connected component after hard masking |
| D1 unresolved | 1 | Boundary-mismatch cell; excluded from sampling and scoring |

D1 v2 uses a 250 m hard-constraint mask for slope above 16 percent, selected perennial NHD waterbodies, PAD-US GAP 1 or 2 protected land, DFIRM polygons marked `FLOODWAY`, and mapped military installations, ranges, and training areas. An eligible cell must retain a largest rook-connected unmasked component of at least 0.10 km². This is an analytical screening rule rather than a parcel-level legal or engineering decision.

### 2.3 Background design

The current primary D2 design is 10 background cells per included presence within the frozen grand-region and metro-distance strata. It has 20 deterministic draws using seeds 4701–4720. Every scenario excludes all known occupied cells from background sampling. The frozen workbook contains 41,400 background rows across the three scenarios.

The 5:1 design met all quotas but its row-level samples must be reconstructed as nested prefixes before sensitivity fitting. The 20:1 design has documented census shortfalls in two small strata and lacks a complete row-level cell-ID delivery. It cannot be treated as an executed sensitivity until those IDs are rebuilt and reconciled to the audit.

### 2.4 Feature contract

The current model may use only the 21 numeric Phase 2 proxy features. They represent:

- transmission proximity, voltage context, and owner diversity;
- major-road and Interstate proximity;
- hydrographic proximity;
- nearby institutions and CIP 11/14 completions within 50 and 100 km; and
- county employment and establishment context.

The three Phase 2D preliminary priorities are `dist_major_road_km`, `dist_transmission_any_km`, and `dist_surface_water_flowline_km`. Ten additional variables are secondary candidates. Eight variables require representative selection within their collinearity groups. This disposition is a starting contract and not a final importance result.

Identifiers, raw coordinates, presence-cell markers, D1 eligibility fields, sampling strata, draw IDs, fold IDs, cluster labels, and other design variables cannot enter the predictor matrix. Hard-constraint fields determine eligibility and remain separate from ranking features.

Fiber route quality, spare utility capacity, interconnection queue position, electric price, public-water capacity, water rights, parcel ownership, detailed land cost, permitting, community acceptance, and comparable site-level hazard data are not present as consistent statewide training features. They remain downstream diligence fields until a new frozen data release passes the same source and coverage audit.

## 3. Audit of Phase 1–3 work completed to date

### 3.1 Work retained in the final evidence chain

| Completed work | Retained role |
|---|---|
| Phase 1 canonical cohort, exclusion audit, and presence-weight scenarios | Source lineage for the 60/74/73 scenario definitions |
| Phase 1 feature dictionary, source catalog, completeness report, and coordinate review | Source, unit, coverage, and uncertainty evidence |
| Phase 2 D0/D1 v2 domain and hard-mask audit | The only statewide eligibility and scoring domain |
| Phase 2 10:1 repeated D2 samples | Primary model-fitting background design |
| Phase 2 21-feature matrix and training contract | The only approved model input interface |
| Phase 2D screening and collinearity groups | A preliminary baseline and training-fold selection specification |
| Phase 3A input-contract audit and spatial-fold registry | Reproducible join rules, prohibited fields, region folds, and 200 km block folds |
| Phase 3B transparent Primary logistic baseline | Interpretable benchmark and current supervised evidence |
| Phase 3C three-scenario model comparison | Scenario stability and screened-versus-contract logistic comparison |

Phase 2 is frozen and is the runtime source for all Phase 3 training and statewide scoring. Phase 1 tables remain provenance evidence and must not be mixed with the Phase 2 feature values.

### 3.2 Work retained only as descriptive or diagnostic evidence

The Phase 1 geographic DBSCAN results describe where documented sites concentrate. At `eps=20 km` and `min_samples=3`, 41 of 60 Primary sites formed four geographic groups; the expanded 75-location description placed 56 locations in five groups. The expanded grouping was stable relative to the baseline, with Adjusted Rand Index about 0.92 and clustered-pair Jaccard about 0.93. These results are useful for visual review, metro influence checks, and communicating sample concentration. Geographic cluster labels do not enter the model.

The Phase 1 site-only feature clustering used 21 numeric variables and selected K=2 with silhouette 0.388. It produced a 20-location and a 55-location environmental grouping. This is useful as an exploratory description of observed sites and as evidence that the feature space contains broad regimes. It is not the final statewide unsupervised analysis because it excludes the 4,391 eligible D1 cells.

Phase 1 PCA, parameter sweeps, coordinate-jitter simulations, manual feature-importance rankings, figures, and the interactive cluster map remain quality-control and communication artifacts. They do not supply learned weights, labels, or suitability grades.

Phase 3B and 3C are model-development evidence rather than the final score. Phase 3B completed 120 spatially held-out L2-logistic fits. Phase 3C completed 720 fits across three scenarios, two logistic specifications, two validation schemes, three folds, and 20 draws. All recorded runs had zero train/test spatial-group overlap; the Primary screened baseline achieved median held-out ranking percentiles near 0.89 in the summarized region and block results. Because the three screened features were selected in Phase 2D using the same overall presence inventory, these figures remain exploratory evidence and are not an independent prospective confirmation.

### 3.3 Work that will not be extended in the current release

The following activities do not improve the current final scoring chain and will stop unless a later data release creates a specific need:

- further tuning of the Phase 1 site-only DBSCAN, KMeans, or PCA outputs;
- using Phase 1 cluster IDs, manual feature rankings, or cluster-separation importance as model inputs or score weights;
- reading Phase 1 `site_feature_matrix.csv` during Phase 3 training, because its point-derived values differ from the frozen Phase 2 interface and include a different analytical population;
- treating background cells as failed projects or raw logistic probabilities as construction probabilities;
- expanding the model catalogue merely to compare more algorithms;
- activating PU learning without a registered class-prior assumption and reproducible spatial-validation design;
- activating capacity-weighted or historical models before comparable capacity, date, and historical-feature coverage exists; and
- inserting unavailable engineering variables through subjective imputation.

A nonlinear challenger is optional. It will be activated only if a reproducible implementation exists in the approved runtime and the effective sample size supports its complexity. Failure to activate it does not block the transparent supervised ranking workflow.

## 4. Phase status and remaining roadmap

| Phase | Scope | Status |
|---|---|---|
| Phase 1 | Site evidence, descriptive geography, site-only environment exploration | Complete |
| Phase 2 | Candidate domain, background design, feature matrix, screening, training contract | Complete and frozen |
| Phase 3A | Input and spatial-fold registration | Complete |
| Phase 3B | Primary transparent supervised baseline | Complete |
| Phase 3C | Scenario and logistic-specification comparison | Complete |
| Phase 3D | Sensitivity, influence, and release-rule registration | Complete — conditional Gate D pass |
| Phase 3E | Statewide unsupervised environmental regimes | Complete |
| Phase 3F | Final supervised model selection, fitting, and statewide prediction | Complete |
| Phase 3G | Supervised–unsupervised evidence reconciliation | Complete |
| Phase 3H | Phase 3 freeze and release decision | Complete |
| Phase 4 | Final cell and candidate scoring product | Released as TN-DC-1.0.0 |
| Phase 5 | Shortlist diligence bridge and decision workflow | Deferred |
| Phase 6 | Release, prospective monitoring, updates, and project closeout | Planned |

## 5. Phase 3D — sensitivity, influence, and rule registration

### Purpose

Determine whether the current supervised signal is stable enough to support statewide scoring and freeze all remaining decision rules before the final surface is inspected.

### Implementation

1. Reconfirm the Phase 2 hash, 60/74/73 scenario counts, 4,391 eligible cells, 21 predictors, fold assignments, and prohibited-field list.
2. Aggregate the completed Phase 3C results by scenario, validation scheme, fold, model, and draw.
3. Compare Primary, Weighted, and Strict results using held-out mean percentile, top-decile capture, top-quintile capture, and background AUC as a secondary diagnostic.
4. Measure rank and coefficient stability across draws and identify any fold, scenario, or feature whose conclusion reverses.
5. Reconstruct the 5:1 samples from the registered random order and verify that each sample is a prefix of its 10:1 counterpart; retain the two logistic specifications as the Phase 3D benchmark comparison.
6. Attempt the 20:1 reconstruction only from the frozen sampling rules, seeds, audit quotas, and cell IDs. If exact reconstruction fails, record it as unavailable rather than generating a different design.
7. Run occupied-cell and large-campus influence checks so that repeated records in one market or campus cannot dominate the conclusion.
8. Register a metropolitan boundary definition before any leave-one-metro-out analysis. If no defensible frozen boundary is available, retain the completed grand-region and 200 km block results as the formal validation and document metro validation as unavailable.
9. Treat 3, 7, and 10 km grid comparisons as conditional extensions because their complete predictor matrices do not yet exist. They do not enter the current model by partial feature substitution.
10. Freeze the model-selection rule, score transformation, review bands, uncertainty fields, and unsupervised comparison rule before producing statewide predictions.

### Required release rule

The Phase 3D benchmark required each Primary fold to exceed the registered 0.50 held-out threshold and recorded the simpler-model tie rule. The final Phase 3 selection then compared Elastic Net, PLS-logistic, spline-logistic, and constrained boosted-stump candidates under the retained spatial-fold evidence; `pls_logistic` had the highest recorded worst-fold median weighted AUC and was frozen in the Phase 3H closeout. Scenario and influence results remain release constraints when they show a material rank reversal, even if mean performance is high.

### Output

One result workbook containing the frozen rules, sensitivity metrics, influence results, unmet dependencies, and a Gate D decision. No row-level process files are retained.

## 6. Phase 3E — statewide unsupervised environmental regimes

### Purpose

Identify recurring environments across all eligible D1 cells without using the presence label. This tests structural consistency and detects high supervised scores in rare or unsupported parts of the feature space.

### Implementation

1. Read the 4,391 eligible D1 rows and the same 21 allowed numeric features from the frozen Phase 2 workbook.
2. Fit all preprocessing on D1 cells only: apply the documented skew transformation, robust scaling, and PCA. Retain enough components to explain at least 80 percent of D1 feature variance, subject to a minimum interpretability review of loadings.
3. Fit KMeans for K=2 through K=8 as the reproducible primary regime method. Select K using silhouette, resampling stability, minimum regime size, and geographic coherence. Presence enrichment is not used to select K.
4. If a reproducible HDBSCAN implementation becomes available, run it as a challenger and report its stability and noise share. It does not replace the primary result unless it passes the same stability and interpretability checks.
5. Freeze the regime model, assign every eligible D1 cell, and then join the presence sites for post-fit evaluation.
6. For every regime, report D1 cell share, feature profile, PCA profile, mapped geography, Primary/Weighted/Strict presence share, weighted enrichment ratio, and uncertainty.
7. Perturb K, initialization, D1 resamples, and reasonable preprocessing choices to compute assignment stability. Small or unstable regimes receive a reliability warning.
8. Compute an out-of-distribution or novelty measure from distance to the assigned regime centroid and D1 feature-range checks. Thresholds are set from the D1 distribution before supervised scores are compared.

For regime `k`, the principal post-fit statistic is:

\[
ER_k = \frac{P(\text{Regime}=k\mid\text{Weighted Presence})}
{P(\text{Regime}=k\mid\text{D1 availability})}.
\]

An enriched regime is an environment associated with the observed sample. It is not automatically suitable, and a non-enriched regime is not automatically unsuitable.

### Output

One result workbook with the regime model specification, D1 assignments, profiles, stability, enrichment, and novelty results, plus final maps needed for interpretation.

## 7. Phase 3F — final supervised model and statewide prediction

### Purpose

Select one transparent ranking specification under the Phase 3D rule, fit it reproducibly, and produce an ensemble prediction for the full D1 domain.

### Implementation

1. Compare the retained candidate specifications under the frozen spatial-fold rule and select the registered winner, `pls_logistic`, for the release package.
2. Use Primary as the anchor learning population. Use Weighted and Strict to measure how Candidate evidence and coordinate quality change statewide ranks.
3. Repeat preprocessing and any representative feature selection within training folds for validation. Fit final full-domain versions separately for each background draw after the specification is selected.
4. Preserve 20 draw-specific predictions rather than averaging predictor rows or background samples before fitting.
5. Predict the relative linear score for all 4,391 eligible D1 cells from each draw-specific model. Do not publish sampled-class probabilities.
6. Convert the median ensemble prediction to a statewide percentile:

\[
Score_{empirical}(s)=100\times PercentileRank\left(\operatorname{median}_d\hat r_d(s)\mid s\in D1\right).
\]

7. Retain the fifth, twenty-fifth, seventy-fifth, and ninety-fifth prediction or rank percentiles across draws; compute rank interquartile range and scenario rank range.
8. Map all 74 weighted-scenario sites and any separate candidate list to D1 cells without changing the cell score. Multiple records in one cell share the cell score and retain distinct source identities.
9. Report standardized coefficients, direction, and draw/fold stability for the selected model. These explain the fitted ranking association rather than a causal site-selection mechanism.

### Output

One result workbook containing the selected specification, validation decision, draw-level model summaries, complete D1 prediction table, candidate-site mapping, coefficients, and uncertainty summaries.

## 8. Phase 3G — supervised and unsupervised evidence comparison

### Purpose

Compare the primary supervised ranking with the independent label-free structure of the D1 feature space. The comparison informs confidence and review priority; it does not average two incomparable outputs into an arbitrary model score.

### Implementation

1. Join each D1 cell's empirical percentile, prediction uncertainty, regime ID, regime stability, enrichment interval, and novelty measure.
2. Report the empirical-score distribution within every regime and the regime distribution within the top 10, 25, and 50 percent of supervised cells.
3. Measure whether high-scoring cells concentrate in stable regimes with positive Presence enrichment.
4. Identify five mutually exclusive evidence states:

| State | Supervised evidence | Unsupervised evidence | Interpretation |
|---|---|---|---|
| `corroborated` | High and stable rank | Stable, enriched regime; not novel | Strongest empirical screening support |
| `model_only` | High rank | Neutral or weak enrichment | Retain score; require closer feature and diligence review |
| `regime_only` | Moderate or low rank | Stable, enriched regime | Potential omitted interaction or local opportunity; manual review |
| `novel_or_unstable` | Any rank | Novel, small, or unstable regime | Low confidence; do not promote solely on the model score |
| `limited_support` | Below high-rank threshold | Stable, non-enriched regime | No positive convergent support; this is not an unsuitability label or exclusion |

5. Compare results across Primary, Weighted, and Strict. A cell whose priority changes materially across scenarios receives a scenario-sensitivity flag.
6. Review apparent disagreements at feature level to determine whether they arise from nonlinear regime structure, a sparse environment, a Candidate-weight effect, or an unavailable engineering variable.

The supervised percentile remains the only learned scalar score. The unsupervised result supplies regime context, corroboration, and caution flags.

### Output

One result workbook and map set with the joined evidence states, regime-by-score comparisons, scenario sensitivity, and exception review.

## 9. Phase 3H — Phase 3 freeze and scoring-release decision (completed)

### Recorded implementation

1. Verify that every Phase 3 result reads the frozen Phase 2 workbook and records its SHA-256 hash.
2. Confirm no IDs, coordinates, domain flags, fold IDs, sampling strata, or cluster labels entered a supervised predictor matrix.
3. Confirm no presence labels or supervised predictions were used to select the unsupervised regime count or preprocessing.
4. Reconcile all model runs, draws, scenarios, folds, and D1 assignments to expected counts.
5. Evaluate Gates A–E in Section 13 and record each as pass, conditional pass, or fail with evidence.
6. Freeze the selected supervised specification, unsupervised regime specification, score transformation, review bands, and version identifier.
7. If the supervised model fails the release gates, stop statewide score publication and deliver the descriptive regimes, held-out association results, and failure reasons. Do not relax a gate after seeing the map.

### Output

A Phase 3 release closeout record and updated Phase 3 README. The release decision and all unresolved dependencies are explicit in `model/phase 3/results/phase3_release_closeout.md`.

## 10. Phase 4 — final ranking and scoring product

### Purpose and boundary

Phase 4 operationalizes the frozen Phase 3 model. It does not select features, tune hyperparameters, retrain a model, or change a coefficient. The released model is the 21-feature `pls_logistic` model selected from Elastic Net, PLS-logistic, spline-logistic, and constrained boosted-stump candidates by spatial three-fold performance. Its 20 Primary-draw models, all candidate-model weights, and D1-only PCA/KMeans model are retained in `phase3_final_model_weights.json`.

### 4A — release lock and score contract

1. Confirm the frozen Phase 2 SHA-256, 21-feature order, score-reference distribution, selected model name, and 20 Primary draw models against the weight package.
2. Freeze a semantic version such as `TN-DC-1.0.0`, the score date, software runtime, and artifact hashes.
3. Record the model-selection evidence: Primary spatial AUC by region, spatial log loss, selected specification, and all non-selected candidate weights.
4. Publish only Primary-model scores in this release. Weighted and Strict final-model weights are not yet frozen; Phase 4 must not claim a final scenario-ranking range until they are trained, retained, and released under a new model version.

### 4B — input and batch-scoring interface

Every input row must contain a stable `location_id`, optional location name and coordinates, and all 21 frozen numeric features in the exact documented units. The scoring code must:

1. reject missing, non-numeric, or out-of-contract values rather than silently imputing them;
2. apply the stored `log1p`, mean, and scale parameters separately for every retained Primary draw;
3. compute the median raw score across the 20 selected-model draws;
4. convert it to the frozen D1-relative `final_score` from 0 to 100;
5. compute rank within the submitted batch, draw P05/P95, and draw IQR; and
6. apply the retained D1-only PCA/KMeans parameters to return `grid_regime`, centroid distance, and `novelty_flag`.

Coordinates support mapping and domain checks; they never enter the supervised predictor matrix.

### 4C — statewide and candidate products

Every D0 cell receives its domain status. Every eligible D1 cell and every valid scored input row receives:

- `final_score`, `final_raw_score`, D1-relative percentile, and rank;
- `score_p05`, `score_p95`, and `score_iqr` across the 20 Primary draws;
- model version, selected specification, frozen Phase 2 hash, and scoring timestamp;
- `grid_regime`, regime distance, and novelty flag;
- the 21 supplied feature values; and
- D1 eligibility, exclusion context, data-quality fields, and unresolved engineering checks when applicable.

The operational bands remain transparent review bands:

| Final score | Band | Use |
|---:|---|---|
| 90–100 | Priority 1 | First set for project-level diligence |
| 75–<90 | Priority 2 | Secondary diligence and alternative-market review |
| 50–<75 | Watchlist | Retain for scenario, expansion, or data updates |
| 0–<50 | Lower empirical affinity | Defer unless external project evidence justifies review |

Novelty and high draw-IQR flags require review but do not secretly alter `final_score`.

### 4D — candidate evaluation and user-facing outputs

1. Score the 14 Phase 2 Candidate records without adding them to the Primary training cohort.
2. Deliver a candidate ranking table showing location metadata, final score, uncertainty, D1-relative percentile, regime, novelty, and required diligence checks.
3. Treat Candidate scores as an external score exercise, not as accuracy evidence: Candidate records are not confirmed positive or negative outcomes.
4. Produce a statewide score map and an uncertainty / novelty map with clear legends and D1 exclusions.
5. Provide the batch input template, score dictionary, model card, and concise decision-user guide.

### 4E — verification and release gate

Before release, verify:

1. batch scoring and one-row scoring return the same score for the same feature vector;
2. all scored D1 IDs are unique, all scores are in 0–100, and D0 excluded/unresolved rows have no score;
3. the score package hash, feature order, 20 draw models, and model name match the frozen weight package;
4. no input ID, coordinate, region, grid identifier, Candidate role, or cluster label enters the supervised scorer;
5. the candidate table contains 14 rows and is separate from Primary training rows; and
6. maps, workbook tables, and code output agree on counts and score ranges.

### 4F — retained deliverables

- one statewide D0/D1 scoring workbook or geospatial table;
- one Candidate ranking workbook or table;
- one final map package with score, draw uncertainty, regime, novelty, and exclusions;
- one versioned model card, input dictionary, and decision-user guide;
- the frozen JSON weight package; and
- the reproducible Notebook and Python code required to train and score.

Only these final result files and code are retained. Temporary exports, caches, scratch tables, intermediate plots, and build logs are removed after verification.

## 11. Phase 5 — shortlist diligence and final location review

The model narrows the search. It does not replace project-level diligence. For Priority 1 and selected Priority 2 cells:

1. identify parcels or sites large enough for the intended facility program;
2. obtain utility confirmation for available capacity, voltage, substation configuration, interconnection path, queue status, schedule, and cost;
3. verify fiber routes, carrier diversity, latency, and service commitments;
4. verify water source, allocation, treatment, discharge, drought exposure, and cooling design when relevant;
5. perform parcel-level flood, wetland, protected-land, slope, geotechnical, and access review;
6. review zoning, permitting, tax, community, noise, air, and environmental-justice considerations;
7. estimate land, power, network, water, construction, tax, and schedule costs under one project specification;
8. record each item as pass, fail, unresolved, or conditionally acceptable with evidence date and owner; and
9. rank the surviving shortlist using a separately approved decision policy whose noncompensable constraints cannot be offset by a high empirical score.

Project-level diligence data may be appended to the candidate report. They enter model retraining only through a new versioned statewide data and feature audit.

## 12. Phase 6 — release, monitoring, updates, and closeout

### 12.1 Release verification

1. Recompute all final artifacts from frozen inputs in a clean runtime.
2. Verify counts, hashes, joins, formulas, score ranges, rank uniqueness rules, missingness, and exclusion handling.
3. Visually inspect statewide and regional maps for projection, clipping, legend, label, and outlier errors.
4. Confirm that all claims match the model card and that engineering proxies are not presented as capacity or approval.
5. Freeze the release version, date, input hashes, parameters, software versions, and owners.

### 12.2 Prospective validation

New qualifying Tennessee sites recorded after the freeze date form a prospective queue. They are scored with the unchanged released model and domain before any retraining. Report their percentile ranks, regimes, and uncertainty. This is the strongest available external check because Phase 3 used the current inventory for model development.

### 12.3 Update triggers

A new model version is required when any of the following occurs:

- the presence inventory or Candidate evidence rules materially change;
- the candidate domain or hard-constraint sources change;
- one or more predictor sources are updated or corrected;
- new statewide engineering features pass coverage and quality gates;
- prospective performance weakens materially; or
- the intended facility type or decision use changes.

Every update repeats the Phase 2 interface audit, Phase 3 spatial validation, unsupervised regime analysis, evidence comparison, scoring, and release checks. Scores from different versions are not compared without a bridge analysis.

### 12.4 Project completion definition

The Tennessee workflow is complete when all of the following exist and pass verification:

1. a frozen and reproducible Phase 2 analytical interface;
2. a supervised model that passes the registered spatial and stability gates;
3. a statewide D1 unsupervised regime model with stability, enrichment, and novelty results;
4. a complete D0/D1 cell table with empirical score, rank, uncertainty, regime, evidence state, and exclusion status;
5. a candidate-site ranking table and map package;
6. a model card, score dictionary, user guide, and diligence checklist;
7. a recorded release decision and unresolved limitation list;
8. a prospective validation and version-update procedure; and
9. removal of temporary process files after the final outputs are reproduced and checked.

Running additional algorithms is not a completion criterion. If a required model gate fails, the completed deliverable is a documented descriptive and validation result explaining why a statewide score was not released.

## 13. Quality gates

| Gate | Pass condition | Status on 2026-09-14 |
|---|---|---|
| A — Frozen interface | Hash, 60/74/73 scenarios, D1 v2, 21 features, 10:1 draws, and prohibited fields reconcile | Passed |
| B — Spatial separation | Three grand-region folds and three 200 km block folds contain usable support and have zero train/test spatial overlap | Passed |
| C — Supervised ranking | Required Primary folds beat the registered random-ranking rule with convergence and no leakage | Provisionally supported; final rule applied in 3D |
| D — Stability and influence | Scenario, background-ratio, draw, fold, and occupied-cell checks do not show an unexplained material reversal | Conditional pass — 5:1 and occupied-cell checks complete; 20:1, metro, and alternate-grid extensions unavailable |
| E — Unsupervised structure | D1 regimes are stable and interpretable; enrichment, high-score distribution, and novelty are reported | Passed |
| F — Score release | Complete D1 table, uncertainty, regime context, OOD flags, score version, model card, and user guide pass QA | Passed in Phase 4 |
| G — Prospective evidence | Post-freeze sites are evaluated without changing the released model | Begins after release |

## 14. Source-of-truth and file policy

The frozen Phase 2 workbook is the only training and statewide-scoring input. Phase 1 files establish provenance and provide diagnostics. Phase 3 workbooks record validation and model decisions. The Proposal records the end-to-end workflow and release criteria.

Each phase directory retains only:

- the final result workbook, table, map, or report needed by the next phase;
- the notebook or code required to reproduce that result; and
- a README that states the input hash, status, outputs, limits, and next handoff.

Temporary data extracts, scripts used only to assemble a result, preview files, execution logs, and superseded duplicates are deleted after the final artifact passes content and visual verification.
