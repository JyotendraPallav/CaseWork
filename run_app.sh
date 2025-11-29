#!/bin/bash

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    venv/bin/pip install -r requirements.txt
fi

echo "Starting CaseWork Scheduler..."
echo "Opening browser..."
open http://127.0.0.1:7860 &

venv/bin/python app.py
