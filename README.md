# Gut Microbiome and Obesity: Deep Learning and Statistical Analysis

**Course:** Machine Learning and Statistics in Medical Applications  
**Final Project: Phase 2**

This repository contains an end-to-end microbiome analysis workflow for studying obesity. The project combines statistical screening, tabular machine learning, and phylogeny-aware deep learning through iMic.

## Project Story
The project is built around one connected question, not two separate tasks:
1. **Do Lean and Obese participants differ at the microbiome level?**
2. **If they do, is that microbial signal strong enough to support prediction on unseen samples?**

The workflow is therefore:
`data challenges -> preprocessing -> statistical testing -> model design -> hold-out evaluation -> interpretation`

This is the intended connection between the statistical and predictive parts of the work.

## Main Findings
- Five taxa passed `FDR < 0.1` after Mann-Whitney U testing with Benjamini-Hochberg correction.
- `Fretibacterium_fastidiosum` was the strongest Lean-associated signal.
- `Clostridium_sp_CAG_58` was enriched in Obese samples.
- On the shared hold-out split, Logistic Regression reached AUC `0.700`, Random Forest reached AUC `0.629`, and iMic reached AUC `0.783`.
- At iMic threshold `0.3`, recall for Obese cases reached `1.00`, with more false positives among Lean samples.

Important limitation: model comparisons are descriptive in the current repo. A formal significance test between model performances was not completed.

## Repository Structure
```text
Data/
  curated_data.ipynb                      # Runnable R notebook for refreshing the raw study tables
  curated_data.R                          # Same refresh logic as a plain R script
  Raw_LeChatelier_metadata.csv            # Metadata used in the project
  Raw_LeChatelier_relative_abundance.csv  # Relative-abundance table used in the project
research.ipynb                            # Main analysis notebook
Final_Paper_Stage2.md                     # Main paper draft in markdown
EXPLICIT_EXPLANATIONS.md                  # Direct explanations for defense questions and unclear steps
scriptpdf.py                              # Script for regenerating the PDF summary artifact
requirements.txt                          # Python dependencies
README.md                                 # Repo overview and run instructions
SUBMISSION_CHECKLIST.md                   # Final submission checklist
```

## Reproduction Instructions
### 1. Python Environment
Use **Python 3.12.x**.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Optional Data Refresh in R
The CSV files already required for this project are committed to the repo.

If you want to refresh them from `curatedMetagenomicData`, use either:
- `Data/curated_data.ipynb` in an R / IRkernel environment
- `Data/curated_data.R` as a plain R script

### 3. Main Analysis Flow
Run `research.ipynb` from top to bottom.

The notebook currently follows this structure:
- **Part A:** cohort definition and MIPMLP preprocessing
- **Part B:** exploratory analysis of sparsity, skewness, and class balance
- **Part C:** Mann-Whitney + FDR statistical screening
- **Part D:** Logistic Regression and Random Forest baselines
- **Part E:** iMic image conversion, CNN tuning, and threshold analysis
- **Part F:** exploratory extensions from the lectures

### 4. Split Logic
This is the most important methodological point to understand before running or defending the project.

- **Training split:** model fitting and any training-only tuning steps
- **Internal validation inside training:** iMic hyperparameter tuning
- **Hold-out test split:** final reporting only

All primary model comparisons in the report are based on the same shared hold-out split.

## Why the Statistical and Modeling Parts Belong Together
The project should be read in this order:
1. The microbiome data are sparse, skewed, and high-dimensional.
2. That motivates non-parametric testing and careful preprocessing.
3. Statistical testing identifies taxa that differ between Lean and Obese groups.
4. Predictive models test whether the same microbiome signal generalizes to unseen individuals.
5. Threshold calibration shows how the model behaves under a screening-oriented objective.

The statistics answer: **is there a biological signal?**  
The models answer: **is that signal predictive?**

## Reported Hold-out Results
| Model | AUC | Accuracy | Precision | Recall | F1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression (`thr = 0.5`) | 0.700 | 0.679 | 0.750 | 0.727 | 0.738 |
| Random Forest (`thr = 0.5`) | 0.629 | 0.566 | 0.679 | 0.576 | 0.623 |
| iMic (`thr = 0.5`) | 0.783 | 0.679 | 0.667 | 0.970 | 0.790 |
| iMic (`thr = 0.3`) | 0.783 | 0.698 | 0.673 | 1.000 | 0.805 |

## Biological Interpretation Notes
The paper discusses two leading taxa:
- `Fretibacterium_fastidiosum` as a Lean-associated signal
- `Clostridium_sp_CAG_58` as an Obese-associated signal

These interpretations are framed as **plausible biological hypotheses**, not as proof of causation. The dataset is observational and cross-sectional.

## Defense Preparation
For the questions the lecturer emphasized, see:
- `EXPLICIT_EXPLANATIONS.md`

That file explains:
- why the log transform was used
- what each pipeline stage takes as input and produces as output
- what belongs to train, validation, and test
- how the statistics connect to the models
- how to talk about MIPMLP and iMic without hand-waving

## Authors
- **Lior Ben Jashar**
- **Yarin Ifrah**
