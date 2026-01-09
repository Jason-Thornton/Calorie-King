# Deployment Guide - Calorie King

## Option 1: Railway (EASIEST - Recommended!)

Railway is the simplest way to deploy your app. Here's how:

### Step 1: Push to GitHub

1. Create a GitHub account at https://github.com if you don't have one
2. Create a new repository called "calorie-king"
3. Push your code:

```bash
cd "c:\Users\19jbi\Desktop\Calorie King\Calorie-King\Calorie King"
git init
git add .
git commit -m "Initial commit - Calorie King app"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/calorie-king.git
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select your "calorie-king" repository
5. Railway will auto-detect it's a Python app!

### Step 3: Add Environment Variables

In Railway project settings, add these variables:

- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `SECRET_KEY`: Any random string (e.g., `my-super-secret-key-123`)

### Step 4: Done!

Railway will give you a URL like: `https://calorie-king.up.railway.app`

**Cost:** $5/month free credit (usually enough for personal use!)

---

## Option 2: Render (Also Easy!)

### Step 1: Push to GitHub (same as above)

### Step 2: Deploy on Render

1. Go to https://render.com
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** calorie-king
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### Step 3: Add Environment Variables

In Render dashboard, add:

- `ANTHROPIC_API_KEY`: Your API key
- `SECRET_KEY`: Random string

### Step 4: Deploy!

Render gives you a URL like: `https://calorie-king.onrender.com`

**Cost:** Free tier available (app sleeps after 15 min of inactivity)

---

## Option 3: Heroku (Classic Choice)

### Step 1: Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Deploy

```bash
cd "c:\Users\19jbi\Desktop\Calorie King\Calorie-King\Calorie King"
heroku login
heroku create calorie-king-app
git push heroku main
```

### Step 3: Set Environment Variables

```bash
heroku config:set ANTHROPIC_API_KEY=your-api-key-here
heroku config:set SECRET_KEY=your-secret-key-here
```

**Cost:** $5-7/month for basic plan

---

## Sharing with Others

Once deployed, anyone can access your app at the URL!

**For your wife's sister:**
1. Share the Railway/Render URL
2. She creates an account
3. She can track her own meals!

Each user has their own private account and meal history.

---

## Important Notes

### Database Persistence

- Railway: Database persists automatically
- Render Free: Database resets if app is inactive for 30+ days
- Solution: Upgrade to paid plan ($7/month) for persistent storage

### API Costs

Your Anthropic API will be charged based on usage:
- ~$0.001-0.005 per image analysis
- 100 meals/month ≈ $0.50
- Very affordable for personal use!

### Custom Domain (Optional)

You can add a custom domain like `calorieking.com`:
1. Buy domain from Namecheap/GoDaddy
2. In Railway/Render settings, add custom domain
3. Update DNS records

---

## Troubleshooting

**App not loading?**
- Check Railway/Render logs for errors
- Verify ANTHROPIC_API_KEY is set correctly

**Database errors?**
- On first deploy, database auto-creates
- If issues, check logs: `heroku logs --tail` or Railway logs

**Out of memory?**
- Upgrade to paid plan with more RAM

---

## Quick Commands

**View logs:**
- Railway: Click on deployment → View Logs
- Render: Go to Logs tab
- Heroku: `heroku logs --tail`

**Redeploy:**
- Just push to GitHub, auto-deploys!

---

Good luck! Your app is ready to share with the world! 🎉
