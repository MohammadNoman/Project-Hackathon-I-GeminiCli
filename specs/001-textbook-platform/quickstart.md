# Quickstart Guide: Physical AI & Humanoid Robotics Textbook Platform

**Feature**: Physical AI & Humanoid Robotics Textbook Platform
**Branch**: `001-textbook-platform`
**Date**: 2025-12-01

This guide provides instructions to quickly set up, run, and interact with the Physical AI & Humanoid Robotics Textbook Platform locally.

## 1. Prerequisites

Ensure you have the following installed on your system:

*   **Git**: For cloning the repository.
*   **Node.js** (v20 LTS recommended): For Docusaurus frontend.
*   **npm** (comes with Node.js) or **Yarn**: Package manager for frontend.
*   **Python** (v3.11 recommended): For FastAPI backend and RAG logic.
*   **pip** (comes with Python): Package installer for Python.
*   **Docker** (Optional, but recommended for database setup): For running Neon Serverless Postgres locally (via Docker, or you can use a remote instance).
*   **OpenAI API Key**: Required for the chatbot's OpenAI Agents/ChatKit SDKs.
*   **Qdrant Cloud API Key/Endpoint**: Required for the vector database.
*   **Neon Serverless Postgres Connection String**: For the database.

## 2. Setup

### 2.1. Clone the Repository

```bash
git clone https://github.com/MohammadNoman/Project-Hackathon-I-GeminiCli.git
cd Project-Hackathon-I-GeminiCli
git checkout 001-textbook-platform
```

### 2.2. Frontend Setup (Docusaurus)

Navigate to the frontend directory and install dependencies:

```bash
cd frontend
npm install # or yarn install
```

### 2.3. Backend Setup (FastAPI RAG Chatbot)

Navigate to the backend directory, create a virtual environment, install dependencies, and configure environment variables.

```bash
cd backend
python -m venv venv
./venv/Scripts/activate # On Windows
# source venv/bin/activate # On macOS/Linux

pip install -r requirements.txt # (assuming requirements.txt will be created)

# Create a .env file in the 'backend' directory with the following:
# OPENAI_API_KEY="your_openai_api_key"
# QDRANT_HOST="your_qdrant_cloud_host"
# QDRANT_API_KEY="your_qdrant_cloud_api_key"
# NEON_DATABASE_URL="your_neon_postgres_connection_string"
```

### 2.4. Initial Content & Embeddings

Before running the chatbot, you'll need to:

1.  Populate Docusaurus `docs/` with your textbook content (Markdown files).
2.  Generate vector embeddings for this content and upload them to Qdrant. This step will likely involve a separate script within the `backend/` or `tools/` directory.

## 3. Running the Application

### 3.1. Start the Backend API

From the `backend` directory (with virtual environment activated):

```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### 3.2. Start the Frontend Development Server

From the `frontend` directory:

```bash
npm start # or yarn start
```

The Docusaurus textbook will be available at `http://localhost:3000`.

## 4. Interacting with Core Features

*   **Browse Textbook**: Navigate to `http://localhost:3000` in your browser and explore the content.
*   **Chatbot Interaction**: The embedded chatbot UI in Docusaurus will make requests to your FastAPI backend (`http://localhost:8000/chat/query`). Type questions or select text snippets to get answers.

## 5. Deployment

To deploy the Docusaurus site to GitHub Pages:

```bash
cd frontend
npm run deploy # or yarn deploy
```

(Ensure your `docusaurus.config.js` is correctly configured for GitHub Pages deployment.)