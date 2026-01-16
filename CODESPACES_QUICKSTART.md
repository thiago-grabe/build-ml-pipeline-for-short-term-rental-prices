# GitHub Codespaces Quick Start Guide

## First Time Setup (5 minutes)

### 1. Create Codespace

1. Go to the repository on GitHub
2. Click the green **Code** button
3. Select **Codespaces** tab
4. Click **Create codespace on main**

⏱️ First build takes ~3 minutes (subsequent starts: ~30 seconds)

### 2. Add Your W&B API Key

1. Go to https://wandb.ai/authorize
2. Copy your **v1 API key**
   - New keys have format: `wandb_v1_...` (86 characters)
   - Legacy 40-character keys are being phased out
3. In GitHub, go to Settings → Codespaces → Secrets
4. Click **New secret**:
   - Name: `WANDB_API_KEY`
   - Value: [paste your full v1 API key]
   - Repository access: Select this repo
5. **Rebuild codespace**: Cmd+Shift+P → "Codespaces: Rebuild Container"

**Note:** This repository uses wandb 0.24.0, which supports the new secure v1 API key format.

### 3. Verify Setup

Open terminal and run:
```bash
conda activate nyc_airbnb_dev
python --version  # Should show Python 3.12.7
wandb whoami      # Should show your username
```

## Running the Pipeline

**⚠️ IMPORTANT:** Before running the pipeline, you must complete the student implementation tasks below!

### Pre-Built Steps (Ready to Run)
```bash
# Download data (works immediately)
mlflow run . -P steps=download
```

### Steps Requiring Implementation

**❌ basic_cleaning** - Directory doesn't exist yet
```bash
# First create with cookiecutter:
cookiecutter cookie-mlflow-step -o src
# Then implement run.py and fill in main.py parameters
```

**⚠️ data_check** - Missing 2 test functions
```bash
# Implement test_row_count and test_price_range first
mlflow run . -P steps=data_check
```

**⚠️ train_random_forest** - Has 7 placeholder sections
```bash
# Fill in all "# YOUR CODE HERE" sections first
mlflow run . -P steps=train_random_forest
```

### Full Pipeline (After Implementation)
```bash
# Only works after all components implemented
mlflow run .
```

### Hyperparameter Tuning
```bash
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.5,1.0 -m"
```

## Jupyter Lab (EDA)

```bash
mlflow run src/eda
```

When Jupyter opens:
1. Create new notebook: Python 3
2. Run EDA code from README.md

**IMPORTANT**: When done:
- File → Close and Halt
- Click "Quit" in top-right
- **DO NOT** use Ctrl+C (corrupts environment)

## Viewing W&B Results

1. Go to https://wandb.ai
2. Select project: `nyc_airbnb`
3. View runs, artifacts, and metrics

## Common Issues

### "WANDB_API_KEY not set"
- Add secret in GitHub Settings → Codespaces → Secrets
- Rebuild container

### "Conda environment not found"
- Run: `conda activate nyc_airbnb_dev`
- Check: `conda info --envs`

### Disk Space Full
- Run cleanup task: Cmd+Shift+P → "Tasks: Run Task" → "Cleanup MLflow Environments"

### Slow Pipeline Execution
- First run creates conda environments (5+ minutes)
- Subsequent runs reuse environments (~30 seconds)

## Stopping Your Codespace

Codespaces auto-stop after 30 minutes of inactivity (free tier).

To manually stop:
1. Click "Codespaces" at bottom-left of VS Code
2. Select "Stop Current Codespace"

**Free Tier**: 60 core-hours/month (4-core = 15 hours)
**With Education**: 180+ core-hours/month

## Student Implementation Tasks

**⚠️ THIS IS A STUDENT TEMPLATE ⚠️**

This project includes TODO sections for you to implement. The pipeline **will not run** until you complete these tasks.

### Task 1: Create basic_cleaning Component

**Status:** ❌ Directory missing

**Steps:**
```bash
# 1. Create component with cookiecutter
cookiecutter cookie-mlflow-step -o src

# When prompted, enter:
# step_name: basic_cleaning
# script_name: run.py
# parameters: input_artifact,output_artifact,output_type,output_description,min_price,max_price
```

**Then implement** `src/basic_cleaning/run.py`:
- Download `sample.csv:latest` from W&B
- Filter prices: keep rows where `min_price <= price <= max_price`
- Convert `last_review` to datetime
- Save and upload `clean_sample.csv` to W&B

**Finally update** `main.py` lines 60-66:
- Replace `# YOUR CODE HERE` with parameter dictionary

### Task 2: Complete train_random_forest Placeholders

**Status:** ⚠️ 7 placeholders to fill

**File:** `src/train_random_forest/run.py`

Replace `# YOUR CODE HERE` at:
- **Line 57:** `trainval_local_path = run.use_artifact(args.trainval_artifact).file()`
- **Line 78:** `sk_pipe.fit(X_train, y_train)`
- **Line 100:** `mlflow.sklearn.save_model(sk_pipe, "random_forest_dir")`
- **Line 109:** Create W&B artifact and upload model directory
- **Line 119:** `run.summary['mae'] = mae`
- **Line 159:** `non_ordinal_categorical_preproc = make_pipeline(SimpleImputer(...), OneHotEncoder())`
- **Line 218:** `sk_pipe = Pipeline([("preprocessor", preprocessor), ("random_forest", random_forest)])`

### Task 3: Implement Missing Tests

**Status:** ⚠️ 2 functions missing

**File:** `src/data_check/test_data.py`

Add after line 60:
```python
def test_row_count(data: pd.DataFrame):
    """Test that dataset has at least 1000 rows"""
    assert len(data) > 1000

def test_price_range(data: pd.DataFrame, min_price: float, max_price: float):
    """Test that all prices are within expected range"""
    assert data['price'].min() >= min_price
    assert data['price'].max() <= max_price
```
