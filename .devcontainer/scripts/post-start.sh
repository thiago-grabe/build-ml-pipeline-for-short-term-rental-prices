#!/bin/bash
set -e

echo "👋 Welcome to NYC Airbnb ML Pipeline Codespace!"

# Activate conda environment
source /opt/conda/etc/profile.d/conda.sh
conda activate nyc_airbnb_dev

# Show environment info
echo ""
echo "📊 Environment Information:"
echo "  Python: $(python --version)"
echo "  MLflow: $(mlflow --version)"
echo "  Conda env: $CONDA_DEFAULT_ENV"
echo ""

# Check disk space
echo "💾 Disk Space:"
df -h /workspaces | tail -1
echo ""

# Quick start reminder
echo "🚀 Quick Start:"
echo "  Run full pipeline:  mlflow run ."
echo "  Run single step:    mlflow run . -P steps=download"
echo "  Open Jupyter:       mlflow run src/eda"
echo ""
echo "📚 Documentation:"
echo "  README.md           - Project overview"
echo "  Quick_Start_Guide.md - Step-by-step tutorial"
echo "  CLAUDE.md           - Architecture notes"
echo ""
