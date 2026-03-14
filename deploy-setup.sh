#!/bin/bash
# Portfolio Deployment Setup Script
# This script initializes git, commits code, and pushes to GitHub

set -e

GITHUB_USERNAME="rahul124rahul"
REPO_NAME="portfolio-flask"
GITHUB_TOKEN="$1"  # Pass as first argument

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Usage: ./deploy-setup.sh <github-token>"
    echo ""
    echo "Get your GitHub token from: https://github.com/settings/tokens"
    exit 1
fi

echo "🚀 Starting Portfolio Deployment Setup..."
echo ""

# Initialize Git
echo "1️⃣ Initializing Git repository..."
git init
git branch -M main
echo "✅ Git initialized"

# Add all files
echo ""
echo "2️⃣ Staging all files..."
git add .
echo "✅ Files staged"

# Create initial commit
echo ""
echo "3️⃣ Creating initial commit..."
git commit -m "Initial commit: Flask developer portfolio with advanced features

- Hero section with typing animation
- 3D project card effects with tilt
- Skill gallery with canvas animation
- Interactive number path game
- Resume viewer with PDF.js
- Visitor counter & analytics
- GitHub project import
- Dark mode toggle
- Responsive design
- Email notifications
- 2FA authentication
- REST API endpoints
- SEO optimization
- Docker & CI/CD ready"
echo "✅ Commit created"

# Add remote
echo ""
echo "4️⃣ Adding remote repository..."
git remote add origin "https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
echo "✅ Remote added"

# Push to GitHub
echo ""
echo "5️⃣ Pushing to GitHub (this may take a moment)..."
git push -u origin main
echo "✅ Code pushed to GitHub!"

echo ""
echo "========================================="
echo "✨ Success! Your code is on GitHub ✨"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Create Neon PostgreSQL account: https://neon.tech"
echo "2. Create Render account: https://render.com"
echo "3. Follow the DEPLOYMENT.md guide"
echo ""
echo "Your repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
