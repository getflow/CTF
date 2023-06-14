from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.post("/commit")
async def commit():
    pass


@app.get("/pull")
async def pull(name: str):
    pass


@app.post("/push")
async def push():
    pass


@app.get("/fetch")
async def fetch():
    pass


@app.get("/")
async def view():
    return HTMLResponse("""<html>
    <head>
    </head>
    <body>
    </body>
</html>""")
