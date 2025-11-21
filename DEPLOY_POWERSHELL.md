# 🚀 PowerShell Commands for Deployment

## Git Commands (PowerShell Compatible)

### 1. Git Initialize & First Commit
```powershell
# Git initialize
git init

# Add all files
git add .

# Commit (PowerShell me quotes zaroori hain)
git commit -m "Initial commit - Student Management System"

# Remote add karo
git remote add origin YOUR_GITHUB_REPO_URL

# Push karo
git push -u origin main
```

### 2. Agar Already Git Repo Hai
```powershell
# Status check
git status

# Changes add karo
git add .

# Commit
git commit -m "Ready for deployment"

# Push
git push
```

## Python Commands (PowerShell)

### Local Testing
```powershell
# Backend folder me jao
cd backend

# Dependencies install
pip install -r requirements.txt

# Server run karo
python app.py
```

### Python Module Run (Agar zaroorat ho)
```powershell
# PowerShell me -m flag sahi se kaam karta hai
python -m pip install -r backend/requirements.txt
```

## Common Errors & Solutions

### Error: "switch m requires a value"
**Solution**: 
- Command me quotes check karo
- Example: `git commit -m "message"` (quotes zaroori hain)

### Error: "&& operator not supported"
**Solution**: PowerShell me `;` use karo ya alag commands run karo
```powershell
# Wrong:
cd backend && python app.py

# Right:
cd backend; python app.py

# Ya phir:
cd backend
python app.py
```

## Railway Deployment (No Commands Needed!)

Railway me directly GitHub se connect karo - koi commands ki zaroorat nahi!

1. Railway.app pe jao
2. "New Project" → "Deploy from GitHub"
3. Repository select karo
4. Auto-deploy!

## Render Deployment

Render me bhi GitHub se directly connect karo:
1. Render.com pe jao
2. "New +" → "Web Service"
3. GitHub connect karo
4. Settings me yeh add karo:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend; gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

---

**Note**: PowerShell me `&&` kaam nahi karta. `;` use karo ya alag lines me commands run karo!

