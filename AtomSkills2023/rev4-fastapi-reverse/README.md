# FastAPI-Reverse

## Run

### Direct run

```#bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### In docker

```#bash
docker build -t fastapi-reverse .
docker run -v ./app.db:/app.db:rw fastapi-reverse
```

## Flag
`flag{17adbe8bd64d7b2bd1a08986d1fa526a}`

