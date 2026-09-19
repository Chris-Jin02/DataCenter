# Phase 3 release closeout

Status: complete. Phase 4 released this frozen specification as `TN-DC-1.0.0`.

## Decision

The released supervised specification is `pls_logistic`, selected from the
Elastic Net, PLS-logistic, spline-logistic, and constrained boosted-stump
candidates under the registered spatial-fold comparison. The winner's worst
fold median weighted AUC is `0.7609467455621302`; its fifth-percentile
weighted AUC is `0.749378698224852`.

The release retains 21 standardized Phase 2 features and 20 deterministic
Primary-cohort 10:1 background draws. The published score is the percentile of
the median prediction across those draw-specific models against the 4,391
eligible D1 cells.

The three-feature `screened_logistic` result remains a transparent Phase 3
development benchmark. It is not the Phase 4 release model and does not define
the `TN-DC-1.0.0` score.

## Frozen evidence

| Item | Value |
|---|---|
| Phase 2 workbook | `TN/model/phase 2/dataset/phase2_model_dataset.xlsx` |
| Phase 2 SHA-256 | `112d6db67d7f4f9e74fa8edde3406937e1f8eb7145e9bc04a64e7030cf1d3e03` |
| Model weights | `TN/model/phase 3/results/phase3_final_model_weights.json` |
| Model weights SHA-256 | `4a8bfdbc6368ad61150c4aee1a94ea516fe7d9dc7b850b691554258a0319fa56` |
| Final scoring workbook | `TN/model/phase 3/results/phase3_final_multilocation_scoring.xlsx` |
| Final scoring workbook SHA-256 | `10bea5146ae63953030e1713d0dc155d1266633ef004b5a0b675d3ecb802f09e` |
| Selected model | `pls_logistic` |
| Feature count | 21 |
| Primary draw count | 20 |
| Score reference | 4,391 eligible D1 cells |

## Handoff

Phase 4 consumes the weight package directly. It does not retrain, select a
model, alter a coefficient, or substitute the Phase 3 benchmark. The released
interface contains the Primary score, draw uncertainty, D1 regime context, and
novelty flags. Weighted and Strict scenario outputs remain development
evidence until a future version freezes and verifies them as release fields.
