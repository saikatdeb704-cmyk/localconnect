# LocalConnect API

FastAPI backend for LocalConnect.

## Setup

```bash
cd apps/api
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --reload
```

API docs: http://localhost:8000/docs

## Database

Run migrations:
```bash
alembic upgrade head
```

## Environment Variables

Create `.env`:
```
DATABASE_URL=postgresql://user:password@localhost/localconnect
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-key
```
