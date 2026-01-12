# Gut Microbiome and Obesity: Predictive Modeling & Statistical Analysis

This project explores the relationship between gut bacterial taxa and obesity using advanced statistical methods and deep learning.

## 🔬 Research Question
**Which gut bacterial taxa are associated with obesity (BMI ≥ 30 vs BMI ≤ 25), and how well can gut microbiome composition predict obesity status?**

## 📊 Data Source
The dataset was obtained from the [curatedMetagenomicData](https://waldronlab.io/curatedMetagenomicData/) repository, specifically the **LeChatelierE_2013** study.
- Initial data acquisition was performed using an R script (see `Data/curated_data.ipynb`).
- **Data Files:**
    - `Data/Raw_LeChatelier_metadata.csv`: Patient metadata including BMI.
    - `Data/Raw_LeChatelier_relative_abundance.csv`: Taxa relative abundance (Samples × Taxa).

## 🛠️ Installation & Requirements
To reproduce this analysis, ensure you have the following installed:
- Python 3.8+
- PyTorch & PyTorch Lightning
- MIPMLP (Microbiome Preprocessing and Machine Learning Pipeline)
- Optuna, Scikit-learn, Pandas, Seaborn, Matplotlib

```bash
pip install torch pytorch-lightning optuna scikit-learn pandas seaborn matplotlib MIPMLP
```

## 🚀 Analysis Workflow (research.ipynb)
1. **MIPMLP Preprocessing**: Taxonomy aggregation at the species level, noise filtering (1% threshold), and relative normalization.
2. **Exploratory Data Analysis (EDA)**: Visualizing sparsity, class imbalance, and log-transformed distributions.
3. **Statistical Association**: Mann-Whitney U tests with FDR (Benjamini-Hochberg) correction to identify biomarkers.
4. **Predictive Modeling**:
    - **Baselines**: L1-Logistic Regression and Random Forest.
    - **Advanced**: **iMic (Deep Learning)** - Converting microbiome data into phylogenetic images and training an Optuna-optimized Convolutional Neural Network (CNN).
5. **Detailed Evaluation**: Clinical metrics (Precision, Recall, F1-Score) and Stability Checks (Loss Curves).

## 📈 Key Results
- Identified **5 significant bacterial taxa** associated with obesity.
- The **iMic CNN model** achieved a superior predictive power with an **AUC of 0.78**, significantly outperforming tabular baseline models.
- High abundance of specific commensal bacteria was found to be a protective factor for the Lean phenotype.

## 📂 Repository Structure
- `research.ipynb`: Main analysis notebook.
- `Data/`: Raw datasets and curation script.
- `research_images/`: Generated phylogenetic images for the iMic model.
- `checkpoints/`: Saved model checkpoints.
- `logs/`: Training logs for stability checks.

---
*Developed as part of the Machine Learning and Statistics in Medical Applications Course.*
