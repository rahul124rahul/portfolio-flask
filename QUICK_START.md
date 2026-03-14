# 🚀 Deployment Quick Reference

## Your Portfolio Details
- **GitHub:** https://github.com/rahul124rahul/portfolio-flask
- **Portfolio URL (after deploy):** https://portfolio-flask.onrender.com
- **Admin Panel:** https://portfolio-flask.onrender.com/admin/login

---

## 📋 Three Simple Steps to Live

### Step 1: Push Code to GitHub (5 min)
**Windows:**
```bash
cd c:\Work\portfolio-flask
deploy-setup.bat <your-github-token>
```

**Mac/Linux:**
```bash
cd ~/portfolio-flask
./deploy-setup.sh "your-github-token"
```

### Step 2: Create Neon Database (5 min)
1. Go to https://neon.tech
2. Sign up (free)
3. Create project, copy connection URL
4. Save the URL

### Step 3: Deploy to Render (5 min)
1. Go to https://render.com
2. Connect GitHub
3. Create Web Service
4. Add environment variables
5. Deploy!

**Estimated total time: 15 minutes ⏱️**

---

## 🔑 Environment Variables Needed

```
DATABASE_URL=<from Neon>
SECRET_KEY=<generate one>
JWT_SECRET_KEY=<generate one>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=<your Gmail>
MAIL_PASSWORD=<Gmail App Password>
ADMIN_EMAIL=<your email>
SITE_URL=https://portfolio-flask.onrender.com
```

---

## 🎯 Testing After Deployment

- [ ] Homepage loads
- [ ] Skills visible
- [ ] Game playable
- [ ] Resume viewable
- [ ] Contact form appears
- [ ] Admin login works

---

## 📱 Keep Live Forever

**Free tier limits:**
- Render: 750 hours/month (more than enough)
- Neon: 0.5GB free database (plenty for portfolio)

**Auto-updates:** Just `git push` and it deploys automatically!

---

## ❓ Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Token invalid" | Generate new token from GitHub |
| "Database connection failed" | Check DATABASE_URL in Render env vars |
| "502 Bad Gateway" | Check Render logs for errors |
| "Admin page not found" | Run `flask db upgrade` in Render shell |

---

## 📞 Get Help

- **Render Dashboard:** https://dashboard.render.com
- **Neon Console:** https://console.neon.tech
- **GitHub Repo:** https://github.com/rahul124rahul/portfolio-flask

---

## ✨ You're Set!

Everything is ready. Just follow the three steps above and you'll be live! 🚀
