#!/bin/bash

# Script to start FastAPI server with sinceAI conda environment

ENV_NAME="sinceAI"

echo "Starting FastAPI with $ENV_NAME environment..."

# Check if conda environment exists
if ! conda env list | grep -q "^$ENV_NAME "; then
    echo "Error: Conda environment '$ENV_NAME' not found"
    echo "Create it with: conda env create -f environment.yml"
    exit 1
fi

# Activate the environment
echo "Activating $ENV_NAME environment..."
conda activate $ENV_NAME

if [[ $? -ne 0 ]]; then
    echo "Error: Failed to activate $ENV_NAME environment"
    exit 1
fi

# Start FastAPI server
echo "Launching uvicorn server on http://localhost:8000"
uvicorn main:app --reload --host 0.0.0.0 --port 8000