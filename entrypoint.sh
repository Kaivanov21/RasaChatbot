#!/bin/sh

echo "Activating virtual environment..."
call /app/venv/Scripts/activate.bat

# echo "Training Rasa model..."
# rasa train

echo "Running Rasa server..."
rasa run --enable-api --cors "*" --debug