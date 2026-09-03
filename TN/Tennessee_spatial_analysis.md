# Spatial Distribution of Tennessee Data Centers: A TN-First Research Workflow

## Research Positioning

> - Study area: Tennessee
> - Primary data source: dcmap.us
> - Current objective: establish a reproducible state-level analysis of spatial distribution and infrastructure association
> - Excluded from the current phase: national data integration, national model training, and future site prediction
> - Long-term direction: expand the same standard to other states only after the Tennessee workflow passes its data and statistical quality gates

This study does not treat Tennessee as a reduced version of a national analysis. It treats the state as a complete research object. The central question is:

\[
\boxed{
\text{After controlling for developable land and urbanization, do operating data centers in Tennessee remain concentrated in specific infrastructure environments?}
}
\]

The research sequence is:

\[
\text{Canonical Sites}
\rightarrow
\text{Observed Spatial Pattern}
\rightarrow
\text{Conditional Infrastructure Association}
\rightarrow
\text{Residual Clustering}
\rightarrow
\text{Exploratory Infrastructure Regimes}
\]

All conclusions are initially limited to observational spatial associations within Tennessee. Causal language such as "mechanism demonstrated" will not be used without independent temporal or policy evidence.

---

# 1. Current Research Boundaries

## 1.1 Study Population

The primary study population is:

\[
S_{op}=\{\text{deduplicated operational sites or campuses in Tennessee recorded by dcmap.us}\}
\]

Under Construction and Planned / Approved projects are retained separately and are not combined with Operational facilities in the primary point pattern.

| Status | Current use | Included in primary point pattern |
|---|---|---:|
| Operational | Facilities in service | Yes |
| Under Construction | Facilities being built | No; described separately |
| Planned / Approved | Announced or approved but not completed | No; described separately |
| Paused | Publicly stalled but not abandoned | No |
| Cancelled | Publicly abandoned projects retained by dcmap.us as development records | No |

## 1.2 Questions Not Addressed in This Phase

This phase does not determine:

- where future data centers should be built in Tennessee;
- whether a data center will necessarily be built at a particular location;
- whether Tennessee findings directly represent the United States; or
- whether any infrastructure variable causally determines data-center development.

## 1.3 Boundary for Future Expansion

The project may later expand beyond Tennessee, but the current phase retains only the following portable requirements:

- stable definitions of sites and facilities;
- consistent field names, units, and temporal conventions;
- preserved source, version, and processing records;
- replaceable state boundaries and candidate domains; and
- no national data download or analysis during the Tennessee phase.

---

# 2. Research Questions and Preregistered Hypotheses

Primary hypotheses must be fixed before final significance results are inspected. PCA, HDBSCAN, and UMAP results must not be used to revise the primary hypotheses after the fact.

## H1: Association With Electric Infrastructure

> After controlling for developable land, urbanization, and market location, operating data centers remain closer than available space to substations or high-voltage transmission environments.

Observations that may support H1 include:

- significantly shorter site-to-substation distances under a conditional background;
- a stable effect direction for electric variables in the point-process model; and
- consistent conclusions across alternative spatial partitions.

Observations that may reject or weaken H1 include:

- disappearance of the effect after controlling for urbanization;
- results driven only by a small number of Nashville or Memphis sites; or
- reversal of the effect under a different definition of developable land.

## H2: Association With Network Infrastructure

> Operating data centers occur more frequently in areas with commercial high-speed fiber coverage or strong network accessibility.

Interpretations to avoid:

- fiber-provider count may merely proxy for urbanization;
- present-day fiber coverage does not automatically explain historical sites; and
- the number of published records is not necessarily the number of independent providers.

## H3: Independent Roles of Market and Infrastructure

> Associations with electric or network infrastructure cannot be explained entirely by proximity to urban markets.

If electric and network variables lose stability after market and population controls are added, report:

> The current data do not show an independent association beyond the urbanization background.

## H4: Differences by Capacity Scale

> The spatial structure of Tennessee data centers differs when measured by site count versus MW-weighted capacity.

This hypothesis compares count geography with capacity geography; it does not assume that either representation is inherently more correct.

---

# 3. Phase One: Build the dcmap.us Tennessee Canonical Dataset

Define the data objects before conducting any spatial statistics. This phase is a research quality gate, not a routine cleaning step.

## 3.1 Two Units of Analysis

### Site/Campus Level

Used for:

- point-pattern analysis;
- KDE maps;
- Ripley's K/L; and
- infrastructure association.

### Facility/Building Level

Used for:

- building counts;
- capacity aggregation;
- campus expansion; and
- development intensity.

Principle:

\[
\boxed{\text{One physical campus contributes only one site point to the primary spatial analysis}}
\]

## 3.2 Recommended Core Fields

| Field | Meaning | Primary use |
|---|---|---|
| site_id | Deduplicated physical-site identifier | Primary analytical key |
| facility_id | dcmap.us facility-record identifier | Source tracing |
| parent_site_id | Site or campus containing the facility | Parent-child relationship |
| site_name | Normalized site name | Manual review |
| operator | Publicly associated operating brand | Deduplication support and description |
| owner / developer / anchor_tenant | Owner, developer, and principal tenant when public | Role separation and description |
| latitude / longitude | Site coordinates | Spatial joins |
| coordinate_precision | Coordinate precision class | Uncertainty analysis |
| county / market | Administrative area and market | Stratification and matching |
| status | Operational and other project states | Sample stratification |
| facility_type | Standardized type | Heterogeneity analysis |
| capacity_mw | Reported or estimated nameplate/planned capacity, not current load | Capacity weighting |
| capacity_estimated | Whether capacity is reported or estimated | Capacity uncertainty analysis |
| opening_year / milestone_date | First operating year or public project milestone | Temporal analysis |
| source_snapshot_date | Data snapshot date | Reproducibility |
| source_url | Source page | Audit |
| review_flag | Whether manual judgment is required | Quality control |

## 3.3 Site Deduplication Sequence

1. Use campus structures or multi-building relationships recorded by dcmap.us.
2. Compare normalized names, operators, and addresses.
3. Compare coordinate distance and shared-campus evidence.
4. When multiple buildings belong to one campus, retain all facility members but create only one site.
5. Do not automatically merge nearby facilities based on distance alone when operators, addresses, or campus evidence differ.
6. When evidence is inconclusive, retain separate sites and set `review_flag` instead of forcing a merge.

Produce at least two tables:

| Table | Contents |
|---|---|
| canonical_sites | One row per independent site |
| site_facility_crosswalk | Mapping of each facility to a site, including the supporting rationale |

## 3.4 Source Audit

Record the following before analysis:

- the method and date of the dcmap.us snapshot;
- dcmap.us terms of use, authorization for record-level access, and redistribution restrictions;
- total Tennessee record count;
- Campus, Facility, and Building structure;
- status definitions;
- coordinate precision;
- missingness for capacity, `capacity_estimated`, and temporal fields;
- coverage by facility type; and
- potential inclusion bias introduced by compiling public records.

Do not describe dcmap.us as a complete Tennessee census before validation. Use this wording:

> Tennessee data-center sites identifiable in dcmap.us.

The public dcmap.us Agent API provides aggregate results only, and its terms do not permit bulk scraping or copying of the underlying dataset. Record-level spatial analysis in this proposal must therefore use an explicitly authorized dcmap.us export or another licensed record-level access method. Public state summary pages may be used to check totals, but not as a substitute for the analytical table.

---

# 4. Phase Two: Define the Tennessee Availability Background

The study does not label random locations as "failed projects," but it must define an availability domain in which data-center development could plausibly be considered.

## 4.1 Three Spatial Backgrounds

### D0: Tennessee Land Baseline

All land within the state, used only as the broadest descriptive baseline.

### D1: Developable-Land Baseline

Exclude clearly unsuitable areas, including:

- major water bodies;
- protected land;
- clearly unacceptable slopes;
- airport runway safety zones;
- restricted military areas; and
- other land classes known to be undevelopable.

D1 is the primary inferential background.

### D2: Urban/Industrial Matched Baseline

Generate matched background locations within comparable metro, industrial, or developed-land environments. Use D2 to test whether electric, network, and water variables are merely proxies for urbanization.

## 4.2 Avoiding Circular Controls

Do not define the background with the variable being tested.

For example:

- when testing substation distance, do not define D1 as "within 2 km of a substation";
- when testing water-service distance, do not first remove every location far from a water-service area; and
- when testing fiber distance, do not use fiber coverage to define the candidate domain.

Otherwise, the study design predetermines the conclusion.

## 4.3 Spatial Scale

Use one fixed equal-area grid or H3 resolution as the primary spatial unit. Counties and Census tracts are for description or sensitivity analysis only.

Compare at least:

- the primary scale;
- one finer scale; and
- one coarser scale.

If the direction of a finding changes by scale, report scale instability instead of retaining only the most significant result.

---

# 5. Phase Three: Descriptive Spatial Distribution

This phase describes where facilities are located; it does not make mechanistic or significance claims.

## 5.1 Base Maps

Map separately:

- Operational sites;
- Under Construction sites;
- Planned / Approved sites;
- facility type;
- site count;
- capacity-weighted symbols; and
- coordinate precision or missing status.

Do not combine Operational, Under Construction, and Planned / Approved records into one "existing sites" layer.

## 5.2 Two Spatial Representations

### Site-count geography

\[
\lambda_{count}(s)
\]

Give every independent site a weight of 1.

### Capacity geography

\[
\lambda_{MW}(s)
\]

Weight sites by verifiable MW capacity.

Do not automatically fill missing capacity with zero. Capacity maps must also report:

- the percentage of sites with recorded capacity;
- spatial coverage of the known-capacity sample; and
- whether missingness is concentrated in a particular facility type.

## 5.3 Role of KDE

Use KDE to:

- display local density around Nashville, Memphis, Knoxville, Chattanooga, and other markets;
- compare count and capacity hotspots; and
- assess map stability across bandwidths.

KDE alone is not evidence of statistical significance. Compare at least 5, 10, 20, and 30 km bandwidths, or select a data-driven bandwidth from nearest-neighbor distances and conduct sensitivity analysis.

---

# 6. Phase Four: Primary Statistical Tests

## 6.1 Preferred Method: Conditional Spatial Point Process

Use an inhomogeneous Poisson point process, or an equivalent case-availability approximation, as the primary model:

\[
\lambda(s)
=
\exp
\left[
\beta_0+
f_{power}(s)+
f_{fiber}(s)+
f_{water}(s)+
f_{market}(s)+
f_{land}(s)
\right]
\]

Background points provide numerical integration or sampling over the availability domain; they do not represent actual failed projects.

## 6.2 First-Version Core Variables

| Factor | First-version variables | Interpretation boundary |
|---|---|---|
| Electric power | Substation distance, transmission-line distance, voltage class | Proximity does not imply spare capacity |
| Network | Commercial high-speed fiber coverage, provider count, or record count | Keep record count separate from independent-provider count |
| Water | Distance to public water-service areas | Service coverage does not imply project-level water availability |
| Market | Metro distance, population, or employment density | Controls for urbanization |
| Land | Developable land, slope, and land-value proxies | Distinguish historical from current years |
| Transportation/risk | A limited set of stable, interpretable variables | Do not accumulate low-quality fields |

Existing data-center density must not enter a regime or association model as an explanatory variable because data-center location is the outcome itself.

## 6.3 Temporal Boundary of Variables

A primary cross-sectional analysis may use one current snapshot, but it can explain only:

> The spatial correspondence between current sites and current infrastructure environments.

Historical siting conditions can be interpreted only when infrastructure data near each `opening_year` are available. Current infrastructure must not be treated as a direct decision-time variable for early sites.

## 6.4 Validation Strategy

Do not use an ordinary random train/test split. Use:

- spatial cross-validation by metro area or spatial block;
- leave-one-metro-out sensitivity analysis;
- influence diagnostics for Nashville, Memphis, and other individual areas;
- spatial block-bootstrap confidence intervals; and
- sensitivity analysis for variable definitions and background domains.

## 6.5 Primary Results to Report

Report:

- effect direction;
- effect size and confidence interval;
- out-of-area validation performance;
- stability across background domains;
- whether results are driven by a single metro area; and
- findings that do not support the hypotheses.

Statistical significance is not a substitute for effect size and spatial stability.

---

# 7. Phase Five: Residual Spatial Clustering

After fitting the primary covariate model, use inhomogeneous Ripley's K/L to test:

> After controlling for developable land, market, electric, network, and water environments, does unexplained clustering of data centers remain?

Requirements:

- use edge correction for the Tennessee boundary;
- use the same availability domain as the primary model;
- compare results with a Monte Carlo envelope;
- preregister the distance range; and
- avoid uncorrected significance interpretations at every individual distance.

The distance scale may begin at 1, 5, 10, 20, 50, and 100 km, but the final range must reflect the number and spatial scale of Tennessee sites.

Use ordinary nearest-neighbor analysis only as an intuitive supplement, not as the primary inferential evidence.

---

# 8. Phase Six: Exploratory Infrastructure Regimes

This phase is exploratory and does not contribute significance claims to the primary hypotheses.

## 8.1 Analytical Units

Construct an infrastructure vector for every spatial cell in the D1 or D2 background:

\[
X_i=[
Power_i,
Fiber_i,
Water_i,
Land_i,
Market_i,
Hazard_i
]
\]

Transform skewed distance and cost variables before standardization.

## 8.2 Recommended Workflow

\[
X
\rightarrow
PCA
\rightarrow
HDBSCAN
\rightarrow
Infrastructure\ Regimes
\rightarrow
DC\ Enrichment
\]

- Use PCA to explain the principal infrastructure dimensions.
- Use HDBSCAN to identify stable environmental types.
- Use UMAP only as a supporting visualization.
- Do not interpret UMAP axes.
- Do not label clusters directly as high, medium, or low suitability.

## 8.3 Regime Enrichment

\[
ER_k=
\frac{P(Regime=k\mid DC)}
{P(Regime=k\mid Availability)}
\]

Use D1 or D2 availability in the denominator, rather than statewide area as the only baseline.

Report:

- enrichment ratio;
- log enrichment;
- spatial block-bootstrap confidence intervals;
- stability across spatial scales and cluster parameters; and
- the HDBSCAN noise percentage.

If Regime A merely represents urban locations, name it an "urban infrastructure regime" rather than inventing an overly abstract mechanism.

---

# 9. Activation Conditions for Facility Type, Capacity, and Time

## 9.1 Facility-Type Analysis

The dcmap.us categories Hyperscale, Colocation, Enterprise, and Neocloud may be stratified only when:

- type definitions map consistently;
- each class contains enough independent sites;
- one campus does not dominate the result; and
- coordinate and key-feature coverage is acceptable.

When samples are insufficient, report descriptive statistics only or combine records into a small number of physically meaningful groups.

## 9.2 Capacity Analysis

Capacity-weighted analysis enters the primary results only when:

- capacity is consistently interpreted under the dcmap.us definition as nameplate or planned capacity, not current operating load;
- reported and estimated capacity are reported separately and subjected to sensitivity analysis;
- missingness patterns are reported; and
- the influence of exceptionally large sites is tested with leave-one-site-out analysis.

## 9.3 Temporal Analysis

Temporal development is an optional later module. Activate it only when:

- `opening_year` coverage is sufficient;
- each period contains enough independent sites;
- status and year definitions are consistent;
- key infrastructure layers have historical versions; and
- inclusion-time bias in the current database can be evaluated.

Otherwise, describe only the present-day spatial distribution of different opening cohorts; do not characterize the result as a change in historical siting mechanisms.

---

# 10. Method Tiers and Priorities

## 10.1 Primary Methods

- Campus/site canonicalization;
- developable-land availability domain;
- conditional point-process model; and
- spatial cross-validation.

## 10.2 Secondary Diagnostics

- KDE;
- count and capacity maps;
- inhomogeneous Ripley's K/L;
- leave-one-metro-out analysis; and
- matched Monte Carlo analysis.

## 10.3 Exploratory Methods

- PCA;
- HDBSCAN;
- regime enrichment;
- UMAP visualization; and
- facility-type and temporal stratification.

## 10.4 Methods Not Treated as Core in the Current Phase

- running Moran's I, LISA, and every Getis-Ord test on raw counts;
- using DBSCAN to force a small number of data-center points into market clusters;
- basing primary conclusions on statewide uniform-random results;
- explaining data-center distribution with existing data-center density;
- revising preregistered hypotheses or analytical thresholds in response to Tennessee results; and
- describing unsupervised clusters as suitability grades.

---

# 11. Multiple Testing and Interpretation

Keep the number of primary hypotheses limited. H1-H4 should be preregistered; all other analyses should be labeled exploratory.

When testing multiple infrastructure variables, distance thresholds, or facility types:

- report the total number of tests;
- use FDR or another appropriate correction;
- report effect sizes and confidence intervals;
- retain nonsignificant results; and
- do not choose bandwidth, spatial scale, or background domain based on significance.

Separate the language of conclusions into:

- **Observed evidence:** results calculated directly from the data;
- **Model inference:** associations obtained under model assumptions;
- **Candidate explanation:** possible infrastructure or market explanations; and
- **Unresolved:** alternative explanations that the data cannot distinguish.

---

# 12. Adversarial Review: What Would Weaken the Findings?

Treat the following as material counterevidence or limitations:

1. Electric and network effects disappear after controlling for the urban/industrial background.
2. Findings are significant only under a statewide uniform background.
3. Removing either Nashville or Memphis reverses the effect direction.
4. Small changes to site-deduplication rules substantially change the clustering result.
5. dcmap.us coordinates or statuses contain systematic errors.
6. Capacity results are entirely driven by one exceptionally large campus.
7. PCA/HDBSCAN regimes change sharply across spatial scales or parameter settings.
8. Current infrastructure variables cannot represent conditions in each site's development year.
9. The public-record compilation method used by dcmap.us materially undercounts small, private, or early-stage facilities.

Do not hide these outcomes in average metrics. Include them in the main limitations or sensitivity analysis.

---

# 13. Tennessee-Phase Deliverables

## 13.1 Data Products

- documentation of the authorized dcmap.us Tennessee snapshot;
- `canonical_sites`;
- `site_facility_crosswalk`;
- status and facility-type mapping tables;
- capacity and `opening_year` missingness reports;
- Tennessee availability domains;
- site-to-infrastructure feature table; and
- source, year, unit, and spatial-processing documentation for each feature.

## 13.2 Figures

1. Stratified Tennessee maps for Operational, Under Construction, and Planned / Approved facilities;
2. site-count KDE;
3. capacity-weighted KDE;
4. D0, D1, and D2 background maps;
5. distributions of primary infrastructure distances;
6. spatial point-process effect plots;
7. residual Ripley's L envelope;
8. PCA loading and regime maps;
9. regime enrichment with confidence intervals; and
10. missing-data and coordinate-precision maps.

## 13.3 Result Tables

- canonicalization summary;
- primary hypotheses and statistical results;
- sensitivity across availability domains;
- leave-one-metro-out results;
- count-versus-capacity differences;
- exploratory regime stability; and
- failed data quality gates.

---

# 14. Phase Quality Gates

## Gate A: Usable Data Objects

Required:

- parent-child relationships are resolved;
- site-deduplication rules are reproducible;
- status definitions are explicit; and
- coordinate errors and duplicate records have review outcomes.

Stop spatial statistics if these conditions are not met.

## Gate B: Usable Primary Spatial Variables

Required:

- infrastructure layers cover Tennessee;
- units and projections are consistent;
- layer years are recorded; and
- sampled checks validate distance and overlap calculations.

Publish descriptive maps only if these conditions are not met.

## Gate C: Usable Statistical Inference

Required:

- enough independent Operational sites exist for the selected model;
- spatial folds do not create empty test regions;
- one metro area does not completely drive the findings; and
- sensitivity analyses can be run.

Do not report strong inference if these conditions are not met.

## Gate D: Usable Extension Modules

Activate facility-type, capacity, and temporal analyses only after each passes its own sample-size, definition, and temporal requirements. They are not required components of the primary workflow.

---

# 15. Optimized Tennessee Workflow

```text
dcmap.us Tennessee Authorized Snapshot
            |
            v
Source and License Audit
            |
            v
Campus / Site Canonicalization
            |
            +-- canonical_sites
            +-- site_facility_crosswalk
            |
            v
Status and Type Stratification
            |
            v
Tennessee Availability Domains
            |
            +-- D0 State Land
            +-- D1 Developable Land
            +-- D2 Urban/Industrial Matched
            |
            v
Descriptive Mapping
            |
            +-- Operational / Under Construction / Planned or Approved
            +-- Site Count
            +-- Capacity Weighted
            |
            v
Conditional Point-Process Analysis
            |
            +-- Power
            +-- Fiber
            +-- Water
            +-- Market
            +-- Land
            |
            v
Spatial Validation and Residual K/L
            |
            v
Exploratory Infrastructure Regimes
            |
            +-- PCA
            +-- HDBSCAN
            +-- Enrichment
            |
            v
Optional Type / Capacity / Temporal Modules
            |
            v
Tennessee Findings and Limitations
```

---

# 16. Most Important Next Step

Do not begin by calculating KDE or PCA or by training a model. The first task is to complete:

\[
\boxed{\text{dcmap.us Tennessee Canonical Site Table}}
\]

Sequence:

1. Obtain and freeze an authorized record-level dcmap.us snapshot for Tennessee.
2. List the raw fields, status values, and facility types.
3. Establish Campus and child-facility relationships.
4. Produce the deduplicated site-level result.
5. Manually review ambiguous merges.
6. Count independent Operational sites.
7. Report capacity, `opening_year`, and coordinate precision.
8. Use the actual sample size to determine which analytical modules can begin.

After completing these steps, select the primary spatial unit, availability domain, and first-version infrastructure variables. National expansion is outside the current phase and must not influence the definition of Tennessee data objects or primary hypotheses.
