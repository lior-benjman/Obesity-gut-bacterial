# Gut Microbiome and Obesity: Deep Learning & Statistical Analysis

**Course:** Machine Learning and Statistics in Medical Applications  
**Final Project: Phase 2**

This repository contains the complete research pipeline for analyzing the relationship between gut bacterial taxa and obesity. It combines statistical testing, tabular machine learning, and a deep learning approach (**iMic**) that converts microbiome data into phylogenetic images.

---

## Project Overview

**Research Question:** Which gut bacterial taxa are associated with obesity (BMI >= 30) vs. Lean status (BMI <= 25), and can deep learning on phylogenetic images outperform traditional tabular models in predicting obesity?

**Key Findings (from current notebook outputs):**
1. **Protective signatures:** High abundance of specific commensal bacteria (e.g., *Fretibacterium fastidiosum*) is associated with the Lean phenotype.
2. **Model performance:** In 5-fold CV, Logistic Regression reaches AUC ~0.70 and Random Forest ~0.74. On the shared hold-out split, Logistic Regression and Random Forest reach AUC ~0.70, while iMic achieves AUC ~0.80.
3. **Clinical calibration:** Shifting the decision threshold from 0.5 to 0.3 improves sensitivity for Obese cases while maintaining high precision (see `research.ipynb`).

---

## Repository Structure

```
Data/
  curated_data.ipynb                      # R notebook to re-download the raw data
  Raw_LeChatelier_metadata.csv            # Processed metadata
  Raw_LeChatelier_relative_abundance.csv  # Processed taxa abundance
research_images/                          # Generated phylogenetic images (iMic)
logs/                                     # PyTorch Lightning logs
checkpoints/                              # Model checkpoints
research.ipynb                            # Main analysis notebook (run this)
README.md                                 # Project documentation
```

---

## Reproduction Instructions

### 1. Prerequisites & Environment
Ensure you have **Python 3.8+** installed. Key libraries:
- `torch`, `pytorch-lightning` (deep learning)
- `MIPMLP` (microbiome preprocessing & image generation)
- `optuna` (hyperparameter optimization)
- `scikit-learn`, `imbalanced-learn` (ML & sampling)
- `pandas`, `seaborn`, `matplotlib` (data manipulation & plotting)

Install:
```bash
pip install torch pytorch-lightning optuna scikit-learn pandas seaborn matplotlib imbalanced-learn mipmlp scipy xgboost
```

### 2. Data Acquisition (Optional)
The required CSV files are already included under `Data/`.
- Source: curatedMetagenomicData (LeChatelierE_2013 study).
- To re-download from scratch, run `Data/curated_data.ipynb` in an R environment.

### 3. Running the Analysis
Open `research.ipynb` and run top to bottom.

#### Part A: Preprocessing & EDA
- MIPMLP pipeline (species-level aggregation + rare taxa filtering)
- Log transformation to handle skewness
- Data sparsity and class imbalance diagnostics

#### Part B: Statistical Analysis
- Mann-Whitney U tests + FDR correction (q < 0.1)
- Volcano plot for differential abundance
- Goldilocks test for protective taxa

#### Part C: Predictive Modeling
- Logistic Regression (L1) and Random Forest (SMOTE + GridSearch)
- Random Forest feature-importance analysis
- iMic CNN with Optuna tuning

#### Part D: Evaluation & Calibration
- AUC, Precision, Recall, F1
- ROC curves and confusion matrix
- Threshold calibration (0.3 vs 0.5)

### 4. Reproducibility
Random seeds are set in `research.ipynb` (NumPy, Python, PyTorch), and splits use fixed `random_state` values.

---

## Summary of Results (current notebook outputs)

**Tabular baselines (5-fold CV):**

| Model | AUC (mean) | Notes |
| :--- | :---: | :--- |
| Logistic Regression (L1) | ~0.70 | CV mean AUC from `research.ipynb` |
| Random Forest (SMOTE + GridSearch) | ~0.74 | CV mean AUC from `research.ipynb` |

**Hold-out test split (same split used for iMic):**

| Model | AUC | Precision | Recall | F1 | Threshold |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 0.70 | 0.75 | 0.73 | 0.74 | 0.5 |
| Random Forest | 0.70 | 0.76 | 0.58 | 0.66 | 0.5 |

**iMic CNN (hold-out test split):**

| Model | AUC | Precision | Recall | F1 | Threshold |
| :--- | :---: | :---: | :---: | :---: | :---: |
| iMic CNN | 0.80 | 0.94 | 0.52 | 0.67 | 0.3 |

Note: `research.ipynb` includes a consolidated hold-out results table for LR, RF, and iMic.

---

## Authors
- **Lior Ben Jashar**
- **Yarin Ifrah**
