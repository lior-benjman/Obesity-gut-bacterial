# Explicit Explanations for the Project and Oral Defense

This file is intentionally direct. It is meant to answer the questions that were unclear in the oral defense and to make the project defendable step by step.

## 1. The One-Sentence Story of the Project
We first test whether Lean and Obese participants differ statistically in their microbiome composition, and then we test whether the same microbiome signal is strong enough to support prediction on unseen samples.

That is the bridge between the two halves of the project.

## 2. Why the Project Is Not Two Unrelated Parts
The lecturer was correct that the project can look disconnected if it is presented badly.

The correct connection is:
1. **Statistical analysis** asks whether there is real phenotype-linked signal in the taxa.
2. **Predictive modeling** asks whether that signal generalizes to new individuals.
3. **Feature interpretation and threshold analysis** explain what the model is using and how it behaves.

So the statistics justify why classification is meaningful, and the classifier tests whether the biological signal has practical predictive value.

## 3. Stage-by-Stage Inputs and Outputs
### Stage A: Load and Define the Cohort
**Input:**
- `Data/Raw_LeChatelier_metadata.csv`
- `Data/Raw_LeChatelier_relative_abundance.csv`

**Process:**
- filter BMI into two groups only
- Lean: `BMI <= 25`
- Obese: `BMI >= 30`

**Output:**
- filtered metadata table
- filtered abundance table
- binary target labels

### Stage B: MIPMLP Preprocessing
**Input:**
- filtered abundance table

**Process:**
- taxonomy aggregation at species level
- relative normalization
- rare taxa filtering

**Output:**
- cleaned microbiome feature table with fewer noisy taxa

### Stage C: Log Transformation
**Input:**
- cleaned abundance table `X`

**Process:**
- compute `log10(X + 1e-6)`

**Output:**
- `X_log`, the main table used for modeling and many visualizations

### Stage D: Statistical Testing
**Input:**
- `X_log` or the processed abundance table
- Lean / Obese labels

**Process:**
- Mann-Whitney U test per taxon
- Benjamini-Hochberg FDR correction

**Output:**
- p-value and q-value per taxon
- ranked list of taxa associated with the phenotype

### Stage E: Tabular Models
**Input:**
- `X_log`
- train/test split labels

**Process:**
- fit Logistic Regression and Random Forest on training data
- evaluate on the same hold-out test split

**Output:**
- AUC, accuracy, precision, recall, F1, ROC curves

### Stage F: iMic
**Input:**
- microbiome table on the same cohort
- phylogenetic structure through `micro2matrix`

**Process:**
- convert each sample into a phylogeny-aware image
- tune CNN hyperparameters inside the training split
- fit final CNN and evaluate on the hold-out test split

**Output:**
- predicted probabilities for the test samples
- ROC curve, confusion matrix, threshold-based metrics

## 4. Why We Used a Log Transform
This is one of the most basic questions, so the answer must be precise.

We used `log10(X + 1e-6)` because raw microbiome abundances are highly right-skewed and contain many values close to zero.

The transform helps because:
1. very large values stop dominating the scale
2. the feature distribution becomes less skewed
3. zero abundances remain numerically valid because of the small offset

What we should **not** say:
- “we did it because everyone does it”
- “it just works better”

What we **should** say:
- “the raw abundance table is sparse and strongly skewed, so the transform stabilizes the numeric scale for both visualization and modeling”

## 5. Why We Used Mann-Whitney U Instead of a Parametric Test
We did not assume normality because the abundance distributions are sparse, skewed, and full of zeros.

So:
- a standard t-test would impose assumptions we do not trust here
- Mann-Whitney is safer for comparing two independent groups under these distributional conditions

## 6. Why FDR Correction Was Necessary
We tested hundreds of taxa.

Without multiple-testing correction, many small p-values would appear just by chance.

So the Benjamini-Hochberg correction controls the false discovery rate across the full taxon set.

What this means in plain language:
- a taxon is not convincing just because it has a low raw p-value
- it must survive the multiple-testing correction step

## 7. Train, Validation, and Test: Exact Roles
This was a weak point in the defense and must be answered cleanly.

- **Train set:** used to fit the model
- **Validation inside training:** used only for tuning choices such as hyperparameters
- **Test set:** used only once at the end for final evaluation

We must never describe a test-set finding as if it was used to build the model.

Good sentence for defense:
- “The test split is only for final reporting. Any design choice or tuning decision must come from training data, possibly with internal validation.”

## 8. What Was Found Where
This is also a question we need to answer without confusion.

- The **differential-abundance findings** are statistical associations on the cohort table.
- The **model metrics** come from the shared hold-out test split.
- The **threshold analysis** is also on the hold-out test split.

So if asked “was this found in train or test?”, the answer depends on the result type:
- taxon significance: association analysis on the processed cohort table
- model AUC / confusion matrix: final hold-out evaluation

## 9. What MIPMLP Contributes
MIPMLP is not just a black-box preprocessing step.

In this project, it helps by:
- aggregating taxa at the species level
- applying normalization consistent with microbiome data
- removing rare taxa that are unlikely to carry stable signal

Plain-language defense answer:
- “MIPMLP turns a noisy microbiome table into a cleaner feature space that is easier to analyze statistically and model predictively.”

## 10. What iMic Contributes
iMic is the bridge from tabular microbiome data to a structured image representation.

The key idea:
- taxa are arranged according to phylogenetic relations instead of arbitrary column order
- neighboring pixels represent biologically related bacteria
- a CNN can then exploit spatial structure that standard tabular models ignore

Good defense sentence:
- “Logistic Regression and Random Forest treat taxa as columns. iMic tries to preserve phylogenetic neighborhood structure so the model can learn patterns between related taxa.”

## 11. What “Sub-PCA” Means Here
If asked about “sub-PCA”, we should not pretend it was a custom theoretical contribution if it was not.

The safe answer is:
- if this term appears inside the package or generated artifact names, it refers to an internal dimensional or structural transformation within the image-construction pipeline, not to the central biological claim of our project
- our project-level claim does **not** depend on inventing a new PCA method
- our defendable contribution is the end-to-end logic: preprocessing, statistics, baselines, iMic, and hold-out evaluation

If the lecturer presses for package internals, the correct response is:
- “that is part of the implementation details of the course method; the project-level point is how the transformed representation is used and evaluated”

## 12. How to Talk About the Two Main Taxa
### Fretibacterium_fastidiosum
Defensible statement:
- “In our cohort, this taxon was significantly more abundant in Lean samples, so we interpret it as a Lean-associated microbial signal.”

Careful discussion-level interpretation:
- “A plausible hypothesis is that it may co-occur with dietary or metabolic patterns associated with satiety and lower adiposity, but our dataset does not prove a causal mechanism.”

### Clostridium_sp_CAG_58
Defensible statement:
- “In our cohort, this taxon was enriched in Obese samples, so we interpret it as an Obese-associated signal.”

Careful discussion-level interpretation:
- “A plausible hypothesis is that it reflects a metabolic environment different from the Lean group, possibly linked to carbohydrate-rich dietary patterns, but our analysis is associative rather than causal.”

What not to say as fact unless cited:
- “this bacterium makes people eat more carbs”
- “this bacterium causes obesity”

## 13. Why the Threshold Change Matters
At threshold `0.5`, iMic already detects most Obese cases.
At threshold `0.3`, recall becomes `1.00` on the hold-out set.

That means:
- we miss fewer Obese cases
- but we accept more false positives among Lean cases

So the threshold is not only a technical detail. It changes the clinical role of the model.

## 14. The Exact Limitation We Must Admit
The clean admission is:
- “We compared model scores on the same hold-out split, but we did not complete a formal statistical significance test between models. Therefore, we present the performance differences descriptively rather than as statistically proven superiority.”

This is much better than overclaiming.

## 15. Short Version for the Oral Defense
If we have only 30 seconds:
- “We first showed that the Lean and Obese groups differ statistically in specific taxa after FDR correction. Then we asked whether that same microbiome signal supports prediction on unseen samples. Logistic Regression gave a strong linear baseline, Random Forest was weaker in this run, and iMic gave the highest descriptive hold-out AUC while allowing a high-recall screening threshold. The project is therefore one connected story from biological signal to predictive usefulness.”
