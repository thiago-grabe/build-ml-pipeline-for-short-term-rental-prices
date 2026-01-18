# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ EDUCATIONAL PROJECT - PRESERVE STUDENT LEARNING

**CRITICAL**: This project is designed for student learning. Some code is intentionally incomplete with TODO placeholders for students to implement. When working on this codebase:

- **DO NOT** implement any `# YOUR CODE HERE` or `# Implement here #` placeholders
- **DO NOT** create `src/basic_cleaning/` directory (students create this with cookiecutter)
- **DO NOT** fill in TODOs in `main.py`, `src/train_random_forest/run.py`, or `src/data_check/test_data.py`
- **ONLY FIX** infrastructure bugs (Python version, MLproject names, dependency conflicts)

### Student Implementation Requirements

Students must implement:

1. **Pipeline Orchestration** (`main.py` lines 52-91): 5 pipeline steps
2. **Model Training** (`src/train_random_forest/run.py` lines 57-218): 5 ML operations
3. **Data Validation** (`src/data_check/test_data.py` lines 63-65): 2 pytest functions

See `CODESPACES_QUICKSTART.md` for details on student tasks.

## Project Overview

This is an MLflow-based ML pipeline for predicting short-term rental prices in NYC. The pipeline uses Weights & Biases (W&B) for artifact tracking and experiment management. It's designed for weekly retraining with new data samples.

**Python Version**: Python 3.12.7 is required (NOT 3.13 - MLflow compatibility)

## Development Environment Setup

### Option 1: GitHub Codespaces (Recommended for Students)

The easiest way to get started is using GitHub Codespaces, which provides a pre-configured development environment:

1. Fork this repository to your GitHub account
2. Add W&B API key to GitHub Codespaces secrets (Settings → Codespaces → Secrets)
3. Click "Code" → "Codespaces" → "Create codespace on main"
4. Wait for setup to complete (~3 minutes first time, ~30 seconds after)

See `CODESPACES_QUICKSTART.md` for detailed instructions.

**Benefits**:
- Zero local setup required
- Pre-configured Python 3.12.7 + MLflow 2.18.0
- Consistent environment across all students
- Free tier: 60 core-hours/month (15 hours on 4-core)

### Option 2: Local Conda Environment

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate nyc_airbnb_dev

# Login to Weights & Biases
wandb login [your API key]
```

## Running the Pipeline

### Execute entire pipeline
```bash
mlflow run .
```

### Execute specific steps
```bash
# Single step
mlflow run . -P steps=download

# Multiple steps
mlflow run . -P steps=download,basic_cleaning

# Override config parameters using Hydra syntax
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.random_forest.n_estimators=100 etl.min_price=50"
```

### Run hyperparameter optimization
```bash
# Multi-run with Hydra (-m flag)
mlflow run . \
  -P steps=train_random_forest \
  -P hydra_options="modeling.max_tfidf_features=10,15,30 modeling.random_forest.max_features=0.1,0.33,0.5 -m"
```

### Test production model
```bash
# Must manually tag a model as "prod" in W&B first
mlflow run . -P steps=test_regression_model
```

### Run from GitHub release
```bash
mlflow run https://github.com/[username]/build-ml-pipeline-for-short-term-rental-prices.git \
  -v 1.0.0 \
  -P hydra_options="etl.sample='sample2.csv'"
```

## Pipeline Architecture

### Configuration System

The pipeline uses **Hydra** for configuration management:
- Configuration file: `config.yaml` in the project root
- All parameters MUST be read from config - no hardcoding
- Access in `main.py` via: `config["section"]["parameter"]`
- Hydra executes scripts in a different directory than the project root

### Pipeline Steps

The pipeline is orchestrated by `main.py` with steps defined in the `_steps` list:

1. **download** - Fetches raw data sample using pre-built component `get_data`
2. **basic_cleaning** - Removes outliers, handles dates (implemented in `src/basic_cleaning/`)
3. **data_check** - pytest-based data validation (in `src/data_check/`)
4. **data_split** - Segregates test set using pre-built component `train_val_test_split`
5. **train_random_forest** - Trains RF model with feature engineering (in `src/train_random_forest/`)
6. **test_regression_model** - Tests production model (pre-built component, requires manual "prod" tag)

### Component Types

**Pre-existing reusable components** (in `components/`):
- `get_data` - Downloads data samples
- `train_val_test_split` - Splits data into train/val/test sets
- `test_regression_model` - Evaluates models on test data
- Referenced via GitHub URL: `config['main']['components_repository']`

**Custom pipeline steps** (in `src/`):
- `basic_cleaning` - Data cleaning logic
- `data_check` - Data validation tests using pytest
- `train_random_forest` - Model training with sklearn pipeline
- `eda` - Jupyter-based exploratory analysis

Each step has:
- `conda.yml` - Conda environment specification
- `MLproject` - MLflow project definition with parameters
- `run.py` - Main execution script

### Artifact Management with W&B

**Critical**: Always specify artifact versions/tags:
- Use `:latest` or `:reference` or `:prod` tag when referencing artifacts
- Example: `sample.csv:latest` NOT `sample.csv`
- Forgetting tags causes: `Attempted to fetch artifact without alias`

**Artifact flow**:
- `sample.csv` (raw_data) → `clean_sample.csv` (clean_sample) → `trainval_data.csv` + `test_data.csv` → `random_forest_export` (model)

**Tagging convention**:
- `latest` - Most recent version
- `reference` - Reference dataset for distribution tests
- `prod` - Production-ready model

### Creating New Steps with Cookiecutter

```bash
cookiecutter cookie-mlflow-step -o src

# Example for basic_cleaning:
step_name: basic_cleaning
script_name: run.py
job_type: basic_cleaning
short_description: A very basic data cleaning
long_description: Download from W&B the raw dataset and apply some basic data cleaning
parameters: input_artifact,output_artifact,output_type,output_description,min_price,max_price
```

### Adding Steps to main.py

**Important path construction** (required due to Hydra's working directory change):
```python
if "basic_cleaning" in active_steps:
    _ = mlflow.run(
        os.path.join(hydra.utils.get_original_cwd(), "src", "basic_cleaning"),
        "main",
        parameters={
            "input_artifact": "sample.csv:latest",  # Must include version tag!
            "output_artifact": "clean_sample.csv",
            "min_price": config['etl']['min_price'],  # Read from config
            # ... other parameters
        },
    )
```

## Key Implementation Patterns

### Data Testing with pytest

Tests are defined in `src/data_check/test_data.py` using pytest fixtures:
- Fixtures defined in `conftest.py` provide: `data`, `ref_data`, `kl_threshold`, `min_price`, `max_price`
- Test functions MUST use exact fixture names for closures to work
- Example: `def test_price_range(data, min_price, max_price):`

### Feature Engineering in train_random_forest

The training pipeline implements:
- **Ordinal encoding** for room_type (ordered categorical)
- **One-hot encoding** for neighbourhood_group (with imputation)
- **Zero imputation** for numerical features
- **Date feature**: Days since last review (using `delta_date_feature()`)
- **NLP feature**: TF-IDF on listing name (limited by `max_tfidf_features`)

Preprocessing is encapsulated in `get_inference_pipeline()` which returns a sklearn Pipeline.

### Model Export and Logging

Save models using MLflow sklearn format:
```python
mlflow.sklearn.save_model(sk_pipe, "random_forest_dir")

artifact = wandb.Artifact(
    args.output_artifact,
    type="model_export",
    description="...",
    metadata=rf_config
)
artifact.add_dir("random_forest_dir")
run.log_artifact(artifact)
```

## Dependency Management

**Always add dependencies to `conda.yml`** when using new libraries:
```yaml
dependencies:
  - pip=24.3.1
  - pandas=2.3.2
  - pip:
      - mlflow==3.3.2
      - wandb==0.21.3
```

## Common Issues and Solutions

### Corrupted MLflow Environments

If conda environments created by mlflow are corrupted:
```bash
# List environments
conda info --envs | grep mlflow | cut -f1 -d" "

# Remove all mlflow environments (USE WITH CAUTION)
for e in $(conda info --envs | grep mlflow | cut -f1 -d" "); do conda uninstall --name $e --all -y; done
```

### Data Validation Failures

When `test_proper_boundaries` fails on new data:
- Add geographic filtering in `basic_cleaning` step before saving CSV
- Example: Filter longitude/latitude to NYC boundaries
- Create new release after fixing

## Testing and Releases

1. Find best model in W&B by sorting runs by MAE (ascending)
2. Tag best model artifact with `prod` in W&B UI
3. Run test step: `mlflow run . -P steps=test_regression_model`
4. Copy best hyperparameters to `config.yaml`
5. Create GitHub release (e.g., `1.0.0`, `1.0.1`)
6. Test release on new data using `mlflow run [github-url] -v [version]`
