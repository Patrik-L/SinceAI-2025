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

# Start FastAPI server in the conda environment
echo "Launching uvicorn server on http://localhost:8000"
conda run -n $ENV_NAME uvicorn main:app --reload --host 0.0.0.0 --port 8000