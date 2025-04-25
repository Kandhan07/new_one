#!/bin/bash
set -e

# Install system dependencies
apt-get update
apt-get install -y --no-install-recommends \
    libpango-1.0-0 \
    libharfbuzz0b \
    libpangoft2-1.0-0

# Install Python dependencies
pip install -r requirements.txt