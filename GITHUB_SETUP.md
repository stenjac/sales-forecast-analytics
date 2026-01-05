# GitHub Setup Guide

Complete guide to pushing your Sales Forecast Analytics Platform to GitHub.

## 📋 Prerequisites

1. **GitHub Account** - Create one at https://github.com if you don't have one
2. **Git Installed** - Verify with: `git --version`

If Git is not installed:
```bash
# macOS
brew install git

# Or download from: https://git-scm.com/downloads
```

## 🚀 Step-by-Step Guide

### Step 1: Configure Git (First Time Only)

```bash
# Set your name (will appear in commits)
git config --global user.name "Your Name"

# Set your email (use your GitHub email)
git config --global user.email "your.email@example.com"

# Verify configuration
git config --global --list
```

### Step 2: Create GitHub Repository

1. Go to https://github.com
2. Click the **+** icon (top right) → **New repository**
3. Fill in:
   - **Repository name**: `sales-forecast-analytics`
   - **Description**: `Comprehensive sales forecasting and analytics platform with interactive dashboards`
   - **Visibility**: Choose Public or Private
   - **DON'T** check "Initialize with README" (we already have one)
4. Click **Create repository**

GitHub will show you setup instructions - we'll use them below.

### Step 3: Initialize Git in Your Project

```bash
# Navigate to your project directory
cd /Users/stefanomazzalai

# Initialize git repository
git init

# Add all files to staging
git add .

# Check what will be committed
git status
```

### Step 4: Create .gitignore File

Before committing, create a `.gitignore` file to exclude unnecessary files:

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Data (optional - remove if you want to include sample data)
# opportunities.csv

# Generated visualizations (optional - these are auto-generated)
# *.html

# Logs
*.log
EOF

# Add .gitignore to git
git add .gitignore
```

### Step 5: Make First Commit

```bash
# Create initial commit
git commit -m "Initial commit: Sales Forecast Analytics Platform

Features:
- Enhanced Streamlit dashboard with professional UI
- Command-line forecast tool with 11 analysis modules
- 5 interactive Plotly visualizations
- Comprehensive documentation
- Sample dataset with 100 opportunities"

# Verify commit
git log --oneline
```

### Step 6: Connect to GitHub Repository

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/sales-forecast-analytics.git

# Verify remote
git remote -v
```

### Step 7: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

**If prompted for credentials:**
- Username: Your GitHub username
- Password: Use a **Personal Access Token** (not your GitHub password)

### Step 8: Create Personal Access Token (If Needed)

If GitHub asks for a password and rejects it:

1. Go to https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Name it: "Sales Forecast Analytics Push"
4. Select scopes: Check **repo** (all sub-options)
5. Click **Generate token**
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

### Step 9: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/sales-forecast-analytics`
2. You should see all your files!
3. The README.md will display automatically

## 🎨 Customize Your README

Before pushing, update these sections in `README.md`:

```bash
# Edit README
nano README.md  # or use any text editor
```

**Replace:**
1. `YOUR_USERNAME` → Your GitHub username
2. `Your Name` → Your actual name
3. Add actual screenshot URLs (optional)

**Save and commit changes:**
```bash
git add README.md
git commit -m "Update README with GitHub username and author info"
git push
```

## 📸 Adding Screenshots (Optional)

To make your README more attractive:

### Method 1: Use GitHub Issues
1. Go to your repo → Issues → New Issue
2. Drag/drop screenshots into the comment box
3. Copy the generated URLs
4. Paste into README.md

### Method 2: Use Screenshots Directory
```bash
# Create screenshots directory
mkdir screenshots

# Add your screenshots there
# Then update README.md image paths:
# ![Overview](screenshots/overview.png)

# Commit
git add screenshots/
git commit -m "Add dashboard screenshots"
git push
```

### Method 3: Use Placeholder Service
Keep the placeholders already in README (via.placeholder.com) - they work immediately!

## 🏷️ Create Release Tags (Optional)

```bash
# Tag version 1.0
git tag -a v1.0 -m "Version 1.0: Initial release"
git push origin v1.0

# Tag version 2.0 (enhanced dashboard)
git tag -a v2.0 -m "Version 2.0: Enhanced dashboard with professional UI"
git push origin v2.0
```

## 🌿 Working with Branches (Best Practices)

```bash
# Create a new feature branch
git checkout -b feature/new-analysis

# Make changes, then commit
git add .
git commit -m "Add new analysis module"

# Push branch to GitHub
git push -u origin feature/new-analysis

# On GitHub: Create Pull Request to merge into main
```

## 🔄 Regular Updates

After making changes to your code:

```bash
# Check what changed
git status

# Add specific files
git add dashboard_enhanced.py
git add forecast.py

# Or add everything
git add .

# Commit with descriptive message
git commit -m "Fix: Improve color contrast in Methodology section"

# Push to GitHub
git push
```

## 📝 Commit Message Best Practices

Use clear, descriptive messages:

```bash
# Good examples:
git commit -m "Add forecast confidence indicators to dashboard"
git commit -m "Fix: Color contrast issue in metric values"
git commit -m "Update: Improve mobile responsiveness"
git commit -m "Docs: Add installation instructions to README"

# Categories:
# Add: New feature
# Fix: Bug fix
# Update: Improvement to existing feature
# Docs: Documentation changes
# Refactor: Code restructuring
# Test: Adding tests
```

## 🛡️ Add License File

```bash
# Create MIT License file
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Commit license
git add LICENSE
git commit -m "Add MIT License"
git push
```

## 🎯 Add GitHub Topics

On GitHub repository page:
1. Click the gear icon ⚙️ next to "About"
2. Add topics: `python`, `streamlit`, `sales-analytics`, `forecasting`, `data-visualization`, `plotly`, `dashboard`, `sales-operations`
3. Save changes

## 📊 Enable GitHub Pages (Optional)

If you want to host documentation:
1. Go to Settings → Pages
2. Source: Deploy from branch
3. Branch: main, folder: /docs or /root
4. Save

## ✅ Verification Checklist

- [ ] Git initialized (`git status` works)
- [ ] .gitignore created
- [ ] All files committed
- [ ] Remote added to GitHub
- [ ] Pushed to GitHub successfully
- [ ] README displays correctly on GitHub
- [ ] Updated README with your username/name
- [ ] License file added (optional)
- [ ] Topics added (optional)
- [ ] Screenshots added (optional)

## 🆘 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/sales-forecast-analytics.git
```

### Error: "failed to push some refs"
```bash
# Pull first, then push
git pull origin main --rebase
git push -u origin main
```

### Error: "Authentication failed"
- Make sure you're using a Personal Access Token, not your password
- Token needs `repo` scope permissions

### Large files warning
```bash
# If CSV or HTML files are too large, add to .gitignore
echo "opportunities.csv" >> .gitignore
echo "*.html" >> .gitignore
git rm --cached opportunities.csv
git rm --cached *.html
git commit -m "Remove large files from tracking"
git push
```

## 🎉 You're Done!

Your repository is now live at:
```
https://github.com/YOUR_USERNAME/sales-forecast-analytics
```

Share this URL with:
- Team members
- Hiring managers (for portfolio)
- Community (get stars ⭐)

---

**Next Steps:**
1. Add a description to your GitHub repo
2. Add topics for discoverability
3. Share on LinkedIn/Twitter
4. Consider adding GitHub Actions for CI/CD
5. Add contributing guidelines if open to contributions

