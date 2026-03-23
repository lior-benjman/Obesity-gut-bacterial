import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd


OUT_PDF = Path("Final_Paper_Stage2.pdf")


METRICS_DF = pd.DataFrame(
    [
        ["Logistic Regression (hold-out, thr=0.5)", 0.700000, 0.679245, 0.750000, 0.727273, 0.738462],
        ["Random Forest (hold-out, thr=0.5)", 0.628788, 0.566038, 0.678571, 0.575758, 0.622951],
        ["iMic CNN (hold-out, thr=0.5)", 0.783333, 0.679245, 0.666667, 0.969697, 0.790123],
        ["iMic CNN (hold-out, thr=0.3)", 0.783333, 0.698113, 0.673469, 1.000000, 0.804878],
    ],
    columns=["Model", "AUC", "Accuracy", "Precision", "Recall", "F1"],
)

SAMPLE_COUNTS = {"Lean": 98, "Obese": 167}

TOP_TAXA_TEXT = [
    "Most significant taxon: Fretibacterium_fastidiosum (p = 1.20e-05)",
    "Second most significant taxon: Clostridium_sp_CAG_58 (p = 6.12e-05)",
    "Total significant taxa after FDR correction (q < 0.1): 5",
    "These statistical signals motivate the predictive stage by showing that the phenotype-linked microbiome structure is not random.",
]

CM = np.array([[4, 16], [0, 33]])


def add_wrapped(ax, x, y, text, width=105, size=10.5, lh=0.028, weight="normal"):
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
        else:
            lines.extend(textwrap.wrap(para, width=width))
    for line in lines:
        ax.text(x, y, line, fontsize=size, va="top", ha="left", fontweight=weight)
        y -= lh
    return y


def page_1(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    y = 0.95
    ax.text(0.05, y, "Gut Microbiome Signatures of Obesity", fontsize=20, fontweight="bold", va="top")
    y -= 0.035
    ax.text(0.05, y, "Statistical Testing, Classical ML, and Phylogenetic Deep Learning", fontsize=13, va="top")
    y -= 0.04
    ax.text(0.05, y, "Authors: Lior Ben Jashar, Yarin Ifrah", fontsize=11, va="top")
    y -= 0.05

    ax.text(0.05, y, "Abstract", fontsize=14, fontweight="bold", va="top")
    y -= 0.03
    abstract = (
        "Obesity is associated with substantial inter-individual variability in gut microbiome composition, "
        "but translating that variability into robust, clinically useful signals remains challenging because "
        "microbiome data are sparse, high-dimensional, and highly skewed. We analyzed the LeChatelier et al. cohort "
        "and framed the task as binary classification of Lean (BMI <= 25) vs Obese (BMI >= 30), while also identifying "
        "taxa associated with group differences.\n\n"
        "Our pipeline combines preprocessing with MIPMLP, non-parametric statistical testing with false-discovery-rate correction, "
        "and predictive modeling with Logistic Regression, Random Forest, and iMic-based CNN models. In this run, five taxa "
        "passed FDR < 0.1; the strongest signal was Fretibacterium_fastidiosum (p = 1.20e-05), followed by "
        "Clostridium_sp_CAG_58 (p = 6.12e-05). On hold-out evaluation, Logistic Regression achieved AUC 0.700 (F1 0.738), "
        "Random Forest achieved AUC 0.629 (F1 0.623), and iMic achieved AUC 0.783 with recall-oriented thresholding.\n\n"
        "Overall, the results support a reproducible end-to-end workflow and show that phylogenetic image representations "
        "can improve discrimination beyond tabular baselines in this dataset. We also highlight the operating-point "
        "trade-off between sensitivity and specificity for screening-oriented deployment. Model differences are reported "
        "descriptively because no formal significance test between models was completed in this submission."
    )
    # Abstract layout tightened to prevent right-edge clipping.
    add_wrapped(ax, 0.05, y, abstract, width=100, size=10.0, lh=0.0255)

    pdf.savefig(fig)
    plt.close(fig)


def page_2(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    y = 0.96
    ax.text(0.05, y, "1. Introduction", fontsize=14, fontweight="bold", va="top")
    y -= 0.03
    intro = (
        "The gut microbiome is increasingly linked to obesity and metabolic disease, but extracting stable signal is difficult: "
        "microbiome matrices include many zeros, compositional constraints, and correlated taxa. This project asks two connected questions: "
        "(1) which taxa are significantly associated with Lean vs Obese phenotypes, and (2) whether predictive models using microbiome "
        "features, including phylogenetic image encoding, improve obesity classification.\n\n"
        "We use a story-driven workflow: characterize the cohort, test statistical hypotheses, build interpretable tabular baselines, "
        "then evaluate a deep-learning model that preserves phylogenetic structure."
    )
    y = add_wrapped(ax, 0.05, y, intro)
    y -= 0.012
    ax.text(0.05, y, "2. Methods", fontsize=14, fontweight="bold", va="top")
    y -= 0.03
    methods = (
        f"Data source: LeChatelier cohort tables in this repository. After BMI filtering (Lean <= 25, Obese >= 30), the final cohort was n={SAMPLE_COUNTS['Lean'] + SAMPLE_COUNTS['Obese']} "
        f"(Lean={SAMPLE_COUNTS['Lean']}, Obese={SAMPLE_COUNTS['Obese']}).\n\n"
        "Preprocessing: MIPMLP taxonomy aggregation (species-level), relative normalization, rare taxa filtering, then global log transform "
        "(log10(X+1e-6)).\n\n"
        "Statistical analysis: per-taxon Mann-Whitney U tests with Benjamini-Hochberg FDR correction (q < 0.1).\n\n"
        "Models: L1-regularized Logistic Regression, Random Forest with scaler+SMOTE+grid-search, and iMic CNN optimized with Optuna.\n\n"
        "Evaluation: fixed shared hold-out split (80/20), fixed seeds, training-only tuning for the iMic validation step, "
        "and hold-out reporting shared across all primary models."
    )
    add_wrapped(ax, 0.05, y, methods)
    pdf.savefig(fig)
    plt.close(fig)


def page_3(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))
    gs = fig.add_gridspec(3, 1, height_ratios=[1.35, 1.35, 1.0], hspace=0.30)
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.axis("off")
    y = 0.98
    ax0.text(-0.05, y, "3. Results: Data Profile and Statistical Signals", fontsize=14, fontweight="bold", va="top")
    y -= 0.13
    for line in TOP_TAXA_TEXT:
        y = add_wrapped(ax0, -0.05, y, f"- {line}", width=95, size=10.5, lh=0.10)

    ax1 = fig.add_subplot(gs[1, 0])
    labels = list(SAMPLE_COUNTS.keys())
    values = [SAMPLE_COUNTS[k] for k in labels]
    bars = ax1.bar(labels, values, color=["#66c2a5", "#fc8d62"], edgecolor="black")
    ax1.set_title("Figure 1. Class Distribution in Filtered Cohort")
    ax1.set_ylabel("Number of Samples")
    for b, v in zip(bars, values):
        ax1.text(b.get_x() + b.get_width() / 2, v + 2, str(v), ha="center", va="bottom", fontsize=10)

    ax2 = fig.add_subplot(gs[2, 0])
    ax2.axis("off")
    caption = (
        "Interpretation: The cohort is imbalanced toward Obese samples. This supports using class-aware \ntraining choices"
        "(balanced logistic regression and SMOTE in RF), and explicit threshold analysis \nduring evaluation."
    )
    add_wrapped(ax2, 0.0, 0.95, caption, width=105, size=10.5, lh=0.12)
    pdf.savefig(fig)
    plt.close(fig)


def page_4(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.38, 1.3, 1.0], hspace=0.3)

    axh = fig.add_subplot(gs[0, 0])
    axh.axis("off")
    axh.text(0.0, 0.95, "3. Results: Predictive Modeling Performance", fontsize=14, fontweight="bold", va="top")

    axt = fig.add_subplot(gs[1, 0])
    axt.axis("off")
    table_df = METRICS_DF.copy()
    table_df[["AUC", "Accuracy", "Precision", "Recall", "F1"]] = table_df[
        ["AUC", "Accuracy", "Precision", "Recall", "F1"]
    ].round(3)
    col_widths = [0.48, 0.10, 0.10, 0.10, 0.10, 0.10]
    tbl = axt.table(
        cellText=table_df.fillna("-").values,
        colLabels=table_df.columns,
        loc="center",
        cellLoc="center",
        colWidths=col_widths,
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8.3)
    tbl.scale(1, 1.38)
    axt.set_title("Table 1. Hold-out Performance Summary (Latest Run)", fontsize=11)

    axb = fig.add_subplot(gs[2, 0])
    auc_df = METRICS_DF[["Model", "AUC"]].dropna().copy()
    wrapped_labels = [
        lbl.replace(" (hold-out, thr=0.5)", "\n(hold-out, thr=0.5)").replace(" (hold-out, thr=0.3)", "\n(hold-out, thr=0.3)")
        for lbl in auc_df["Model"]
    ]
    y_pos = np.arange(len(auc_df))
    axb.barh(y_pos, auc_df["AUC"], color=["#4C78A8", "#F58518", "#54A24B", "#B279A2"], height=0.55)
    axb.set_yticks(y_pos)
    axb.set_yticklabels(wrapped_labels, fontsize=7.5)
    axb.invert_yaxis()
    axb.set_xlim(0.55, 0.90)
    axb.set_xlabel("AUC", fontsize=9)
    axb.set_title("Figure 2. AUC Comparison Across Models", fontsize=10)
    axb.tick_params(axis="x", labelsize=8)
    for i, v in enumerate(auc_df["AUC"]):
        axb.text(v + 0.004, i, f"{v:.3f}", va="center", fontsize=8)
    pos = axb.get_position()
    axb.set_position([0.37, pos.y0, 0.56, pos.height * 0.95])

    pdf.savefig(fig)
    plt.close(fig)


def page_5(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.28, 1.2, 1.0], hspace=0.3)
    axh = fig.add_subplot(gs[0, 0])
    axh.axis("off")
    axh.text(0.0, 0.95, "3. Results: Operating-Point Calibration", fontsize=14, fontweight="bold", va="top")

    axcm = fig.add_subplot(gs[1, 0])
    im = axcm.imshow(CM, cmap="Greens")
    axcm.set_xticks([0, 1])
    axcm.set_xticklabels(["Pred Lean", "Pred Obese"])
    axcm.set_yticks([0, 1])
    axcm.set_yticklabels(["True Lean", "True Obese"])
    axcm.set_title("Figure 3. Confusion Matrix at iMic Threshold = 0.3")
    for (i, j), val in np.ndenumerate(CM):
        axcm.text(j, i, str(val), ha="center", va="center", fontsize=12, color="black")
    fig.colorbar(im, ax=axcm, fraction=0.046, pad=0.04)

    axt = fig.add_subplot(gs[2, 0])
    axt.axis("off")
    calibr_text = (
        "At threshold 0.3, iMic reaches recall = 1.00 for Obese cases with precision = 0.673 and accuracy = 0.698.\n"
        "The confusion matrix (n=53) shows TP=33, FN=0, TN=4, FP=16.\n\n"
        "Storytelling takeaway: lowering the threshold shifts the model toward sensitivity (screening behavior), "
        "reducing missed Obese cases while increasing false positives among Lean samples. The suitable threshold "
        "depends on downstream clinical cost."
    )
    add_wrapped(axt, -0.03, 0.95, calibr_text, width=92, size=10.0, lh=0.105)

    pdf.savefig(fig)
    plt.close(fig)


def page_6(pdf):
    fig = plt.figure(figsize=(8.27, 11.69))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    y = 0.96
    ax.text(0.05, y, "4. Discussion", fontsize=14, fontweight="bold", va="top")
    y -= 0.03
    discussion = (
        "This analysis follows a coherent path from biological question to deployable model behavior. Statistically, five taxa "
        "showed significant group differences after FDR control. Predictively, tabular models established a baseline (LR outperforming RF "
        "in this run), while iMic improved discrimination and demonstrated stronger sensitivity at tuned thresholds.\n\n"
        "The strongest practical signal is not a single metric but the shape of trade-offs: iMic can be operated as a high-sensitivity "
        "screening model when missing Obese cases is costly. The main methodological limitation is that no formal significance test was "
        "completed between model performances, so observed score differences should be interpreted descriptively."
    )
    y = add_wrapped(ax, 0.05, y, discussion, width=106)
    y -= 0.012

    ax.text(0.05, y, "5. Limitations", fontsize=14, fontweight="bold", va="top")
    y -= 0.03
    limits = (
        "- Single cohort; no external validation cohort in this submission.\n"
        "- Cross-sectional design supports association, not causality.\n"
        "- Performance may vary under distribution shift and prevalence changes."
    )
    y = add_wrapped(ax, 0.05, y, limits, width=106)
    y -= 0.012

    ax.text(0.05, y, "6. Conclusion", fontsize=14, fontweight="bold", va="top")
    y -= 0.03
    concl = (
        "The project demonstrates a reproducible, end-to-end obesity microbiome pipeline combining statistical rigor and predictive modeling. "
        "In the latest run, iMic models outperform tabular baselines on AUC and can be calibrated for screening-oriented recall. "
        "The resulting workflow is submission-ready and provides a solid base for external validation and prospective extension."
    )
    y = add_wrapped(ax, 0.05, y, concl, width=106)
    y -= 0.018

    ax.text(0.05, y, "References", fontsize=14, fontweight="bold", va="top")
    y -= 0.03
    refs = (
        "1. Le Chatelier E, et al. Richness of human gut microbiome correlates with metabolic markers. Nature. 2013.\n"
        "2. Course lecture materials: MIPMLP and iMic methodology.\n"
        "3. Reproducible implementation and outputs: research.ipynb."
    )
    add_wrapped(ax, 0.05, y, refs, width=106)

    pdf.savefig(fig)
    plt.close(fig)


def main():
    with PdfPages(OUT_PDF) as pdf:
        page_1(pdf)
        page_2(pdf)
        page_3(pdf)
        page_4(pdf)
        page_5(pdf)
        page_6(pdf)
    print(f"Regenerated {OUT_PDF}")


if __name__ == "__main__":
    main()
