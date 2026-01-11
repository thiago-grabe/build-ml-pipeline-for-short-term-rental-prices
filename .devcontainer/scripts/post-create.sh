#!/bin/bash
set -e

echo "🚀 Running post-create setup..."

# Activate conda environment
source /opt/conda/etc/profile.d/conda.sh
conda activate nyc_airbnb_dev

# Verify installations
echo "🔍 Verifying installations..."
python --version
conda --version
mlflow --version
pip list | grep wandb

# Check for WANDB_API_KEY
if [ -z "$WANDB_API_KEY" ]; then
    echo "⚠️  WARNING: WANDB_API_KEY is not set!"
    echo "📝 Please add your W&B API key:"
    echo "   1. Go to https://wandb.ai/authorize"
    echo "   2. Copy your API key"
    echo "   3. Add it to GitHub Codespaces secrets"
    echo "   4. Rebuild this codespace"
else
    echo "✅ WANDB_API_KEY is set"
    # Configure wandb
    wandb login --relogin <<< "$WANDB_API_KEY"
fi

echo "✅ Post-create setup complete!"
