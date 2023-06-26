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

## Hints

- Find out some ciphered text in sqlite database. Check the fields, they may contain hints

## Solution

- The source code doesn't contain any bugs but there was some sometimes ago. Yo can see that in older versions commit hash calculation was a little buggy(see the commented code). That's why commit hashes in database are incorrect
- Write the function to recalculate commit hashes and fix database records
- Call `head` method
- Call `flag` method with the data returned in previous step

