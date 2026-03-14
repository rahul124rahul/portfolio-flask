#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt
pip install psycopg2-binary==2.9.9

# Create upload directories
mkdir -p app/static/uploads/profile_images
mkdir -p app/static/uploads/project_images
mkdir -p app/static/uploads/resumes

# Run database migrations
flask db upgrade
