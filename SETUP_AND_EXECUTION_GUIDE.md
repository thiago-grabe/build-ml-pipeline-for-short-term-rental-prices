# Complete Setup and Execution Guide

This guide will walk you through setting up and running the NYC Airbnb ML Pipeline from the very beginning. This pipeline predicts short-term rental prices using a Random Forest model with MLflow for orchestration and Weights & Biases for experiment tracking.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Option A: GitHub Codespaces Setup (Recommended)](#option-a-github-codespaces-setup-recommended)
3. [Option B: Local Environment Setup](#option-b-local-environment-setup)
4. [Weights & Biases Configuration](#weights--biases-configuration)
5. [Running the Complete Pipeline](#running-the-complete-pipeline)
6. [Running Individual Pipeline Steps](#running-individual-pipeline-steps)
7. [Hyperparameter Optimization](#hyperparameter-optimization)
8. [Model Promotion and Testing](#model-promotion-and-testing)
9. [Training on New Data Samples](#training-on-new-data-samples)
10. [Troubleshooting](#troubleshooting)
11. [Pipeline Architecture Overview](#pipeline-architecture-overview)

---

## Prerequisites

Before you begin, ensure you have:

- A GitHub account
- A Weights & Biases account (free at [wandb.ai](https://wandb.ai))
- Basic familiarity with command-line operations

**Supported Operating Systems:**
- Ubuntu 22.04 or 24.04 (including WSL)
- macOS (recent versions)
- GitHub Codespaces (cloud-based, recommended)

**Required Python Version:** Python 3.12.7 (MLflow 2.18.0 compatibility requirement)

---

## Option A: GitHub Codespaces Setup (Recommended)

GitHub Codespaces provides a fully configured cloud development environment, eliminating local setup complexity.

### Step 1: Fork the Repository

1. Navigate to the repository on GitHub
2. Click the **Fork** button in the upper-right corner
3. This creates your own copy of the repository

### Step 2: Launch Codespaces

1. In your forked repository, click the green **Code** button
2. Select the **Codespaces** tab
3. Click **Create codespace on main**
4. Wait 2-3 minutes for the environment to build

The Codespace will automatically:
- Install Python 3.12.7
- Create the conda environment
- Install all dependencies from `environment.yml`

### Step 3: Activate the Environment

Once your Codespace loads, open a terminal and activate the conda environment:

```bash
conda activate nyc_airbnb_dev
```

**Note:** The environment should activate automatically, but if not, run the command above.

### Step 4: Verify Installation

```bash
# Check Python version (should be 3.12.7)
python --version

# Check MLflow installation
mlflow --version

# Check conda environment
conda env list
```

---

## Option B: Local Environment Setup

If you prefer to work locally instead of using Codespaces:

### Step 1: Clone the Repository

```bash
git clone https://github.com/[your-username]/build-ml-pipeline-for-short-term-rental-prices.git
cd build-ml-pipeline-for-short-term-rental-prices
```

### Step 2: Install Conda

If you don't have conda installed:

- **Linux/macOS:** Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- **Windows:** Use WSL2 with Ubuntu, then install Miniconda

### Step 3: Create the Conda Environment

```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate nyc_airbnb_dev
```

This will install:
- Python 3.12.7
- MLflow 2.18.0
- Weights & Biases 0.21.3
- Hydra 1.3.2
- All other dependencies

### Step 4: Verify Installation

```bash
# Check Python version
python --version

# Check MLflow
mlflow --version

# List installed packages
conda list
```

---

## Weights & Biases Configuration

Weights & Biases (W&B) is used for experiment tracking and artifact management.

### Step 1: Get Your API Key

1. Go to [https://wandb.ai/authorize](https://wandb.ai/authorize)
2. Click the **+** icon to copy your API key to clipboard

### Step 2: Login to W&B

```bash
wandb login [paste-your-api-key-here]
```

You should see a message like:
```
wandb: Appending key for api.wandb.ai to your netrc file: /home/[username]/.netrc
```

### Step 3: Verify Login

```bash
wandb verify
```

If successful, you'll see: `API key is valid!`

---

## Running the Complete Pipeline

The complete pipeline consists of 5 main steps:
1. **download** - Fetches raw data sample
2. **basic_cleaning** - Removes outliers and handles dates
3. **data_check** - Validates data quality with pytest
4. **data_split** - Segregates test set
5. **train_random_forest** - Trains the model

### First Run: Create Reference Dataset

For the first run, execute only the first 3 steps to create a reference dataset for data validation:

```bash
mlflow run . -P steps=download,basic_cleaning
```

**What happens:**
- Downloads `sample1.csv` from the data source
- Creates artifact `sample.csv` in W&B
- Cleans the data (removes price outliers, converts dates)
- Creates artifact `clean_sample.csv` in W&B

### Tag the Reference Dataset

Before running data_check, you need to tag the cleaned data as a reference:

1. Open your browser and go to [wandb.ai](https://wandb.ai)
2. Navigate to your project: **nyc_airbnb**
3. Click on the **Artifacts** tab
4. Find **clean_sample** artifact type
5. Click on the version with the **latest** tag
6. In the **Aliases** section on the right, click the **+** button
7. Add the tag: **reference**

![Add reference tag](images/wandb-tag-data-test.png)

### Run the Complete Pipeline

Now you can run all steps:

```bash
mlflow run .
```

**Expected Duration:** 10-15 minutes (depending on your machine/Codespace)

**What happens:**
1. Downloads data → `sample.csv`
2. Cleans data → `clean_sample.csv`
3. Validates data quality (pytest tests)
4. Splits data → `trainval_data.csv` + `test_data.csv`
5. Trains Random Forest → `random_forest_export` (model artifact)

**Monitor Progress:**
- The terminal will show detailed logs for each step
- Visit W&B dashboard to see real-time experiment tracking
- Check W&B Artifacts tab to see data and model artifacts

### Verify Success

After completion, check W&B:

1. Go to your **nyc_airbnb** project on W&B
2. **Runs** tab: You should see runs for each pipeline step
3. **Artifacts** tab: You should see:
   - `sample.csv` (raw_data)
   - `clean_sample.csv` (clean_sample)
   - `trainval_data.csv` and `test_data.csv`
   - `random_forest_export` (model_export)

---

## Running Individual Pipeline Steps

During development or debugging, you can run specific steps:

### Single Step

```bash
# Run only the download step
mlflow run . -P steps=download

# Run only data cleaning
mlflow run . -P steps=basic_cleaning

# Run only data validation
mlflow run . -P steps=data_check

# Run only model training
mlflow run . -P steps=train_random_forest
```

### Multiple Steps

```bash
# Run download and cleaning
mlflow run . -P steps=download,basic_cleaning

# Run data check and split
mlflow run . -P steps=data_check,data_split

# Skip download (use cached data)
mlflow run . -P steps=basic_cleaning,data_check,data_split,train_random_forest
```

### Override Configuration Parameters

Use Hydra syntax to override parameters from `config.yaml`:

```bash
# Change price range
mlflow run . \
  -P steps=basic_cleaning \
  -P hydra_options="etl.min_price=20 etl.max_price=300"

# Change Random Forest parameters
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.random_forest.n_estimators=200 modeling.random_forest.max_depth=20"

# Change test/validation split sizes
mlflow run . \
  -P steps=data_split \
  -P hydra_options="modeling.test_size=0.3 modeling.val_size=0.15"
```

---

## Hyperparameter Optimization

Use Hydra's multi-run feature to explore different hyperparameter combinations:

### Example: Grid Search

```bash
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5 -m"
```

The `-m` flag enables multi-run mode. This will create:
- 3 × 3 = **9 training runs** with different parameter combinations

### Parameters to Tune

Based on `config.yaml`, you can tune:

**NLP Feature:**
- `modeling.max_tfidf_features`: Number of words for TF-IDF (e.g., 5, 10, 15, 30)

**Random Forest Parameters:**
- `modeling.random_forest.n_estimators`: Number of trees (e.g., 50, 100, 200)
- `modeling.random_forest.max_depth`: Maximum tree depth (e.g., 10, 15, 20, 25)
- `modeling.random_forest.min_samples_split`: Minimum samples to split (e.g., 2, 4, 8)
- `modeling.random_forest.min_samples_leaf`: Minimum samples in leaf (e.g., 1, 3, 5)
- `modeling.random_forest.max_features`: Features per split (e.g., 0.1, 0.33, 0.5, 0.75, 1.0)

### Example: Comprehensive Search

```bash
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.max_tfidf_features=10,15,30 \
                     modeling.random_forest.n_estimators=100,200 \
                     modeling.random_forest.max_depth=15,20 \
                     modeling.random_forest.max_features=0.33,0.5,0.75 -m"
```

This creates: 3 × 2 × 2 × 3 = **36 runs**

### Find the Best Model

1. Go to W&B project dashboard
2. Switch to **Table** view (second icon on left)
3. Click **Columns** → **Hide all**
4. Select: **ID**, **Job Type**, **mae**, **r2**, and hyperparameters
5. Click on **mae** column → **Sort ascending** (best at top)
6. The top row is your best model

---

## Model Promotion and Testing

### Step 1: Promote Model to Production

After finding the best model:

1. Go to W&B → **Artifacts** tab
2. Find the **model_export** artifact from your best run
3. Click on the artifact version
4. In the **Aliases** section, click **+**
5. Add the tag: **prod**

This marks the model as production-ready.

### Step 2: Test Production Model

The `test_regression_model` step evaluates the production model on the held-out test set:

```bash
mlflow run . -P steps=test_regression_model
```

**Important Notes:**
- This step is **NOT** run by default in the pipeline
- It requires a model tagged with `prod` to exist
- It uses `test_data.csv:latest` (untouched during training)

**What it does:**
- Loads the model tagged `prod`
- Loads the test dataset
- Computes MAE and R² on test data
- Logs results to W&B

### Step 3: Update Configuration

Copy the best hyperparameters to `config.yaml`:

```yaml
modeling:
  max_tfidf_features: 15  # Your best value
  random_forest:
    n_estimators: 200     # Your best value
    max_depth: 20         # Your best value
    max_features: 0.5     # Your best value
    # ... other parameters
```

This makes these values the default for future runs.

---

## Training on New Data Samples

The pipeline is designed for weekly retraining with new data samples.

### Step 1: Create a GitHub Release

1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Tag: `1.0.0`
4. Title: `Version 1.0.0`
5. Description: Brief summary of the release
6. Click **Publish release**

### Step 2: Run Pipeline on New Data

Train on `sample2.csv` (a new data batch):

```bash
mlflow run https://github.com/[your-username]/build-ml-pipeline-for-short-term-rental-prices.git \
  -v 1.0.0 \
  -P hydra_options="etl.sample='sample2.csv'"
```

Replace `[your-username]` with your GitHub username.

**What happens:**
- MLflow clones your repository at version `1.0.0`
- Downloads `sample2.csv` instead of `sample1.csv`
- Runs the complete pipeline
- Compares new data distribution to reference dataset

### Step 3: Handle Data Validation Failures

If `test_proper_boundaries` fails (data outside NYC coordinates):

1. Add geographic filtering to `src/basic_cleaning/run.py` before saving CSV:

```python
# Filter to NYC boundaries
idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
df = df[idx].copy()
```

2. Commit and push changes
3. Create a new release: `1.0.1`
4. Re-run with `-v 1.0.1`

---

## Troubleshooting

### Issue: Corrupted MLflow Conda Environments

**Symptoms:**
- Pipeline fails with conda environment errors
- Dependency resolution issues

**Solution:**

List all MLflow environments:
```bash
conda info --envs | grep mlflow | cut -f1 -d" "
```

Remove all MLflow environments (use with caution):
```bash
for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda uninstall --name $e --all -y; done
```

Then re-run the pipeline.

### Issue: W&B Artifact Version Error

**Error message:**
```
Attempted to fetch artifact without alias (e.g. "<artifact_name>:v3" or "<artifact_name>:latest")
```

**Cause:** Missing version tag when referencing artifacts

**Solution:** Always include `:latest`, `:reference`, or `:prod` tag:
- ✅ `sample.csv:latest`
- ❌ `sample.csv`

### Issue: pytest Fails in data_check Step

**Possible Causes:**
1. Reference dataset not tagged in W&B
2. Data distribution has changed significantly
3. Price range violations

**Solutions:**
1. Ensure `clean_sample.csv:reference` exists in W&B
2. Check `kl_threshold` in `config.yaml` (default: 0.2)
3. Verify `min_price` and `max_price` in config match data cleaning step

### Issue: Python Version Mismatch

**Error:** MLflow fails to create conda environments

**Solution:**
Ensure all `conda.yml` files specify Python 3.12.7:

```yaml
dependencies:
  - python=3.12.7
  # ...
```

Check and update:
- `environment.yml`
- `src/basic_cleaning/conda.yml`
- `src/data_check/conda.yml`
- `src/train_random_forest/conda.yml`

### Issue: Long Pipeline Execution Time

**Normal Duration:** 10-15 minutes for complete pipeline

**If slower:**
1. Check internet connection (downloads artifacts from W&B)
2. Reduce Random Forest `n_estimators` for testing
3. Use fewer hyperparameter combinations

---

## Pipeline Architecture Overview

### Pipeline Steps

```
download
   ↓
basic_cleaning
   ↓
data_check
   ↓
data_split
   ↓
train_random_forest
   ↓
test_regression_model (manual)
```

### Artifact Flow

```
sample.csv (raw_data)
   ↓
clean_sample.csv (clean_sample)
   ↓
trainval_data.csv + test_data.csv
   ↓
random_forest_export (model_export)
```

### Configuration System

- **Framework:** Hydra
- **Config file:** `config.yaml` in project root
- **Access:** `config["section"]["parameter"]` in `main.py`
- **Override:** Use `-P hydra_options="key=value"`

### Feature Engineering

The Random Forest pipeline includes:

1. **Ordinal Encoding:** `room_type` (ordered categorical)
2. **One-Hot Encoding:** `neighbourhood_group` (with imputation)
3. **Zero Imputation:** Numerical features
4. **Date Feature:** Days since last review
5. **NLP Feature:** TF-IDF on listing name (configurable max features)

### Key Files

- `main.py`: Pipeline orchestration
- `config.yaml`: All parameters
- `environment.yml`: Main conda environment
- `src/basic_cleaning/`: Data cleaning component
- `src/data_check/`: pytest-based validation
- `src/train_random_forest/`: Model training with sklearn
- `components/`: Pre-built reusable components

---

## Next Steps

1. **Explore W&B Dashboard:**
   - View experiment runs
   - Compare hyperparameters
   - Analyze feature importance plots
   - Visualize pipeline DAG (Directed Acyclic Graph)

2. **Experiment with Parameters:**
   - Try different price ranges
   - Adjust train/test split ratios
   - Explore Random Forest hyperparameters

3. **Advanced Topics:**
   - Implement additional feature engineering
   - Add more data validation tests
   - Integrate additional data sources
   - Deploy model to production API

---

## Additional Resources

- **MLflow Documentation:** [https://mlflow.org/docs/latest/index.html](https://mlflow.org/docs/latest/index.html)
- **Weights & Biases Docs:** [https://docs.wandb.ai/](https://docs.wandb.ai/)
- **Hydra Documentation:** [https://hydra.cc/docs/intro/](https://hydra.cc/docs/intro/)
- **Project README:** See `README.md` for detailed step-by-step tutorial

---

## Summary: Quick Command Reference

```bash
# Setup
conda activate nyc_airbnb_dev
wandb login [your-api-key]

# First-time setup: Create reference dataset
mlflow run . -P steps=download,basic_cleaning
# Then tag clean_sample.csv as 'reference' in W&B

# Run complete pipeline
mlflow run .

# Run specific steps
mlflow run . -P steps=download,basic_cleaning

# Override parameters
mlflow run . -P hydra_options="etl.min_price=20"

# Hyperparameter tuning
mlflow run . -P steps=train_random_forest \
  -P hydra_options="modeling.max_tfidf_features=10,15,30 \
                     modeling.random_forest.max_features=0.33,0.5 -m"

# Test production model (after tagging as 'prod')
mlflow run . -P steps=test_regression_model

# Train on new data from release
mlflow run https://github.com/[username]/[repo].git \
  -v 1.0.0 \
  -P hydra_options="etl.sample='sample2.csv'"
```

---

**Congratulations!** You now have a fully functional ML pipeline for short-term rental price prediction. The pipeline is reproducible, version-controlled, and ready for weekly retraining with new data.
