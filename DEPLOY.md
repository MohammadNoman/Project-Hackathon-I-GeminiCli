# Deploying Your Physical AI Platform 🚀

This guide requires **Render.com** (recommended for ease of use) OR separate accounts on **Vercel** (Frontend) and **Render** (Backend/DB).

## � ZERO-CONFIG DEPLOYMENT (Recommended)

We have added a `render.yaml` Blueprint to the project. This is the easiest way to deploy everything correctly.

1.  Push your code to GitHub.
2.  Go to [Render Dashboard](https://dashboard.render.com).
3.  Click **New +** -> **Blueprint**.
4.  Select your Repository.
5.  Render will automatically stick 2 services:
    *   `textbook-platform-backend`
    *   `textbook-platform-frontend`
6.  Click **Apply**.
7.  **IMPORTANT:** Once the services are created, go to the **Backend Service** > **Environment** and ADD your secrets (`OPENAI_API_KEY`, `NEON_DATABASE_URL`, etc.) which cannot be in the YAML file.
8.  Get the **Backend URL** (e.g., `https://textbook-platform-backend.onrender.com`) and update `frontend/src/config.ts` with it.
9.  Push again to update the frontend.

## 🗄️ 1. Database (Neon Postgres)
...
2.  Copy the **Connection String** (e.g., `postgresql://user:pass@ep-xyz.us-east-2.aws.neon.tech/neondb`).
3.  Save this for the Backend Environment Variables.

## 🧠 2. Vector DB (Qdrant)
1.  Go to [Qdrant Cloud](https://cloud.qdrant.io/) and create a free cluster.
2.  Get the **Cluster URL** and **API Key**.

## 🖥️ 3. Backend Deployment (Render)
1.  Login to [Render.com](https://render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  **Settings:**
    *   **Root Directory:** `backend`
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5.  **Environment Variables:** Add keys from your local `.env`:
    *   `OPENAI_API_KEY`
    *   `QDRANT_HOST`
    *   `QDRANT_API_KEY`
    *   `NEON_DATABASE_URL`
    *   `SECRET_KEY` (Generate a random string)
    *   `ALGORITHM`: `HS256`
    *   `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
6.  Click **Deploy**. Copy your new backend URL (e.g., `https://my-backend.onrender.com`).

## 🌐 4. Frontend Deployment (Render or Vercel)
**Option A: Render (Static Site)**
1.  Click **New +** -> **Static Site**.
2.  Connect the same repo.
3.  **Settings:**
    *   **Root Directory:** `frontend`
    *   **Build Command:** `npm install && npm run build`
    *   **Publish Directory:** `frontend/build`
4.  **Environment Variables**:
    *   *Note: Docusaurus is static. To inject the Backend URL, you must edit the code or use build-time variables.*
    *   **CRITICAL:** Open `frontend/src/config.ts`.
    *   Find `PROD_BACKEND_URL` and REPLACE the placeholder with your **Render Backend URL**.
    *   *Commit and Push this change before deploying the frontend.*
5.  Click **Deploy**.

## ✅ Final Check
1.  Visit your Frontend URL.
2.  Try **Sign Up**.
3.  Try the **Chatbot**.
4.  Try **Personalizing** a chapter.

🎉 **You are live!**
