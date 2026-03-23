# Gut Microbiome Signatures of Obesity:
## Statistical Screening, Tabular Modeling, and Phylogeny-Aware Deep Learning

**Authors:** Lior Ben Jashar, Yarin Ifrah

## Abstract
Obesity is associated with marked variation in gut microbiome composition, but microbiome measurements are sparse, high-dimensional, and strongly skewed, which makes both interpretation and prediction difficult. We analyzed the LeChatelier et al. cohort and framed the task as binary classification of Lean (BMI <= 25) versus Obese (BMI >= 30), while also testing which taxa differ significantly between the groups.

Our workflow was designed as one connected pipeline rather than two separate tasks. First, we characterized the data distribution and applied microbiome-oriented preprocessing with MIPMLP, relative normalization, rare-taxa filtering, and a global log transform. Second, we used Mann-Whitney U tests with Benjamini-Hochberg false-discovery-rate control to identify taxa associated with the phenotype. Third, we evaluated predictive models on the same shared hold-out split so that classical tabular baselines and iMic could be compared fairly. Five taxa passed `FDR < 0.1`; the strongest Lean-associated signal was **Fretibacterium_fastidiosum** (`p = 1.20e-05`), while **Clostridium_sp_CAG_58** was enriched in Obese samples (`p = 6.12e-05`). On the hold-out split, Logistic Regression achieved AUC `0.700` (`F1 = 0.738`), Random Forest achieved AUC `0.629` (`F1 = 0.623`), and iMic achieved AUC `0.783`. At threshold `0.3`, iMic reached recall `1.00` for Obese cases at the cost of more false positives among Lean samples.

These results show that the microbiome contains both interpretable statistical signals and predictive structure. The statistical findings help explain which taxa differ between groups, while the modeling section tests whether that signal is strong enough to support classification. The analysis remains associative rather than causal, and the model comparisons should be interpreted descriptively because no formal significance test between models was completed in the current submission.

## 1. Introduction
The gut microbiome is increasingly linked to obesity and metabolic disease, but extracting stable signal from microbiome tables is difficult because the data are sparse, compositional, high-dimensional, and strongly correlated across taxa. For that reason, a useful project in this domain must do more than report isolated p-values or isolated model scores. It must show how the biological question, the statistical tests, the preprocessing choices, and the predictive models all fit together.

This project asks two linked questions:
1. Which bacterial taxa differ significantly between Lean and Obese individuals?
2. Can those microbiome signals support prediction of obesity status, and does a phylogeny-aware image representation add value beyond standard tabular models?

The central narrative of the project is therefore:
`data challenges -> preprocessing -> statistical screening -> model design -> hold-out evaluation -> interpretation`.

This connection is important. The statistical section tells us whether meaningful group-level microbial differences exist at all. The modeling section then asks whether those same microbiome patterns are strong enough to generalize to unseen samples. In that sense, the statistical analysis establishes biological plausibility, and the predictive analysis establishes practical usefulness.

## 2. Methods
### 2.1 Data and Cohort Definition
- Source files: `Data/Raw_LeChatelier_metadata.csv`, `Data/Raw_LeChatelier_relative_abundance.csv`
- Cohort filter: Lean if `BMI <= 25`, Obese if `BMI >= 30`
- Final cohort size: `n = 265` (`Lean = 98`, `Obese = 167`)
- Target variable: binary obesity status derived from BMI thresholds

### 2.2 Data Characteristics and Challenges
The microbiome table is tabular, but it is not a simple independent-feature setting. Several challenges shape the analysis:
- many zeros because many taxa are absent or below detection in many samples
- strong right-skew in abundance values
- high dimensionality relative to cohort size
- dependence between taxa because microbial abundances are not independent biological entities
- moderate class imbalance toward the Obese group

These properties are the reason we did not move directly to modeling. We first applied preprocessing to stabilize the feature space and then performed non-parametric testing that does not assume Gaussian distributions.

### 2.3 Preprocessing
We used the course MIPMLP pipeline with `taxonomy_level = 7`, relative normalization, and rare-taxa filtering (`rare_bacteria_threshold = 0.01`). After preprocessing, the feature table contained 373 taxa.

We then applied a global transform:
`X_log = log10(X + 1e-6)`

This step serves three purposes:
1. it compresses extreme abundance values so that a small number of highly abundant taxa do not dominate the analysis
2. it makes the feature distribution less skewed and therefore easier for downstream models to handle
3. it keeps zeros numerically valid by adding a small constant before the logarithm

### 2.4 Statistical Analysis
We performed per-taxon Mann-Whitney U tests comparing Lean versus Obese samples. This test was chosen because the abundance distributions are sparse and non-Gaussian. To control for multiple testing across hundreds of taxa, we applied Benjamini-Hochberg false-discovery-rate correction and used `q < 0.1` as the significance threshold.

The purpose of this section was not only to list significant taxa. It was also to answer a gating question for the modeling section: does the microbiome contain detectable phenotype-linked signal at the individual taxon level?

### 2.5 Predictive Models
We evaluated three predictive approaches:
- **Logistic Regression**: L1-regularized, class-balanced baseline on log-transformed abundances
- **Random Forest**: scaler + SMOTE + grid search on the training partition
- **iMic CNN**: `micro2matrix` phylogenetic image conversion followed by a CNN optimized with Optuna

These models play different roles in the story:
- Logistic Regression asks whether a sparse linear signal is already sufficient.
- Random Forest asks whether non-linear interactions improve performance in the same tabular space.
- iMic asks whether preserving phylogenetic structure in an image-like representation helps the model use relationships between taxa that plain column-wise tabular models may ignore.

### 2.6 Split Logic and Evaluation
To keep comparisons interpretable, we used one shared `80/20` hold-out split for the final evaluation of Logistic Regression, Random Forest, and iMic.

The split logic is:
- **training split**: fit models and perform any training-only feature filtering or tuning
- **internal validation inside training**: choose iMic hyperparameters during Optuna tuning
- **hold-out test split**: final model reporting only

This point is critical: any effect reported on the test set must be described as a final evaluation result, not as a discovery used to design the model.

### 2.7 Metrics and Comparison Limits
We report AUC, accuracy, precision, recall, F1, ROC curves, and confusion matrices. These metrics are useful because obesity screening has asymmetric costs: missing Obese cases is different from producing additional false positives.

However, in the current submission we did **not** complete a formal statistical significance test between models on the shared test set. Therefore, model differences should be interpreted as descriptive performance differences rather than definitive proof that one model is statistically superior.

## 3. Results
### 3.1 Cohort Profile and Distributional Motivation
After BMI filtering, the cohort contained 98 Lean and 167 Obese samples. The abundance table remained sparse and skewed after filtering, which justified both the use of non-parametric statistics and the use of a log transform before modeling.

### 3.2 Differential Abundance Findings
Five taxa passed `FDR < 0.1`.

The two strongest signals were:
- **Fretibacterium_fastidiosum**: strongest significant association, higher in Lean samples (`p = 1.20e-05`)
- **Clostridium_sp_CAG_58**: second strongest significant association, enriched in Obese samples (`p = 6.12e-05`)

This section is the biological anchor of the project. It shows that the Lean and Obese groups are not only separable by black-box prediction scores; they also differ at the level of specific taxa.

### 3.3 How the Statistical Findings Inform the Models
The statistics and the models answer different questions, but they are connected.

- The Mann-Whitney + FDR section establishes that there is real phenotype-linked microbial structure in the data.
- The feature-importance and focused-taxon analyses show whether the same taxa that differ statistically are also informative predictively.
- The iMic model then tests whether embedding the taxa in a phylogeny-aware spatial representation captures signal beyond standard tabular baselines.

In other words, the statistical results motivate why classification is reasonable, and the predictive section tests whether that signal transfers to unseen data.

### 3.4 Hold-out Predictive Performance
All primary models were evaluated on the same hold-out split.

| Model | AUC | Accuracy | Precision | Recall | F1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression (`thr = 0.5`) | 0.700 | 0.679 | 0.750 | 0.727 | 0.738 |
| Random Forest (`thr = 0.5`) | 0.629 | 0.566 | 0.679 | 0.576 | 0.623 |
| iMic (`thr = 0.5`) | 0.783 | 0.679 | 0.667 | 0.970 | 0.790 |
| iMic (`thr = 0.3`) | 0.783 | 0.698 | 0.673 | 1.000 | 0.805 |

Interpretation:
- Logistic Regression is a strong tabular baseline, which suggests that the signal is not purely non-linear.
- Random Forest under this feature-space and split did not outperform the linear baseline.
- iMic produced the highest AUC in this run and, more importantly, was highly sensitive to Obese cases after threshold calibration.

Because no paired significance test between models was completed, we report these as observed differences rather than statistically confirmed superiority claims.

### 3.5 Operating-Point Interpretation
At threshold `0.3`, the iMic confusion matrix on the hold-out set (`n = 53`) is:
- `TN = 4`
- `FP = 16`
- `FN = 0`
- `TP = 33`

This operating point is intentionally sensitivity-oriented. It detects all Obese cases in the test set, but it does so by labeling many Lean samples as Obese. This does not make the model universally better; it makes it better suited to a screening-style use case where false negatives are more costly than false positives.

## 4. Discussion
### 4.1 Main Conclusions
The project supports three main conclusions.

1. The Lean and Obese groups differ at the microbiome level in a way that is statistically detectable after multiple-testing correction.
2. Those group-level differences are strong enough to support prediction on unseen samples.
3. The value of the predictive model depends not only on AUC, but also on the operating point chosen for the clinical goal.

### 4.2 Interpreting the Two Strongest Taxa
**Fretibacterium_fastidiosum** was more abundant in Lean participants. A cautious interpretation is that this taxon may be part of a microbial environment associated with a Lean phenotype in this cohort. One biologically plausible hypothesis is that taxa associated with protein-rich fermentation patterns may co-occur with dietary behaviors linked to satiety and lower adiposity. This interpretation should be treated as a hypothesis, not as causal proof from the present analysis.

**Clostridium_sp_CAG_58** was more abundant in Obese participants. A cautious interpretation is that this taxon may be part of a microbial profile associated with metabolic environments that differ from the Lean group. One plausible hypothesis is that carbohydrate-rich dietary patterns may support taxa enriched in the Obese cohort. Again, this is an interpretation layer added to the statistical result, not direct proof that the bacterium itself causes obesity, alters appetite, or drives host behavior.

The key distinction is important for the oral defense: the dataset supports **association**, while the mechanistic narrative remains **biologically plausible speculation** unless supported by external literature and experimental validation.

### 4.3 Why the Project Is One Story
The lecturer’s main criticism was that the project looked like two disconnected parts: hypothesis testing and classification. The correct framing is:
- statistics establish whether phenotype-linked microbiome differences exist
- feature interpretation shows which taxa carry signal
- modeling asks whether that signal generalizes to new samples
- threshold calibration translates the score into decision behavior

This is the linking logic of the project. Without the statistical section, the classifier would be less interpretable. Without the predictive section, the statistical findings would not answer whether the signal is practically usable.

### 4.4 Limitations
- single cohort with no external validation set
- cross-sectional data, so the analysis supports association rather than causation
- no completed formal significance test between model performances
- microbiome features are dependent and compositional, so standard ML baselines remain an approximation
- some exploratory model variants should be treated cautiously unless rerun and fully documented under cleaned split logic

### 4.5 Practical Value
Even with those limitations, the project demonstrates a defensible end-to-end workflow for microbiome data:
- diagnose the data distribution
- choose preprocessing that matches that distribution
- test hypotheses with multiple-testing correction
- compare baselines and structure-aware models on one hold-out split
- interpret predictions through clinically meaningful thresholds

## 5. Conclusion
This project should be defended as a connected microbiome-analysis pipeline rather than as a collection of tests. The statistical section shows that obesity-linked microbial differences exist in the cohort. The predictive section shows that these differences can support classification, with iMic providing the strongest descriptive hold-out AUC in the current run and especially strong recall after threshold calibration. The biological interpretation of specific taxa is promising but still associative, and formal significance testing between models remains a clear next step.

## References
1. Le Chatelier E, et al. *Richness of human gut microbiome correlates with metabolic markers*. Nature. 2013.
2. Course lecture materials on MIPMLP and iMic methodology.
3. Notebook implementation and outputs: `research.ipynb`.
