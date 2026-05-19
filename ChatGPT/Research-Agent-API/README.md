# AI Research Agent API

A simple, production-ready AI Research Agent API built with **FastAPI**, **Google Generative AI**, and **SQLAlchemy** for local development.

## Features

- **Smart Research Agent**: Uses **Google Gemini** (default) to perform deep research on any topic.
- **Agentic Workflows**: Automates complex tasks using intelligent agents.
- **Persistence**: Saves research history and outputs to a PostgreSQL database.
- **Async API**: Built with FastAPI for high-performance asynchronous operations.
- **Rate Limiting**: Built-in rate limiting to respect API quotas.

## 📁 Project Structure

```
research-agent/
├── agent/
│   ├── planner.py            # Research planning logic
│   ├── research_worker.py    # AI research execution
│   └── tools.py              # AI tools and utilities
├── config/
│   ├── settings.py           # Environment configuration
│   └── database.py           # Database connection
├── models/
│   ├── base.py               # Base SQLAlchemy models
│   └── research_session.py   # Research history model
├── schemas/
│   ├── requests.py           # Pydantic request models
│   ├── responses.py          # Pydantic response models
│   └── agent.py              # Agent configuration schemas
├── services/
│   ├── ai_service.py         # AI model interactions
│   └── rate_limiter.py       # Rate limiting logic
├── api/
│   ├── api_v1/
│   │   ├── endpoints/
│   │   │   └── research.py   # Research API endpoints
│   │   └── routes.py         # API router
│   └── server.py             # FastAPI application entry point
├── main.py                   # Application entry point
└── requirements.txt          # Dependencies
```

## 🚀 Getting Started

### Prerequisites

- **Python 3.12+**
- **PostgreSQL** (or Docker)
- **Google Generative AI API Key**

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Research-Agent-API
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Copy the sample `.env` file and fill in your credentials:
   ```bash
   cp .env.example .env
   ```
   
   Required variables in `.env`:
   ```env
   GOOGLE_API_KEY=your_google_key_here
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```

### Database Setup

Ensure your PostgreSQL database is running and the `DATABASE_URL` in your `.env` file points to it.

### Running the Server

Start the development server:

```bash
uvicorn api.server:app --reload --host [IP_ADDRESS] --port 8000
```

The API will be available at `http://localhost:8000`.

## 🏗️ API Endpoints

### Create Research Session

Starts a new research session with an intelligent agent.

**Endpoint**: `POST /api/v1/research/session`

**Request Body**:
```json
{
    "topic": "The impact of AI on job markets",
    "description": "Research current trends and future projections",
    "session_type": "deep_research"
}
```

**Response**:
```json
{
    "id": "c24c998e-b7c3-4b4a-ad4b-70d6235b26b5",
    "topic": "The impact of AI on job markets",
    "status": "IN_PROGRESS",
    "created_at": "2024-01-15T10:30:00.000Z",
    "updated_at": "2024-01-15T10:30:00.000Z",
    "research_output": null
}
```

### Get Research Session

Retrieves the status and output of a specific research session.

**Endpoint**: `GET /api/v1/research/session/{session_id}`

**Response**:
```json
{
    "id": "c24c998e-b7c3-4b4a-ad4b-70d6235b26b5",
    "topic": "The impact of AI on job markets",
    "status": "COMPLETED",
    "created_at": "2024-01-15T10:30:00.000Z",
    "updated_at": "2024-01-15T10:30:00.000Z",
    "research_output": {
        "summary": "AI is transforming job markets through automation...",
        "key_findings": [...],
        "sources": [...],
        "timestamp": "2024-01-15T10:35:00.000Z"
    }
}
```

## 🛠️ Usage Examples

### Python Example

```python
import requests

base_url = "http://localhost:8000/api/v1"

# Start research
session_data = {
    "topic": "Quantum Computing Explained",
    "description": "Explain quantum computing in simple terms",
    "session_type": "deep_research"
}

response = requests.post(f"{base_url}/research/session", json=session_data)
session_id = response.json()["id"]
print(f"Research session started: {session_id}")

# Get results
result = requests.get(f"{base_url}/research/session/{session_id}").json()
print(result["research_output"]["summary"])
```

### Shell Example

```bash
# Start research
curl -X POST "http://localhost:8000/api/v1/research/session" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Machine Learning Basics", "description": "Intro to ML", "session_type": "quick_summary"}'

# Get results
curl -X GET "http://localhost:8000/api/v1/research/session/{session_id}"
```

## 🗄️ Database Schema

The database uses SQLAlchemy with PostgreSQL to store research sessions:

```sql
CREATE TABLE research_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    topic VARCHAR(255) NOT NULL,
    description TEXT,
    session_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'IN_PROGRESS',
    research_output JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🛡️ Security

- **Environment Variables**: All sensitive configuration is managed through environment variables in `.env`.
- **Rate Limiting**: The `rate_limiter.py` module implements a sliding window algorithm to prevent abuse.
- **Input Validation**: Pydantic schemas validate all incoming request data.

## ⚙️ Configuration

Customize the application behavior by modifying the following environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Generative AI API key | Required |
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `MAX_REQUESTS_PER_MINUTE` | Rate limiting requests per minute | 10 |
| `WINDOW_SIZE_SECONDS` | Rate limiting window size | 60 |
| `AI_MODEL` | Google model to use | `gemini-2.5-flash` |
| `REQUEST_TIMEOUT` | AI request timeout in seconds | 30 |