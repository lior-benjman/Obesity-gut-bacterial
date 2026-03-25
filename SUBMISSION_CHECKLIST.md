# Submission Checklist (Stage 2)

Use this checklist before final submission. The first section is the lecturer-focused pass and should be treated as mandatory.

## Lecturer-Focused Must-Fix Items
- [ ] The oral story is one pipeline: data challenges -> preprocessing -> statistics -> prediction -> interpretation.
- [ ] The paper includes one explicit bridge from significant taxa to predictive interpretation.
- [ ] The defense answer for each stage has exact inputs and outputs, not vague descriptions.
- [ ] We can say exactly which findings come from the full cohort, which from train-only processing, and which from the hold-out test.
- [ ] Exploratory PCA / XGBoost / RFE cells are clearly separated from the core report and are not used as primary evidence.
- [ ] Any claim that one model is better than another is backed by the shared-split significance-testing step, or else described only as descriptive.

## Required Deliverables
- [ ] Final paper submitted as an English PDF (`<= 8` pages).
- [ ] GitHub repo link included in submission.
- [ ] `README.md` matches the final paper and actual notebook logic.
- [ ] Full analysis is reproducible from repository contents.
- [ ] Dataset files required for reproduction are included in the repo.

## Paper Quality
- [ ] The paper reads as one coherent story, not as disconnected tests.
- [ ] The bridge between statistical findings and model design is explicit.
- [ ] Methods describe actual implementation choices, not generic textbook definitions.
- [ ] Results distinguish clearly between association findings and predictive findings.
- [ ] Discussion separates observed results from biological interpretation and from speculation.

## Scientific Rigor
- [ ] Train / validation / test roles are stated explicitly.
- [ ] Metrics are reported on the correct split.
- [ ] Multiple-testing correction is documented.
- [ ] Any model comparison claim is either statistically tested or clearly labeled as descriptive only.
- [ ] Limitations are stated honestly: no causality claim, no external validation, no overclaiming.

## Figures and Tables
- [ ] Axes have titles and readable labels.
- [ ] Colors are meaningful and consistent.
- [ ] Figure captions explain what the figure supports in the story.
- [ ] Confusion matrices and threshold analyses are numerically consistent with the text.

## Reproducibility
- [ ] Python dependencies are pinned in `requirements.txt`.
- [ ] Optional data refresh is documented in `Data/curated_data.ipynb` or `Data/curated_data.R`.
- [ ] `research.ipynb` runs top-to-bottom.
- [ ] Reported metrics in README, paper, and notebook match.

## Oral Defense Readiness
- [ ] `EXPLICIT_EXPLANATIONS.md` exists and is accurate.
- [ ] We can explain why log transform was used.
- [ ] We can explain what each pipeline stage takes as input and produces as output.
- [ ] We can explain exactly where each key result was found.
- [ ] We can explain why the statistics and the models are one connected workflow.
