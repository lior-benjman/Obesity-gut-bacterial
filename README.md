# Obesity-gut-bacterial
Data science project in ML and medical applications

First step - Research question branstorming.
we wanted to explore gut bacteria and it's connection to the obesity / type 2 diabetes..

Our Final Research Question: Which gut bacterial taxa are associated with obesity (BMI ≥ 30 vs BMI ≤ 25), and how well can gut microbiome composition predict obesity status?

Data source - https://waldronlab.io/curatedMetagenomicData/
The dataset was obtained from the *LeChatelierE_2013* study.
Initial data acquisition was performed using an R script (see `Data/curated_data.ipynb`) to export raw metadata and relative abundance.

Files:
- `Data/Raw_LeChatelier_metadata.csv`: Patient metadata including BMI.
- `Data/Raw_LeChatelier_relative_abundance.csv`: Taxa relative abundance (Samples × Taxa).

### Analysis Workflow
1. **Data Preprocessing**: Using the **MIPMLP Pipeline** (Microbiome Preprocessing and Machine Learning Pipeline) for taxonomy aggregation, filtering (1% threshold), and relative normalization.
2. **Exploratory Analysis**: Visualizing data challenges like sparsity, class imbalance, and skewness.
3. **Statistical Association**: Performing Mann-Whitney U tests with Benjamini-Hochberg FDR correction to identify taxa significantly associated with obesity.
4. **Predictive Modeling**: Training an L1-regularized Logistic Regression model to predict obesity status from microbiome composition, evaluated via cross-validation (ROC-AUC).

### Key Results
The analysis identifies specific gut bacterial taxa that are significantly enriched or depleted in obese individuals and evaluates the overall predictive power of the gut microbiome for obesity.

---
Successfully processed the datasets and conducted the full analysis in `Obesity_bacteria.ipynb`.