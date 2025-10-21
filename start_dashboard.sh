#!/bin/bash
# Start Discord Bot with Admin Dashboard

echo "🚀 Starting Discord Bot with Admin Dashboard..."
echo ""

# Check if poetry is installed
if command -v poetry &> /dev/null; then
    echo "📦 Using Poetry..."
    poetry run python main.py
else
    echo "📦 Using system Python..."
    python3 main.py
fi
