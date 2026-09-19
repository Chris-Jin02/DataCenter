# Phase 3 Notebook archive

[Phase 3 overview](../README.md) · [Result workbooks](../results/) · [Shared helpers](../../notebook_support/README.md)

This directory contains the two notebooks listed below. Their output workbooks and figures are stored in `../results/`; their shared imports are maintained in `../../notebook_support/`. See the [model execution-layout notes](../../README.md) for the current root and output-path requirements.

This directory is the permanent home for executable Phase 3 notebooks. Keep each notebook together with the result workbook it produces. Do not remove a notebook when retaining its result.

The original notebooks for 3A–3G were removed under the earlier result-only retention instruction. They are not present in the workspace, Git history, temporary files, or local editor history, so an exact byte-for-byte recovery is not possible. Any reconstructed notebook must state its source inputs, frozen Phase 2 hash, output workbook, validation checks, and the fact that it is reconstructed.

Future Phase 3 work begins here and retains both code and final outputs.

## Retained notebooks

- [Phase 3 final model training and D1 scoring](phase3_final_model_training.ipynb) contains the final Primary-only model source, stable released-workbook export, numerical tests, and Matplotlib PNG result displays.
- [Phase 3 training, comparison, and visualization](phase3_model_training_comparison_visualization.ipynb) reads only the frozen Phase 2 dataset, produces a new retained result workbook without overwriting the established 3A–3G workbooks, and writes the score-map and regime-space Matplotlib PNG visualizations.
