# Multilingual Ticket Translator

An enterprise SaaS web application for multilingual support ticket management with AI-powered translation and response suggestions.

## Features

### Client Portal
- Submit tickets in any language
- Upload files (PDF, images, documents)
- Real-time ticket status tracking with color-coded badges
- View translated responses in native language

### Admin Dashboard
- KPI metrics overview
- FIFO ticket queue management
- AI-powered language detection and translation
- AI response suggestions
- Manual response with auto-translation

### AI Capabilities
- Automatic language detection (40+ languages)
- Real-time translation to English for admin review
- Response translation back to client's language
- AI-suggested responses using Ollama/LLM

## Tech Stack

- **Frontend**: React.js, React Router, Axios
- **Backend**: FastAPI, SQLAlchemy, SQLite
- **AI/Translation**: LangDetect, Deep Translator, Ollama
- **Deployment**: Docker, Docker Compose

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd multilingual-ticket-translator

# Start all services
docker-compose up -d

# Access the application
# Frontend: [localhost](http://localhost:3000)
# Backend API: [localhost](http://localhost:8000)
# API Docs: [localhost](http://localhost:8000/docs)