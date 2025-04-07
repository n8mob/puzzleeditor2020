#!/bin/bash

set -e
set -o pipefail

echo "📥 Pulling from GitHub..."
git pull origin main

echo "🎒Activate python virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🧹Building static files..."
python3 manage.py collectstatic --noinput
