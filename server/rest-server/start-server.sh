#!/bin/bash

# Script to start FastAPI server with environment selection
# Default: rest environment

ENV_TYPE="${1}"

# If no argument provided, show usage and default to rest
if [[ -z "$ENV_TYPE" ]]; then
    echo "No environment specified. Using default: rest"
    ENV_TYPE="rest"
fi

# Validate environment choice
if [[ "$ENV_TYPE" != "rest" && "$ENV_TYPE" != "ml" ]]; then
    echo "Error: Invalid environment '$ENV_TYPE'"
    echo ""    #!/bin/bash
    
    # Script to start FastAPI server with environment selection
    # Default: rest environment
    
    ENV_TYPE="${1}"
    
    # If no argument provided, show usage and default to rest
    if [[ -z "$ENV_TYPE" ]]; then
        echo "No environment specified. Using default: rest"
        echo ""
        echo "Usage: ./start-server.sh [rest|ml]"
        echo "  rest - REST API only (lightweight) [DEFAULT]"
        echo "  ml   - REST API + ML dependencies"
        echo ""
        ENV_TYPE="rest"
    fi
    
    # Validate environment choice
    if [[ "$ENV_TYPE" != "rest" && "$ENV_TYPE" != "ml" ]]; then
        echo "Error: Invalid environment '$ENV_TYPE'"
        echo ""
        echo "Usage: ./start-server.sh [rest|ml]"
        echo "  rest - REST API only (lightweight) [DEFAULT]"
        echo "  ml   - REST API + ML dependencies"
        exit 1
    fi
    
    # Select environment based on argument
    if [[ "$ENV_TYPE" == "rest" ]]; then
        ENV_NAME="sinceAI-Rest"
        ENV_FILE="environment-rest.yml"
    else
        ENV_NAME="sinceAI"
        ENV_FILE="environment.yml"
    fi
    
    echo "Starting FastAPI with $ENV_NAME environment..."
    
    # Check if already in a conda environment
    if [[ -n "$CONDA_DEFAULT_ENV" && "$CONDA_DEFAULT_ENV" != "base" ]]; then
        echo "Already in conda environment: $CONDA_DEFAULT_ENV"
        if [[ "$CONDA_DEFAULT_ENV" != "$ENV_NAME" ]]; then
            echo "Switching to $ENV_NAME..."
            conda activate $ENV_NAME
            if [[ $? -ne 0 ]]; then
                echo "Failed to switch environments. Creating $ENV_NAME..."
                conda env create -f $ENV_FILE
                conda activate $ENV_NAME
            fi
        else
            echo "$ENV_NAME is already active. Proceeding..."
        fi
    else
        # Not in a conda environment, activate the required one
        source activate $ENV_NAME
    
        if [[ $? -ne 0 ]]; then
            echo "Environment $ENV_NAME not found. Creating it..."
            conda env create -f $ENV_FILE
            source activate $ENV_NAME
        fi
    fi
    
    # Start FastAPI server
    echo "Launching uvicorn server on http://localhost:8000"
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    echo "Usage: ./start-server.sh [rest|ml]"
    echo "  rest - REST API only (lightweight) [DEFAULT]"
    echo "  ml   - REST API + ML dependencies"
    exit 1
fi

# Select environment based on argument
if [[ "$ENV_TYPE" == "rest" ]]; then
    ENV_NAME="sinceAI-Rest"
    ENV_FILE="environment-rest.yml"
else
    ENV_NAME="sinceAI"
    ENV_FILE="environment.yml"
fi

echo "Starting FastAPI with $ENV_NAME environment..."

if [[ $? -ne 0 ]]; then
    echo "Environment $ENV_NAME not found. Creating it..."
    conda env create -f $ENV_FILE
    source activate $ENV_NAME
fi

# Start FastAPI server
echo "Launching uvicorn server on http://localhost:8000"
uvicorn main:app --reload --host 0.0.0.0 --port 8000