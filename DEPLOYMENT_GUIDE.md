# 🚀 HEALYNX-AI Production Deployment Guide
### Backend on Render · Frontend on Vercel · Database on Supabase

This guide outlines the exact, error-free setup to deploy HEALYNX-AI to production in under 10 minutes.

---

## 1. 🗄️ Database: Supabase Setup

1. **Create Project**: Go to [supabase.com](https://supabase.com) ➔ New Project (Recommended region: `Singapore` for Bangladesh users).
2. **Run SQL Schema**:
   - Open Supabase Dashboard ➔ **SQL Editor** ➔ New query.
   - Run the contents of `supabase/migrations/0001_extensions.sql`.
   - Run the contents of `supabase/migrations/0002_core.sql`.
   - Run the contents of `supabase/migrations/0003_security.sql`.
3. **Get Database Connection String**:
   - Go to **Project Settings ➔ Database ➔ Connection Pooling**.
   - Select **Mode: Session** (Port `5432`).
   - Copy URI:
     ```text
     postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres
     ```
   - *(Note: HEALYNX-AI automatically normalizes `postgres://` or `postgresql://` to `postgresql+psycopg://` in Python).*

---

## 2. ⚡ Backend: Render Deployment (`apps/api`)

1. Go to [render.com](https://render.com) ➔ **New ➔ Web Service**.
2. Connect your GitHub repository: `abid-222/HEALYNX-AI`.
3. Configure the service:
   - **Name**: `healynx-api`
   - **Region**: `Singapore`
   - **Branch**: `main`
   - **Root Directory**: *(leave blank)*
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     cd apps/api && pip install -r requirements.txt
     ```
   - **Start Command**:
     ```bash
     cd apps/api && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
4. **Environment Variables**:
   | Variable | Value / Notes |
   |---|---|
   | `APP_ENV` | `production` |
   | `DATABASE_URL` | Your Supabase Session Pooler URI from Step 1 |
   | `JWT_SECRET` | 32+ character random secret string |
   | `CORS_ORIGINS` | `https://healynx-ai.vercel.app,http://localhost:3000` *(Vercel domain)* |
   | `STORAGE_ALLOW_LOCAL` | `1` |
   | `EMAIL_PROVIDER` | `none` *(or `resend` if using Resend API key)* |
   | `GEMINI_API_KEY` | *(Optional: Your Google Gemini API Key)* |

5. Click **Create Web Service**. Your API will be live at:
   `https://healynx-api.onrender.com` (Docs at `/docs`, Health check at `/health`).

---

## 3. 🌐 Frontend: Vercel Deployment (`apps/web`)

1. Go to [vercel.com](https://vercel.com) ➔ **Add New... ➔ Project**.
2. Import `abid-222/HEALYNX-AI`.
3. Configure the Project:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: Click *Edit* ➔ select `apps/web`.
4. **Environment Variables**:
   | Variable | Value |
   |---|---|
   | `NEXT_PUBLIC_API_URL` | `https://healynx-api.onrender.com` *(your Render backend URL)* |

5. Click **Deploy**. Vercel will build and assign your domain:
   `https://healynx-ai.vercel.app`

---

## 🛡️ Built-in Error Protections in HEALYNX-AI

- **Automatic URL Normalization**: Whether you input your Render URL with or without `/api/v1` or trailing slashes, `apps/web/lib/api.ts` resolves it seamlessly.
- **Dynamic Vercel CORS Support**: The backend automatically allows any preview or production Vercel branch via regex (`https://*.vercel.app`) in addition to your configured domain.
- **Psycopg3 Database Driver Auto-Fix**: Automatically upgrades `postgresql://` URIs to SQLAlchemy 2.0 `postgresql+psycopg://` drivers.
