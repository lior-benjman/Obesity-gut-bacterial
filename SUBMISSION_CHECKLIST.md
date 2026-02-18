# Submission Checklist (Stage 2)

Use this checklist before final submission.

## Required Deliverables

- [ ] Final paper submitted as **English PDF** (`<= 8` pages).
- [ ] GitHub repo link included in submission.
- [ ] Detailed `README.md` exists with exact run instructions.
- [ ] Full analysis is reproducible from repository contents.
- [ ] Dataset files required for reproduction are included in the repo.

## Paper Structure (must appear in the PDF)

- [ ] `Abstract`: background, main result(s), conclusion.
- [ ] `Introduction`: literature context and research motivation.
- [ ] `Results`: hypothesis-driven results with figures/tables.
- [ ] `Methods`: practical implementation details (not textbook theory).
- [ ] `Discussion`: conclusions, limitations, and implications.

## Analysis Quality Expectations

- [ ] The work is presented as a coherent story (not disconnected tests).
- [ ] Visualizations are readable (labels, titles, colors, captions).
- [ ] Train/validation/test logic is clear and methodologically sound.
- [ ] Metrics are reported clearly (AUC, precision, recall, F1, etc.).
- [ ] Statistical testing details are documented (including multiple-testing handling when applicable).

## Reproducibility Checks

- [ ] Environment/dependencies are pinned (`requirements.txt`).
- [ ] Data acquisition path is documented (`Data/curated_data.ipynb` for optional refresh).
- [ ] Main notebook runs in order (`research.ipynb`).
- [ ] Random seeds and split strategy are documented.

## Final Sanity Pass

- [ ] Remove machine-specific/noisy warning output from notebook where possible.
- [ ] Verify file paths are relative and repo-portable.
- [ ] Confirm no broken references in README or notebook.
