# SHL Assessment Recommendation API

## Setup

```bash
git clone <repository-url>
cd SHL-Assessment-Agent

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Run:

```bash
uvicorn app.main:app
```

API:

- Health: `GET /health`
- Chat: `POST /chat`

Swagger:

```
http://127.0.0.1:8000/docs
```