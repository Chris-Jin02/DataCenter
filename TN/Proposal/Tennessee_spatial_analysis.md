# Tennessee data center siting patterns and decision support

## Research position

> - Study area: Tennessee
> - Data foundation: the frozen Tennessee multisource public facility inventory
> - Current objective: identify reproducible spatial siting patterns and determine which features remain informative outside the markets used for model fitting
> - Next-stage objective: rank feasible Tennessee locations by relative empirical siting affinity and relevant site conditions
> - Later extension: apply the Tennessee workflow to other states after it passes the data, model, and decision quality gates

The project has two related purposes:

1. describe the geographic pattern of the 61 documented Tennessee Master locations; and
2. build a transparent method for comparing potential locations.

The central research question is:

\[
\boxed{
\text{Which measurable infrastructure, land, market, and risk conditions consistently distinguish the 61 Master locations from feasible Tennessee locations?}
}
\]

The available data identify 61 Master records and 16 Candidate_Sites records, but they do not provide a representative sample of locations that developers considered and rejected. All 61 Master records enter the main analysis with full presence weight. Candidate records with usable coordinates enter the same model with lower confidence weights. The models therefore estimate relative spatial association, ranking, and similarity within a defined availability domain. They do not estimate the unconditional probability that a data center will be built or operate successfully.

The research sequence is:

\[
\text{Canonical Sites}
\rightarrow
\text{Availability Domain}
\rightarrow
\text{Observed Siting Patterns}
\rightarrow
\text{Presence-Background and PU Models}
\rightarrow
\text{Spatial Validation and Interpretation}
\rightarrow
\text{Relative Site Score}
\]

Unsupervised learning will identify infrastructure environments and measure similarity to the weighted presence sample. It cannot establish site suitability on its own. Conclusions remain observational unless they are supported by independent temporal, policy, utility, or project-level evidence.

## Current Tennessee data foundation

The Phase 1 frozen workbook contains 61 Master records: 50 core data-center or interconnection records and 11 crypto-mining records. The main analysis includes all 61 records together, regardless of status, facility type, or analysis scope. Each Master record contributes one presence point with weight 1.

All 61 Master records have coordinate pairs. Forty-two have exact or address/site-level precision, and 41 have high location confidence. Coordinate precision and confidence remain quality fields but do not determine whether a Master record enters the pooled sample. The workbook also tracks 16 candidate sites. Thirteen currently have coordinate pairs and can enter spatial modeling after duplicate checks, giving a current maximum of 74 mapped training locations. The other three remain in the data-enrichment queue until their locations are resolved.

Published capacity is available for 15 of the 61 Master records and is concentrated in a small number of large projects. Capacity-weighted inference is inactive until coverage and influence requirements are met. Opening-year coverage is also insufficient for historical siting inference.

The frozen workbook remains unchanged. Analytical tables, derived features, sampling records, and model outputs will be stored as versioned downstream products with a separate processing log.

---

# 1. Decision context and research boundaries

## 1.1 Intended decision

The final system will help analysts, planners, and project teams decide which candidate locations warrant closer investigation. It will answer:

> Given the Tennessee candidate domain and the available evidence, which locations exhibit the conditions associated with the weighted Master and Candidate sample, and which constraints or uncertainties could change that ranking?

The system is a screening tool. A high score means that a location ranks favorably under the selected data, model, domain, and decision criteria. It does not certify utility capacity, permitting, land acquisition, community acceptance, environmental compliance, commercial feasibility, or future construction.

## 1.2 Primary analytical population

The weighted presence sample is:

\[
S_{train}=S_{Master}\cup S_{Candidate,mappable}
\]

Every Master record remains in the main sample after identity and coordinate checks. Records are not split by `status_normalized`, `facility_type`, or `analysis_scope` for model fitting. These fields remain available for describing the sample and interpreting possible source-composition effects.

Candidate_Sites records with coordinates enter the same model as partial presences. Their initial weights are fixed before feature inspection:

\[
w_i=
\begin{cases}
1.00, & i\in Master \\
0.75, & i\in CandidateHigh \\
0.50, & i\in CandidateMedium \\
0.25, & i\in CandidateLow
\end{cases}
\]

These values represent confidence in using a record as presence evidence. They are not estimates of site suitability or construction probability. The weights will be tested against two bounding cases: Candidate weight 0, which excludes them, and Candidate weight 1, which treats them like Master records. Candidate records without coordinates cannot enter a spatial model. A candidate linked to an existing Master record cannot create a second point unless evidence establishes a distinct location.

This pooled and weighted definition changes the interpretation of the outcome. The model learns the environments associated with publicly documented data-center-related facilities, projects, and credible candidates. Because the sample includes operational, proposed, under-construction, expanding, cancelled, interconnection, crypto-mining, and candidate records, the output is not a model of operational success alone.

## 1.3 Claims outside the scope

The current phase does not claim:

- that unobserved locations are unsuitable;
- that background samples are failed projects;
- that model scores are calibrated construction probabilities;
- that SHAP values or feature importance establish causal siting mechanisms;
- that current infrastructure necessarily existed when older sites were selected;
- that an unsupervised cluster is a suitability grade; or
- that Tennessee results directly generalize to other states.

---

# 2. Research questions and hypotheses

Primary hypotheses and evaluation rules will be fixed before final model comparison and statewide scoring.

## RQ1: Observed spatial pattern

Where are the pooled and weighted Tennessee facility, project, and candidate records concentrated, and how does that concentration compare with feasible Tennessee locations?

## H1: Electric infrastructure association

> After controlling for developable land, market conditions, and urbanization, pooled Master and weighted Candidate locations remain associated with shorter distance or stronger access to relevant electric infrastructure.

Evidence that weakens H1 includes an effect that disappears under the urban and industrial matched background, reverses across spatial folds, or is driven by one metro or campus.

## H2: Network infrastructure association

> Pooled Master and weighted Candidate locations occur more frequently in feasible areas with stronger commercial network access after controlling for market and urbanization variables.

Provider count, coverage, route proximity, and published record count will remain distinct measurements. H2 will be interpreted in light of the facility mix, source coverage, and Candidate weighting rule.

## H3: Independent and stable feature contribution

> At least one power or network feature contributes stable out-of-area ranking information beyond land and market controls.

Support requires consistent effect direction or predictive contribution across spatial folds, alternative backgrounds, and leave-one-metro-out tests. In-sample fit is insufficient.

## H4: Out-of-area ranking performance

> A parsimonious presence-background model ranks spatially withheld weighted presence locations above comparable available locations in separated test areas.

H4 concerns relative ranking within the availability domain. It is not a claim about the probability of future construction.

## Exploratory questions

- Which infrastructure regimes contain more or fewer observed data-center sites than expected?
- Do nonlinear supervised models add stable out-of-area information beyond a transparent statistical baseline?
- Which features have stable permutation importance and SHAP patterns across spatial folds?
- Which feasible areas receive high model scores but also high uncertainty or out-of-distribution warnings?
- How sensitive are model rankings and feature interpretations to the Candidate confidence weights?

Capacity, facility-type subclasses, and historical development remain conditional modules rather than primary hypotheses.

---

# 3. Phase one: canonical analytical data

## 3.1 Units of analysis

### Site or campus level

Each of the 61 frozen Master records contributes one full-weight point to the primary spatial analysis. Each eligible Candidate contributes one lower-weight point. Identity checks may correct documentation errors, but the analytical cohort preserves all 61 Master IDs and does not collapse records for the main model.

### Facility or building level

Facility and building records are retained for source tracing, campus membership, capacity aggregation, development intensity, and later site-specific work. They do not create additional positive points when they belong to the same physical campus.

## 3.2 Required analytical tables

| Table | Purpose |
|---|---|
| `canonical_sites` | One row for each of the 61 Master records |
| `site_facility_crosswalk` | Maps every source record to its Master record, with rationale and evidence role |
| `analysis_cohort` | Records source class, confidence weight, inclusion status, and spatial usability |
| `weighted_presence_cohort` | Combines all Master records and eligible Candidate records for model fitting |
| `analysis_processing_log` | Records derived variables, corrections, software, parameters, and dates |
| `data_quality_summary` | Reports missingness, coordinate precision, unresolved reviews, and sample counts |

The crosswalk distinguishes records used for entity identity, coordinates, lifecycle status, measurements, or supporting evidence. A source record marked as included must have a documented analytical destination.

## 3.3 Required site fields

| Field | Purpose |
|---|---|
| `site_id` | Stable analytical key |
| `facility_id` and `parent_site_id` | Facility-to-campus traceability |
| `site_name`, `operator`, `owner`, `developer`, `anchor_tenant` | Entity review and role separation |
| `latitude`, `longitude`, `coordinate_precision`, `location_confidence` | Spatial analysis and uncertainty |
| `county`, `market`, `status`, `facility_type` | Stratification and spatial validation |
| `capacity_mw`, `capacity_estimated`, `capacity_definition` | Conditional capacity analysis |
| `opening_year`, `milestone_date` | Conditional temporal analysis |
| `source_snapshot_date`, `evidence_urls` | Reproducibility and audit |
| `review_flag`, `cohort_role` | Manual review and analytical inclusion |

## 3.4 Gate A checks

Before spatial modeling:

1. resolve or explicitly flag campus and child-facility relationships without removing Master records from the pooled cohort;
2. confirm that every one of the 61 Master IDs appears exactly once in `canonical_sites`;
3. reconcile included raw records with the crosswalk;
4. confirm that all 61 Master IDs enter once with weight 1 and each eligible Candidate enters once with its predeclared confidence weight;
5. record the handling of ambiguous entity matches;
6. report capacity, temporal, and feature missingness;
7. identify sites requiring coordinate sensitivity analysis; and
8. freeze the analytical cohort and processing rules.

Spatial inference stops if the primary site definition cannot be reproduced.

---

# 4. Phase two: candidate domain and background sampling

The study uses available or background locations because verified rejected-project labels are not sufficiently numerous or representative. Background locations support estimation of relative spatial association. They are not treated as true negatives.

## 4.1 Availability domains

### D0: Tennessee land baseline

All Tennessee land, used for broad description and sensitivity analysis.

### D1: Feasible-land baseline

Exclude locations that fail predeclared feasibility rules, such as major water bodies, protected or restricted land, unacceptable terrain, and incompatible land classes. D1 is the main statewide scoring domain.

### D2: Urban and industrial matched baseline

Sample background locations from market, development, and industrial contexts comparable to observed sites. D2 tests whether apparent infrastructure associations mainly reflect urbanization or commercial geography.

## 4.2 Avoiding circular definitions

The availability domain must not be defined by the feature being tested. For example, substation proximity cannot be both a prerequisite for entering D1 and the primary explanatory variable in H1.

Hard constraints must be separated from preference variables:

- a hard constraint determines whether a cell remains in the candidate domain;
- a preference feature helps rank cells that remain feasible; and
- an uncertain constraint produces a flag rather than an automatic favorable value.

## 4.3 Background sampling protocol

For each model version:

1. preserve the full feasible grid for final scoring;
2. draw repeated background samples for computational model fitting;
3. stratify or weight sampling so large rural areas do not overwhelm comparable market environments;
4. prevent Master cells, included Candidate cells, and duplicate locations from being sampled as background;
5. retain sample seeds, inclusion probabilities, and weights;
6. repeat fitting across multiple background draws; and
7. report sensitivity to D0, D1, and D2.

The ratio of background points to positive sites affects classification metrics and raw model outputs. It must be fixed or included in sensitivity analysis.

## 4.4 Spatial scale

Use one equal-area grid or H3 resolution as the primary scoring unit. Select it from feature resolution, coordinate uncertainty, computational feasibility, and the scale of the decision. Compare at least one finer and one coarser resolution.

---

# 5. Phase three: feature system

## 5.1 Feature families

| Family | Candidate variables | Interpretation boundary |
|---|---|---|
| Electric power | Substation distance, transmission distance, voltage class, utility territory | Proximity does not establish spare capacity or interconnection approval |
| Network | Fiber coverage, route distance, provider count, carrier diversity, exchange access | Current coverage may reflect urbanization or later investment |
| Water and cooling context | Public-water service, water-source distance, reuse opportunity, watershed and drought indicators | Service-area presence does not establish project allocation |
| Market and labor | Metro distance, population, employment density, relevant labor access | These variables may proxy for several unobserved market factors |
| Land and parcel | Developable area, slope, land use, parcel scale, land-value proxy | Current values may not represent historical acquisition conditions |
| Transportation | Highway, airport, and freight access | Accessibility is not automatically a requirement |
| Hazard and environmental context | Flood, heat, drought, seismic, wildfire, and other relevant risks | Hazard layers require consistent years, units, and resolution |
| Community and receptor context | Homes, schools, parks, churches, streams, and other locally relevant receptors | These variables support screening and tradeoff review, not automated approval |

Training-presence density and distance to the nearest included presence are excluded from explanatory models that seek independent siting conditions. They may be displayed separately for market context.

## 5.2 Feature documentation

Every feature records:

- source and access date;
- measurement year or effective period;
- original units and analytical units;
- coordinate reference system and spatial resolution;
- transformation and spatial-join method;
- missing-data handling;
- known coverage limitations; and
- whether it is a hard constraint, model feature, reporting variable, or sensitivity variable.

## 5.3 Feature screening before modeling

Feature selection begins with data and domain quality rather than model importance:

1. remove features with unacceptable coverage, inconsistent meaning, or temporal mismatch;
2. avoid duplicate encodings of the same source signal;
3. transform strongly skewed distances and costs where justified;
4. identify highly correlated feature groups;
5. preselect a small, interpretable baseline set; and
6. perform data-driven selection only inside training folds.

Statewide held-out outcomes are not used for feature selection before final evaluation.

---

# 6. Phase four: descriptive siting patterns

## 6.1 Maps and summaries

Map separately:

- all 61 Master locations and spatially usable Candidate locations as the mapped training sample;
- Candidate confidence weights through symbol size or another explicit visual channel;
- status, facility type, and analysis scope as descriptive overlays;
- coordinate precision and confidence;
- D0, D1, and D2; and
- coverage and missingness of major features.

## 6.2 Density and distance analysis

Use KDE and nearest-neighbor summaries to describe concentration. KDE bandwidths are selected before comparing results and evaluated across multiple scales. KDE does not show that a location is suitable or that clustering is statistically significant.

Compare the feature distributions of observed sites with D1 and D2 background locations. Report standardized differences, overlap, uncertainty, and metro-specific patterns before fitting complex models.

---

# 7. Phase five: presence-background and PU modeling

## 7.1 Statistical baseline

The primary inferential model is an inhomogeneous Poisson point process or an equivalent weighted presence-background model:

\[
\lambda(s)=\exp\left[\beta_0+f_{power}(s)+f_{network}(s)+f_{water}(s)+f_{market}(s)+f_{land}(s)+f_{risk}(s)\right]
\]

A regularized logistic regression or GAM fitted to observed sites and appropriately weighted background points may be used as a computational approximation. Its raw classification probability is not interpreted as the probability that a project will be built.

The baseline model provides effect direction and uncertainty, transparent response functions, and a relative intensity surface. It also provides a reference for evaluating more complex models.

## 7.2 Positive-unlabeled learning

Positive-unlabeled learning is the main supervised extension when Master records are full presences, eligible Candidate records are weighted presences, and the status of remaining feasible cells is unknown.

Candidate approaches include:

- bagging PU models that repeatedly treat subsets of unlabeled cells as temporary background;
- weighted logistic or tree-based models tested across assumed positive prevalence; and
- non-negative PU risk estimation if sample size and implementation checks support it.

PU outputs depend on coverage of the presence sample, Candidate weights, and assumptions about class prevalence. The analysis will report several Candidate-weight and class-prior scenarios when these values cannot be estimated credibly.

## 7.3 Supervised machine-learning benchmarks

Random Forest, gradient-boosted trees, or another nonlinear model may be compared with the statistical baseline after Gate C is satisfied. Model complexity must reflect the number of independent positive sites and spatial folds.

A complex model advances only if it improves spatially held-out ranking and remains stable across background draws. In-sample fit does not satisfy this requirement.

## 7.4 Model interpretation and feature importance

Model interpretation uses:

- standardized coefficients or smooth functions for the statistical baseline;
- held-out permutation importance within spatial folds;
- SHAP values for fitted machine-learning models;
- accumulated local effects or partial-dependence diagnostics when appropriate; and
- stability of feature rank, sign, and response shape across folds and background samples.

SHAP values describe how a fitted model distributes prediction contributions among its features. They do not show that a feature caused a site choice. Correlated variables can split or exchange importance, so SHAP and permutation results will be reported for individual features and predefined feature families.

Feature importance is not used as a one-pass filter on the full dataset. If importance guides feature reduction, that reduction occurs inside nested training folds and is compared with the predeclared baseline feature set.

---

# 8. Phase six: unsupervised learning and infrastructure regimes

## 8.1 Purpose

Unsupervised learning addresses this question:

> What recurring infrastructure, land, market, and risk environments exist across feasible Tennessee locations, and which environments contain more observed data centers than expected under the availability domain?

It supports structure discovery, regime mapping, feature diagnostics, and comparison with supervised results.

## 8.2 Regime workflow

Construct a feature vector for each D1 or D2 grid cell:

\[
X_i=[Power_i,Network_i,Water_i,Land_i,Market_i,Risk_i,Community_i]
\]

The primary workflow is:

\[
X\rightarrow PCA\rightarrow HDBSCAN\rightarrow Infrastructure\ Regimes\rightarrow Site\ Enrichment
\]

- PCA summarizes the main feature combinations and multicollinearity.
- HDBSCAN identifies stable environmental regimes without forcing every cell into a cluster.
- UMAP may support visualization, but its axes are not interpreted as physical factors.
- Regimes receive descriptive names based on their measured profiles.

For regime \(k\):

\[
ER_k=\frac{P(Regime=k\mid WeightedPresence)}{P(Regime=k\mid Availability)}
\]

Report enrichment, uncertainty, spatial scale sensitivity, parameter sensitivity, and the HDBSCAN noise share.

## 8.3 One-class similarity models

One-Class SVM, Isolation Forest, or related methods may identify areas whose feature profiles resemble or differ from the weighted presence sample. These are secondary similarity diagnostics. A different profile could indicate an unsuitable location or a new configuration that is absent from the training data.

One-class scores are not converted directly into final suitability grades.

---

# 9. Phase seven: spatial validation

## 9.1 Validation design

Primary evaluation uses:

- spatial block cross-validation;
- leave-one-metro-out validation;
- repeated background sampling;
- influence diagnostics for Nashville, Memphis, Knoxville, Chattanooga, and large individual campuses;
- sensitivity to D0, D1, and D2;
- sensitivity to grid scale and coordinate precision; and
- spatial block bootstrap or another spatially appropriate uncertainty method.

Hyperparameter tuning, feature selection, and preprocessing are performed inside the training portion of each spatial fold. Ordinary random train/test splitting is not used for primary evaluation.

## 9.2 Evaluation measures

Because background cells are unlabeled, evaluation emphasizes ranking and stability rather than ordinary classification accuracy. Report:

- weighted held-out presence rank and percentile;
- weighted top-decile and top-quintile capture of held-out locations;
- spatial lift over the relevant availability baseline;
- rank correlation across background samples and model versions;
- performance by withheld metro area;
- uncertainty intervals; and
- the share of high-scoring cells flagged as out of distribution.

ROC-AUC, precision-recall metrics, or Brier scores may be reported only with an explanation of how background sampling and assumed prevalence affect them.

## 9.3 External and prospective checks

All 61 Master records and all spatially usable Candidate records enter primary training under the stated weights. Candidate records without coordinates remain outside spatial fitting until location evidence is added. Future records added after the freeze are not used to revise an already registered evaluation model.

Facilities added after the freeze date provide the strongest prospective ranking test. Their evaluation must preserve the earlier model, candidate domain, features, and score version.

## 9.4 Residual spatial structure

After fitting the primary covariate model, use inhomogeneous Ripley's K or L with edge correction and Monte Carlo envelopes to test whether unexplained clustering remains. Distance ranges and global-envelope procedures are fixed before final inspection.

---

# 10. Phase eight: relative site scoring

## 10.1 Score structure

The scoring product reports four components:

1. feasibility status, based on documented hard constraints;
2. empirical siting affinity, based on the spatially validated model ranking;
3. decision context, including infrastructure, land, market, risk, and community measures; and
4. reliability, including predictive uncertainty, data coverage, coordinate sensitivity, and out-of-distribution status.

For feasible cell \(s\), the primary empirical score is a percentile transformation of ensemble predictions from models that have passed spatial out-of-fold evaluation:

\[
Score_{empirical}(s)=100\times PercentileRank\left(\hat{r}(s)\mid s\in D1\right)
\]

The score is relative to the versioned Tennessee D1 domain. It is recalculated when the domain, features, weights, or model version changes.

## 10.2 Decision score

A composite decision score may be produced after decision owners specify their priorities and noncompensable constraints. These weights are recorded separately from the learned model.

\[
Score_{decision}(s)=g\left(Score_{empirical},Infrastructure,Land,Market,Risk,Community\right)
\]

The function \(g\), component directions, normalization, and weights must be published with the score. A favorable result in one component cannot override a legal, physical, environmental, or utility constraint.

## 10.3 Score output

Each scored cell or candidate site reports:

- score version and candidate domain;
- empirical percentile score;
- component scores and raw feature values;
- spatial fold or ensemble uncertainty;
- data quality and missingness flags;
- out-of-distribution flag;
- strongest model contributions with their interpretation limits; and
- project-level checks that remain unresolved.

Score categories such as `higher priority for review`, `middle priority for review`, and `lower priority for review` may be defined from preregistered percentile ranges. These are screening categories, not permitting or investment recommendations.

---

# 11. Activation conditions for capacity and time

## 11.1 Capacity

Capacity-weighted analysis activates only when:

- capacity definition and units are consistent;
- reported and estimated values are distinguished;
- missingness and spatial coverage are acceptable;
- no single campus determines the statewide result; and
- leave-one-site-out conclusions remain stable.

Until then, capacity is descriptive and is excluded from the primary suitability model.

## 11.2 Time

Historical siting analysis activates only when opening-year coverage is adequate and feature layers can be aligned with plausible decision periods. Current infrastructure supports present-day spatial correspondence, not historical causal interpretation.

## 11.3 Facility composition

Facility type, analysis scope, and lifecycle status do not split the primary model. They remain descriptive metadata and are used to assess whether the pooled result mainly reflects one part of the 61-record Master and weighted Candidate sample.

---

# 12. Model and decision quality gates

## Gate A: Usable site objects

Required:

- reproducible campus-level canonicalization;
- complete crosswalk and cohort roles;
- explicit lifecycle and facility-type definitions;
- reviewed duplicate and coordinate issues; and
- a frozen weighted presence sample containing all 61 Master records and every eligible Candidate record.

## Gate B: Usable feature system

Required:

- statewide or documented partial coverage;
- consistent units, projections, years, and spatial resolution;
- reproducible feature construction;
- sampled validation of distances and overlays; and
- separation of hard constraints from ranking features.

## Gate C: Usable model

Required:

- enough effective weighted presences for the proposed model complexity;
- spatial folds with usable training and test positives;
- preprocessing and selection contained within folds;
- performance above the relevant background baseline; and
- conclusions that are not determined by one metro, campus, Candidate-weight choice, background draw, or feature definition.

If Gate C fails, the project reports descriptive associations and regime enrichment instead of a statewide predictive score.

## Gate D: Interpretable and stable features

Required:

- feature direction or importance is reasonably stable across folds;
- correlated-feature effects are disclosed;
- SHAP and permutation results are evaluated on held-out spatial data; and
- interpretation distinguishes prediction contribution from causal mechanism.

## Gate E: Decision-ready score

Required:

- the score has a defined decision owner and use case;
- domain, model, components, weights, and version are visible;
- uncertainty and out-of-distribution warnings accompany rankings;
- hard constraints cannot be offset by favorable model scores; and
- prospective monitoring and update rules are defined.

---

# 13. Adversarial review

The following findings would weaken the analysis or block release of the score:

1. power or network effects disappear under D2;
2. held-out metro performance is no better than the availability baseline;
3. removing Nashville, Memphis, or one large campus reverses conclusions;
4. changes to site canonicalization materially alter the result;
5. the mix of facility types or source coverage accounts for most of the network association;
6. high model performance results from spatial leakage or preprocessing outside folds;
7. feature importance or SHAP rankings change sharply across folds;
8. PU results depend strongly on an unsupported class-prior assumption;
9. rankings or feature importance change sharply across reasonable Candidate weights;
10. high-scoring regions are predominantly out of distribution;
11. unsupervised regimes are unstable across scale or parameters;
12. current features cannot represent the time at which older sites were selected; or
13. future sites do not rank favorably under the frozen model.

Negative and unstable results remain in the main report. Threshold, background, and feature choices will not be changed solely to remove them.

---

# 14. Deliverables

## 14.1 Data products

- versioned frozen source inventory and source audit;
- `canonical_sites` and `site_facility_crosswalk`;
- analytical cohort and data-quality report;
- `weighted_presence_cohort` with Master and Candidate weights;
- Candidate confidence-weight register and sensitivity scenarios;
- D0, D1, and D2 spatial domains;
- grid-level and site-level feature tables;
- repeated background-sample register;
- model training and spatial-fold register;
- statewide score table with uncertainty and flags; and
- model card and score-version documentation.

## 14.2 Figures

1. lifecycle- and type-stratified site maps;
2. coordinate uncertainty and missingness maps;
3. D0, D1, and D2 maps;
4. count KDE and feature-distribution comparisons;
5. statistical baseline effect plots;
6. spatially held-out performance by metro;
7. permutation-importance and SHAP stability plots;
8. PCA loadings and infrastructure-regime maps;
9. regime enrichment with uncertainty;
10. residual Ripley's L envelope; and
11. empirical score, uncertainty, and out-of-distribution maps.

## 14.3 Result tables

- canonicalization and cohort summary;
- feature definitions and quality status;
- hypothesis results;
- model comparison under spatial validation;
- sensitivity across availability domains and grid scales;
- leave-one-metro-out results;
- feature-importance stability;
- external and prospective ranking checks;
- score components and release status; and
- failed quality gates and unresolved limitations.

---

# 15. Tennessee workflow

```text
Frozen Multisource Tennessee Inventory
                |
                v
Canonical Sites and Crosswalk
                |
                +-- All 61 Master Records at Weight 1
                +-- Mappable Candidates at Confidence Weights
                +-- Duplicate and Coordinate Checks
                |
                v
Candidate Domains
                |
                +-- D0 Tennessee Land
                +-- D1 Feasible Land
                +-- D2 Urban and Industrial Matched
                |
                v
Feature System and Quality Audit
                |
                v
Observed Siting Patterns
                |
                +-- Maps and KDE
                +-- Feature Distributions
                |
                v
Modeling
                |
                +-- Point Process or Presence-Background Baseline
                +-- Positive-Unlabeled Learning
                +-- Nonlinear Supervised Benchmarks
                +-- Unsupervised Infrastructure Regimes
                |
                v
Spatial Validation and Interpretation
                |
                +-- Leave-One-Metro-Out
                +-- Repeated Background Samples
                +-- Permutation Importance and SHAP Stability
                +-- Residual K or L
                |
                v
Relative Tennessee Site Score
                |
                +-- Empirical Affinity
                +-- Decision Components
                +-- Uncertainty and OOD Flags
                |
                v
External and Prospective Validation
```

---

# 16. Immediate next step

The next task is to create an analysis-ready weighted presence sample and a versioned Tennessee candidate domain.

Required sequence:

1. produce `canonical_sites` and `site_facility_crosswalk` from the frozen workbook;
2. confirm that all 61 Master records enter once with weight 1;
3. add the 13 currently mappable Candidate records using the predeclared confidence weights;
4. resolve coordinates for the remaining three Candidate records and prevent Master-Candidate duplicate points;
5. reconcile every included raw record with a site or supporting-evidence role;
6. publish the Gate A missingness, weighting, and coordinate-uncertainty report;
7. define D1 hard constraints without using the features being tested;
8. define D2 matching or sampling strata;
9. select the first-version feature set and document source, year, unit, and resolution;
10. validate spatial joins on a small sample of presence and background cells;
11. preregister H1 through H4, Candidate weights, spatial folds, background draws, and evaluation measures; and
12. fit the transparent presence-background baseline before activating more complex models.

Unsupervised learning, PU learning, Random Forest, gradient boosting, feature importance, and SHAP follow only after the weighted presence sample, candidate domain, features, and spatial validation design are reproducible.
