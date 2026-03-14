# 🚀 Deployment Guide - Flask Portfolio to Render

## Overview
This guide will get your portfolio **live on the internet for FREE** using:
- **GitHub** - Code repository
- **Render** - Web hosting (replaces Heroku)
- **Neon** - PostgreSQL database (free tier)
- **GitHub Actions** - Automatic CI/CD pipeline

Total cost: **$0/month** ✨

---

## 📊 Architecture

```
Your Computer
    ↓ git push
GitHub Repository
    ↓ webhook trigger
GitHub Actions (CI/CD)
    ↓ tests pass
Render Web Service
    ↓ connects to
Neon PostgreSQL Database
    ↓
Your Portfolio Live! 🎉
```

---

## ✅ Prerequisites Checklist

- [x] GitHub account (rahul124rahul)
- [x] GitHub Personal Access Token (you're getting this now)
- [ ] Render account (free signup)
- [ ] Neon account (free signup)
- [ ] Gmail account with App Password

---

## 🔧 STEP 1: Initialize Git & Push to GitHub (5 min)

### 1.1 Initialize Local Git Repository

```bash
cd c:\Work\portfolio-flask
git init
git branch -M main
git add .
git commit -m "Initial commit: Flask developer portfolio with features"
```

### 1.2 Create GitHub Repository

Go to https://github.com/new and create:
- **Repository name:** `portfolio-flask`
- **Description:** "Professional Flask developer portfolio"
- **Public:** Yes (for deployment)
- **Don't initialize with README** (you already have one)

### 1.3 Add Remote & Push

```bash
git remote add origin https://github.com/rahul124rahul/portfolio-flask.git
git push -u origin main
```

✅ Your code is now on GitHub!

---

## 🗄️ STEP 2: Set Up Neon PostgreSQL Database (5 min)

### 2.1 Create Neon Account

1. Go to https://neon.tech
2. Sign up (free) using your GitHub account (easier!)
3. Create a new project: `portfolio-flask`

### 2.2 Get Connection String

1. In Neon dashboard, go to your project
2. Click **"Connection string"**
3. Make sure it says **"PostgreSQL"**
4. Copy the entire URL (looks like):
   ```
   postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/portfolio_db?sslmode=require
   ```

5. **Save this** - you'll need it for Render!

### 2.3 Create Initial Database Tables

```bash
# Set DATABASE_URL to your Neon connection string
$env:DATABASE_URL="postgresql://..."

# Run migrations
flask db upgrade
```

✅ Your database is ready!

---

## 🌐 STEP 3: Deploy to Render (5 min)

### 3.1 Create Render Account

1. Go to https://render.com
2. Sign up (free, use GitHub login for easier auth)

### 3.2 Create Web Service

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository:
   - Select `portfolio-flask` repository
   - Allow Render to access your GitHub
3. Configure the service:

**Name:** `portfolio-flask`

**Environment:** `Python`

**Build Command:**
```bash
pip install -r requirements.txt && flask db upgrade
```

**Start Command:**
```bash
gunicorn run:app
```

**Plan:** `Free`

### 3.3 Add Environment Variables

In Render dashboard, go to **Environment** section and add:

```
DATABASE_URL = postgresql://user:pass@...neon.tech/portfolio_db?sslmode=require
SECRET_KEY = (generate: python -c "import secrets; print(secrets.token_hex(32))")
JWT_SECRET_KEY = (generate: python -c "import secrets; print(secrets.token_hex(32))")
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USERNAME = your-email@gmail.com
MAIL_PASSWORD = your-gmail-app-password
ADMIN_EMAIL = your-email@gmail.com
SITE_URL = https://portfolio-flask.onrender.com
FLASK_ENV = production
```

### 3.4 Deploy

Click **"Deploy Web Service"**

⏳ Wait 3-5 minutes for first deployment

✅ Check the **Logs** tab - should see "Application running on 0.0.0.0:10000"

---

## 🎯 STEP 4: Initialize Database on Render (2 min)

After deployment succeeds:

1. In Render dashboard, go to your service
2. Click **"Shell"** tab
3. Run:
   ```bash
   flask db upgrade
   ```

This creates all the tables in your Neon database!

---

## ✅ STEP 5: Test Your Deployment

1. Go to your Render dashboard
2. Click the **URL** at the top (like `https://portfolio-flask.onrender.com`)
3. Your portfolio should be **LIVE**! 🎉

**Test these features:**
- [ ] Homepage loads cleanly
- [ ] Skills, projects, experience visible
- [ ] Resume viewer works
- [ ] Number game plays
- [ ] Visitor counter increments
- [ ] Contact form appears

---

## 🔄 STEP 6: Set Up CI/CD (Automatic Deploys)

Your `.github/workflows/ci.yml` already exists and will:

1. **Lint** - Check code quality (flake8)
2. **Test** - Run pytest with SQLite
3. **Build** - Build Docker image (Render uses this)

### How it works:

```
You push to GitHub
    ↓
GitHub Actions runs tests
    ↓
Tests pass ✅
    ↓
Render sees new push
    ↓
Auto-deploys new version
    ↓
Your site updates live!
```

**No manual deployment needed** - just `git push` and you're done!

---

## 🚨 Troubleshooting

### Issue: "Database connection failed"
**Solution:** Check DATABASE_URL in Render environment variables. Make sure it includes `?sslmode=require` at the end.

### Issue: "Module not found error"
**Solution:** Your `requirements.txt` might be missing packages. Check it includes all dependencies.

### Issue: "502 Bad Gateway"
**Solution:** App crashed. Check logs in Render dashboard. Usually a code issue - fix locally, commit, push.

### Issue: "Admin login not working"
**Solution:** Run in Render shell:
```bash
flask shell
>>> from app import db
>>> from app.models import Admin
>>> admin = Admin(username='testadmin', email='test@example.com')
>>> admin.set_password('testpass123')
>>> db.session.add(admin)
>>> db.session.commit()
```

---

## 📱 Post-Deployment Checklist

- [ ] Portfolio is live and loading
- [ ] Admin login works (`/admin/login`)
- [ ] Add content in admin panel
- [ ] Test contact form (sends to your email)
- [ ] Add your GitHub username to social links (for GitHub stats)
- [ ] Test on mobile (responsive?)
- [ ] Update profile info in admin
- [ ] Upload resume
- [ ] Share the live URL! 🚀

---

## 🎓 Next Steps (Optional)

### 1. Custom Domain
- Buy domain ($10-15/year)
- Point DNS to Render
- Enable SSL in Render settings

### 2. Monitoring
- Check Render logs regularly
- Set up email alerts (optional)

### 3. Backup Database
- Neon auto-backups for free
- Backup locally: `pg_dump DATABASE_URL > backup.sql`

### 4. Update Content
- Admin panel available at `/admin/dashboard`
- Login with credentials you created

---

## 🆘 Need Help?

### Common Commands

```bash
# Check deployment logs
# Go to Render dashboard → Service → Logs

# Run Flask shell on Render
# Render dashboard → Service → Shell
flask shell

# View deployed app logs
# Render dashboard → Logs tab

# Restart the service
# Render dashboard → Restart button
```

---

## 📞 Support Resources

- **Render Docs:** https://render.com/docs
- **Neon Docs:** https://neon.tech/docs
- **Flask Docs:** https://flask.palletsprojects.com
- **GitHub Actions:** https://docs.github.com/en/actions

---

## ✨ Congratulations!

Your portfolio is now:
- ✅ Version controlled (GitHub)
- ✅ Automatically tested (GitHub Actions)
- ✅ Automatically deployed (Render)
- ✅ Live on the internet (Free forever!)
- ✅ Scalable (upgrade anytime)

**Your portfolio URL:** `https://portfolio-flask.onrender.com`

🎉 **You're live!** 🚀
