#!/bin/bash

# Activate virtual environment (if needed)
source venv/bin/activate

# Run the FastAPI app with uvicorn
uvicorn src.backend.email_sender.main:app --reload
