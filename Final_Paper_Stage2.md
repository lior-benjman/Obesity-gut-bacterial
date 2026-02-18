# Gut Microbiome Signatures of Obesity:
## Statistical Testing, Classical ML, and Phylogenetic Deep Learning

**Authors:** Lior Ben Jashar, Yarin Ifrah

## Abstract
Obesity is associated with substantial inter-individual variability in gut microbiome composition, but translating that variability into robust, clinically useful signals remains challenging because microbiome data are sparse, high-dimensional, and highly skewed. We analyzed the LeChatelier et al. cohort and framed the task as binary classification of Lean (BMI <= 25) vs Obese (BMI >= 30), while also identifying taxa associated with group differences.

Our pipeline combines preprocessing with MIPMLP, non-parametric statistical testing with false-discovery-rate correction, and predictive modeling with Logistic Regression, Random Forest, and iMic-based CNN models. In this run, five taxa passed FDR < 0.1; the strongest signal was **Fretibacterium_fastidiosum** (p = 1.20e-05), followed by **Clostridium_sp_CAG_58** (p = 6.12e-05). On hold-out evaluation, Logistic Regression achieved AUC 0.700 (F1 0.738), Random Forest achieved AUC 0.629 (F1 0.623), and iMic achieved AUC 0.783 with improved recall at lower thresholding. A leakage-safe iMic variant using train-derived top-5 RF taxa reached AUC 0.86.

Overall, the results support a reproducible end-to-end workflow and show that phylogenetic image representations can improve discrimination beyond tabular baselines in this dataset. We also highlight the operating-point trade-off between sensitivity and specificity for screening-oriented deployment.

## 1. Introduction
The gut microbiome is increasingly linked to obesity and metabolic disease, but signal extraction is difficult because microbiome matrices include many zeros, compositional effects, and correlated taxa. A practical modeling pipeline must therefore do three things well: (1) preserve biological structure, (2) control statistical false positives, and (3) evaluate predictive performance under realistic split logic.

This project asks two connected questions:
1. Which taxa are significantly associated with Lean vs Obese phenotypes?
2. Can predictive models on microbiome features (including phylogenetic image encoding) distinguish obesity status better than tabular baselines?

We emphasize a story-driven workflow: characterize the data, test hypotheses, build interpretable baselines, and then test whether structured deep learning adds incremental value.

## 2. Methods
### 2.1 Data and Cohort Definition
- Source files: `Data/Raw_LeChatelier_metadata.csv`, `Data/Raw_LeChatelier_relative_abundance.csv`
- Cohort filter: Lean if BMI <= 25, Obese if BMI >= 30
- Final sample size: **n = 265** (Obese = 167, Lean = 98)

### 2.2 Preprocessing
- Taxonomic preprocessing with **MIPMLP** (`taxonomy_level=7`, relative normalization, rare taxa threshold 0.01)
- Global transform: `log10(X + 1e-6)` for skew mitigation and numeric stability

### 2.3 Statistical Analysis
- Per-taxon group comparison via Mann-Whitney U test
- Multiple-testing control with Benjamini-Hochberg FDR
- Significance criterion: `q < 0.1`

### 2.4 Predictive Models
- **Logistic Regression**: L1-regularized, class-balanced baseline
- **Random Forest**: scaler + SMOTE + RF grid search
- **iMic CNN**: phylogenetic image conversion (`micro2matrix`) + Optuna hyperparameter search

### 2.5 Evaluation Design
- Shared hold-out split for cross-family comparison (80/20)
- Fixed seeds for reproducibility
- Additional leakage-safe variant:
  - Feature selection and RF importance computed on training data only
  - Top-5 train-derived taxa used for iMic image generation

### 2.6 Metrics
- AUC, accuracy, precision, recall, F1
- Confusion matrix and threshold analysis for clinical operating-point interpretation

## 3. Results
### 3.1 Data Profile and Significant Taxa
- Significant taxa after correction: **5** (`FDR < 0.1`)
- Most significant taxon: **Fretibacterium_fastidiosum** (`p = 1.20e-05`)
- Second strongest: **Clostridium_sp_CAG_58** (`p = 6.12e-05`)

Group-level abundance snapshots (from notebook outputs) indicate overlapping dominant taxa, but with measurable shifts in rank and abundance between Lean and Obese groups.

### 3.2 Classical Model Performance
Hold-out metrics:
- Logistic Regression (thr=0.5): AUC **0.700**, F1 **0.738**
- Random Forest (thr=0.5): AUC **0.629**, F1 **0.623**

Interpretation: LR is a strong and stable tabular baseline here; RF under this feature-space and split is less competitive.

### 3.3 iMic Deep Learning Performance
- iMic hold-out (thr=0.5): AUC **0.783**, recall **0.970**, F1 **0.790**
- iMic hold-out (thr=0.3): AUC **0.783**, recall **1.000**, F1 **0.805**
- Leakage-safe top-5 iMic variant: AUC **0.86**

Thresholding effects are clinically relevant:
- Lowering threshold from 0.5 to 0.3 increases obesity recall to 1.0
- This comes with reduced Lean specificity (more false positives)

Confusion matrix at thr=0.3 (`n=53`):
- Lean correctly identified: 4
- Lean flagged as Obese: 16
- Obese missed: 0
- Obese correctly identified: 33

This operating point is sensitivity-oriented and suitable for screening contexts where missing obese cases is costly.

## 4. Discussion
### 4.1 Main Takeaways
The analysis supports three practical conclusions:
1. A small set of taxa carries significant obesity-related signal after FDR correction.
2. Phylogenetic image modeling (iMic) can outperform tabular baselines on this cohort.
3. Model thresholding changes the clinical role of the model (screening vs confirmatory behavior).

### 4.2 Why the Story Matters
A microbiome project can easily degrade into disconnected tests. Here, the progression from cohort definition -> preprocessing -> hypothesis testing -> baseline models -> deep learning -> calibration creates a coherent chain from biological question to decision-relevant output.

### 4.3 Limitations
- Single cohort and no external validation cohort in this submission
- Cross-sectional design (association, not causality)
- Threshold-specific performance can vary across populations

### 4.4 Practical Implications
The pipeline is reproducible and can be extended to prospective cohorts. For translational use, we recommend external validation and calibration under deployment prevalence before any clinical decision support integration.

## 5. Conclusion
This project demonstrates that obesity-associated microbiome signatures can be captured through a reproducible hybrid workflow combining non-parametric statistics, classical ML, and phylogeny-aware deep learning. In the latest run, iMic delivered stronger discrimination than tabular baselines, and threshold calibration provided a clinically interpretable sensitivity/specificity trade-off. The final outcome is a complete, reproducible analysis narrative suitable for Stage-2 project submission.

## References
1. Le Chatelier E, et al. Richness of human gut microbiome correlates with metabolic markers. *Nature*. 2013.
2. Course lecture materials on MIPMLP/iMic methodology.
3. Notebook implementation and outputs: `research.ipynb`.
