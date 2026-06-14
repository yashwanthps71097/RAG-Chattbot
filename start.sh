#!/bin/bash

# Start the daily scheduler in the background
echo "Starting daily scheduler daemon in the background..."
python -m scheduler.daily &

# Start the FastAPI web application
echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT
