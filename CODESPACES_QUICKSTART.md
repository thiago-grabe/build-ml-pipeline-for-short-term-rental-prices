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

### Full Pipeline
```bash
mlflow run .
```

### Single Steps
```bash
# Download data
mlflow run . -P steps=download

# Data cleaning
mlflow run . -P steps=basic_cleaning

# Multiple steps
mlflow run . -P steps=download,basic_cleaning,data_check
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

**IMPORTANT**: This project includes TODO sections for you to implement as part of your learning. The following sections are intentionally incomplete:

### 1. Pipeline Orchestration (`main.py`)
You need to implement 5 pipeline steps:
- `basic_cleaning` - Clean raw data (remove outliers, convert dates)
- `data_check` - Run pytest-based data validation
- `data_split` - Split data into train/val/test sets
- `train_random_forest` - Train RF model with feature engineering
- `test_regression_model` - Evaluate production model

### 2. Model Training (`src/train_random_forest/run.py`)
You need to implement:
- Download artifact with `run.use_artifact(...).file()`
- Fit model with `sk_pipe.fit(X_train, y_train)`
- Save model with `mlflow.sklearn.save_model(...)`
- Create and log W&B artifact
- Log MAE metric

### 3. Data Validation (`src/data_check/test_data.py`)
You need to implement pytest functions:
- `test_row_count(data)` - Verify dataset size
- `test_price_range(data, min_price, max_price)` - Validate price bounds

See `CLAUDE.md` for detailed implementation requirements.
