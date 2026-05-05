# Vercel Deployment Guide

## Overview
This guide will deploy your Real Estate CRM to **Vercel** (free tier) with a **PostgreSQL** database (free via Neon).

---

## Step 1: Create Free PostgreSQL Database (Neon)

1. Go to [neon.tech](https://neon.tech)
2. Sign up with GitHub
3. Create a new project
4. Copy the **Connection String** (looks like: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require`)

---

## Step 2: Generate a Secret Key

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Save this key for Step 3.

---

## Step 3: Push to GitHub

```powershell
cd D:\Webapps\project_2\myproject
git init
git add .
git commit -m "Initial commit: Real Estate CRM"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

---

## Step 4: Deploy to Vercel

### Option A: Vercel CLI (Recommended)

```powershell
npm i -g vercel
cd D:\Webapps\project_2\myproject
vercel
```

Follow the prompts, then add environment variables:

```powershell
vercel env add SECRET_KEY
vercel env add DATABASE_URL
vercel env add DEBUG
vercel env add ALLOWED_HOSTS
```

Values:
| Variable | Value |
|---|---|
| `SECRET_KEY` | Your generated key from Step 2 |
| `DATABASE_URL` | Neon connection string from Step 1 |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1,.vercel.app` |

### Option B: Vercel Dashboard

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Import your GitHub repo
4. Set environment variables in **Settings > Environment Variables**
5. Click **Deploy**

---

## Step 5: Run Migrations on Production

After first deploy, run migrations:

```powershell
vercel env pull .env.production
```

Then locally:
```powershell
DATABASE_URL="your-neon-url" python manage.py migrate
```

Or use the Vercel dashboard **Shell** feature:
1. Go to your Vercel project > **Settings** > **General** > **Deployment Protection** > set to **Standard**
2. Go to **Deployments** > click your deployment > **...** > **Shell**
3. Run: `python manage.py migrate`

---

## Step 6: Create Superuser

Run in Vercel Shell or locally with production DATABASE_URL:

```powershell
python manage.py createsuperuser
```

---

## Step 7: Access Your App

Your CRM will be at: `https://your-project.vercel.app`

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Django secret key |
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `DEBUG` | No | Set to `False` in production |
| `ALLOWED_HOSTS` | No | Comma-separated hostnames |
| `CSRF_TRUSTED_ORIGINS` | No | Comma-separated URLs (e.g., `https://your-project.vercel.app`) |

---

## Troubleshooting

**SQLite Error**: Vercel doesn't persist SQLite. You MUST use PostgreSQL (Neon, Supabase, etc.)

**Static Files Missing**: WhiteNoise is configured. Run `collectstatic` if needed:
```powershell
python manage.py collectstatic --noinput
```

**Cold Start Slow**: Normal for free tier. First request takes 2-5 seconds.

**CSRF Error**: Add your Vercel URL to `CSRF_TRUSTED_ORIGINS` env var.
