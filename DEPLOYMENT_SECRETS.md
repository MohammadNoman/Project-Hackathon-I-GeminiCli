# Deployment Secrets Management

This document outlines how to securely manage environment variables and API keys required for deployment of both the frontend (Docusaurus) and backend (FastAPI) components of the Physical AI & Humanoid Robotics Textbook Platform.

## 1. GitHub Secrets

Sensitive API keys and credentials **MUST NOT** be committed directly to the repository. Instead, they should be stored as GitHub Secrets and accessed within GitHub Actions workflows.

**For FastAPI Backend Deployment:**
*   `DOCKER_USERNAME`: Your Docker registry username (e.g., Docker Hub).
*   `DOCKER_PASSWORD`: Your Docker registry password or access token.
*   `GCP_SA_KEY` (Optional, for Google Cloud Run): The JSON key file content for your Google Cloud Service Account, base64 encoded.
*   `GCP_PROJECT_ID` (Optional, for Google Cloud Run): Your Google Cloud Project ID.
*   `AWS_ACCESS_KEY_ID` (Optional, for AWS App Runner): Your AWS Access Key ID.
*   `AWS_SECRET_ACCESS_KEY` (Optional, for AWS App Runner): Your AWS Secret Access Key.

**For Chatbot API Keys (used by backend during runtime):**
These are typically set directly in your chosen serverless platform's environment variables rather than GitHub Secrets, but can be passed through if the platform supports it.

*   `OPENAI_API_KEY`: Your OpenAI API key.
*   `QDRANT_HOST`: Qdrant Cloud service host (e.e., `https://<cluster-id>.qdrant.tech`).
*   `QDRANT_API_KEY`: Qdrant Cloud API key.
*   `NEON_DATABASE_URL`: Connection string for your Neon Serverless Postgres database.

**How to Add GitHub Secrets:**
1.  Navigate to your GitHub repository.
2.  Go to `Settings` > `Secrets and variables` > `Actions`.
3.  Click `New repository secret` and add each secret with its corresponding value.

## 2. Cloud Platform Secrets

For runtime environment variables accessed by the deployed FastAPI backend, these should be configured directly within the chosen serverless platform.

*   **Google Cloud Run:** Environment variables can be configured during deployment using the `gcloud run deploy` command or through the Cloud Run console.
*   **AWS App Runner:** Environment variables are managed within the App Runner service configuration.

Ensure that these runtime secrets are also treated with the highest security, using the platform's native secrets management capabilities.

## 3. Local Development (`.env` file)

For local development, create a `.env` file in your `backend/` directory (based on `backend/.env.example`) and populate it with your actual API keys and connection strings. This file is ignored by Git (`.gitignore`) and is for local use only.
