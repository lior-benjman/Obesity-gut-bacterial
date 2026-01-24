# Gut Microbiome and Obesity: Deep Learning & Statistical Analysis

**Course:** Machine Learning and Statistics in Medical Applications  
**Final Project: Phase 2**

This repository contains the complete research pipeline for analyzing the relationship between gut bacterial taxa and obesity. It employs advanced statistical methods, tabular machine learning, and a novel deep learning approach (**iMic**) that converts microbiome data into phylogenetic images.

---

## 📌 Project Overview

**Research Question:** Which gut bacterial taxa are associated with obesity (BMI ≥ 30) vs. Lean status (BMI ≤ 25), and can deep learning on phylogenetic images outperform traditional tabular models in predicting obesity?

**Key Findings:**
1.  **Protective Signatures:** High abundance of specific commensal bacteria (e.g., *Fretibacterium fastidiosum*) is strongly associated with the Lean phenotype.
2.  **Model Performance:** The **iMic CNN model** achieved an **AUC of 0.80**, outperforming Logistic Regression (0.70) and Random Forest (0.74).
3.  **Clinical Optimization:** By calibrating the decision threshold from 0.5 to 0.3, we increased **Sensitivity (Recall) by 73%** (from 0.30 to 0.52) while maintaining high **Precision (0.94)**, making the model a viable screening tool.

---

## 📂 Repository Structure

```
├── Data/
│   ├── curated_data.ipynb            # R script for downloading raw data (curatedMetagenomicData)
│   ├── Raw_LeChatelier_metadata.csv  # Processed Metadata
│   └── Raw_LeChatelier_relative_abundance.csv # Processed Taxa Abundance
├── research_images/                  # Generated Phylogenetic Images (for iMic model)
├── logs/                             # TensorBoard training logs
├── checkpoints/                      # PyTorch Lightning model checkpoints
├── research.ipynb                    # MAIN ANALYSIS NOTEBOOK (Run this)
└── README.md                         # Project Documentation
```

---

## 🛠️ Reproduction Instructions

To fully reproduce the analysis presented in the final report, follow these steps.

### 1. Prerequisites & Environment
Ensure you have **Python 3.8+** installed. The project relies on the following key libraries:
*   `torch`, `pytorch-lightning` (Deep Learning)
*   `MIPMLP` (Microbiome Preprocessing & Image Generation)
*   `optuna` (Hyperparameter Optimization)
*   `scikit-learn`, `imbalanced-learn` (ML & Sampling)
*   `pandas`, `seaborn`, `matplotlib` (Data Manipulation & Plotting)

**Installation:**
```bash
pip install torch pytorch-lightning optuna scikit-learn pandas seaborn matplotlib imbalanced-learn mipmlp
```

### 2. Data Acquisition (Optional)
The necessary CSV files (`Raw_LeChatelier_*.csv`) are **already included** in the `Data/` folder.
*   *Source:* [curatedMetagenomicData](https://waldronlab.io/curatedMetagenomicData/) (LeChatelierE_2013 study).
*   *Re-download:* If you wish to re-download the data from scratch, you must run `Data/curated_data.ipynb` using an **R environment**.

### 3. Running the Analysis
Open **`research.ipynb`** in Jupyter Lab or VS Code. This single notebook executes the entire pipeline sequentially:

#### **Part A: Preprocessing & EDA**
*   **MIPMLP Pipeline:** Aggregates taxonomy to species level and filters rare bacteria (<1% prevalence).
*   **Transformation:** Applies Log-transformation to handle skewness.
*   **Goldilocks Test:** Verifies the hypothesis that "balance" (intermediate abundance) or high abundance of commensals is protective.

#### **Part B: Statistical Analysis**
*   **Differential Abundance:** Runs Mann-Whitney U tests.
*   **FDR Correction:** Applies Benjamini-Hochberg correction ($q < 0.1$) to identify 5 significant biomarkers.
*   **Visualization:** Generates the **Volcano Plot** showing enrichment in Lean vs. Obese groups.

#### **Part C: Predictive Modeling**
1.  **Baselines:** Trains Logistic Regression (L1-regularized) and Random Forest (with SMOTE and GridSearch).
2.  **iMic Deep Learning:**
    *   **Image Generation:** Converts tabular abundance data into 2D phylogenetic images (stored in `research_images/`).
    *   **Optimization:** Uses **Optuna** to find the best learning rate, dropout, and batch size for the CNN.
    *   **Training:** Trains the final CNN model using PyTorch Lightning.

#### **Part D: Evaluation & Calibration**
*   **Metrics:** Calculates AUC, Precision, Recall, and F1-Score.
*   **Threshold Tuning:** Demonstrates the fix for low recall by shifting the decision boundary to 0.3.
*   **Output:** Generates Confusion Matrices and ROC Curves.

---

## 📊 Summary of Results

| Model | AUC | Precision | Recall | F1-Score |
| :--- | :--- | :--- | :--- | :--- |
| **Logistic Regression (Baseline)** | 0.70 | - | - | - |
| **Random Forest (Optimized)** | 0.74 | - | - | - |
| **iMic CNN (Threshold 0.5)** | 0.80 | 1.00 | 0.30 | 0.47 |
| **iMic CNN (Threshold 0.3)** | **0.80** | **0.94** | **0.52** | **0.67** |

*The iMic model with threshold calibration provides the best balance for clinical screening.*

---

## 👥 Authors
*   **[Lior Ben Jashar]**
*   **[Yarin Ifrah]**
