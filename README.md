# Physical AI & Humanoid Robotics Textbook Platform

**A Next-Generation Adaptive Learning Platform for Robotics Education.**

This project is a sophisticated, spec-driven web application that combines a comprehensive textbook with advanced AI Agents to provide a personalized, interactive, and multilingual learning experience.

## 🌟 Key Features

### 1. 📘 Interactive Textbook
Built with **Docusaurus**, offering a fast, SEO-friendly, and beautiful reading experience.
- Mobile-responsive design
- Dark mode support
- Rich typography and code highlighting

### 2. 🤖 RAG Chatbot (User Story 2)
An integrated AI Assistant that answers student questions using **Retrieval-Augmented Generation (RAG)**.
- **Context-Aware:** Uses vector search (Qdrant) to find relevant textbook sections.
- **Accurate:** Grounded in the textbook content to prevent hallucinations.
- **Glassmorphism UI:** Premium, floating interaction window.

### 3. 👤 Intelligent Personalization (User Story 3)
The platform adapts to **WHO** you are.
- **Signup/Login:** Secure authentication (JWT + Bcrypt).
- **Background Profiling:** Users define their background (e.g., Software Engineer, Hardware Tech, Python Dev).
- **AI Adaptation:** The "Personalize for Me" feature rewrites technical content to match your background (e.g., explaining C++ concepts using Python analogies).

### 4. 🌍 Real-time Localization (User Story 4)
Breaking language barriers in technical education.
- **AI Translation:** Instantly translate complex technical content into **Urdu** (and other languages) while preserving technical accuracy.
- **RTL Support:** Full support for Right-to-Left scripts.

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React (Docusaurus)
- **Styling:** CSS Modules, Glassmorphism design
- **State:** React Context API

### Backend
- **API:** Python FastAPI (Async)
- **database:** Neon Serverless Postgres (User Data)
- **Vector DB:** Qdrant Cloud (Textbook Embeddings)
- **AI:** OpenAI GPT-3.5/4 (RAG, Personalization, Translation)
- **Auth:** JWT, Passlib, Bcrypt

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- OpenAI API Key
- Qdrant API Key & URL
- Neon Postgres Connection String

### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in `backend/`:
```env
OPENAI_API_KEY=sk-...
QDRANT_HOST=...
QDRANT_API_KEY=...
NEON_DATABASE_URL=postgresql://...
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Run the server:
```bash
uvicorn src.main:app --reload
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```
Visit `http://localhost:3000`.

---

## 🏗️ Architecture

The project follows a **Spec-Driven Development (SDD)** approach.
- **`specs/`**: Contains detailed requirements and tasks.
- **`history/prompts/`**: Records of all AI interactions and implementation steps.
- **`tools/`**: Automation scripts (e.g., Embedding Generator).

---

## 🧪 Testing

```bash
# Backend Tests
cd backend
pytest

# Frontend Tests
cd frontend
npm test
```
