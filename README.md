# backend-hackathon-2026

Sales Objection Handler API - AI-powered B2B SaaS objection response system

## Setup

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Environment variables are already configured in `.env`

3. Run the application:
```bash
cd backend
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /objections/` - Submit a sales objection and get AI response
- `GET /objections/` - List all objections
- `GET /objections/{id}` - Get specific objection by ID
- `GET /health` - Health check

## Example Request

```bash
curl -X POST "http://localhost:8000/objections/" \
  -H "Content-Type: application/json" \
  -d '{"objection_text": "Your product is too expensive"}'
```

## Database

SQLite database (`objections.db`) is automatically created on first run.
