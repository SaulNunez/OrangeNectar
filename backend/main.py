from fastapi import FastAPI

from routers import export, reddit

app = FastAPI(title="OrangeNectar")
app.include_router(reddit.router, prefix="/reddit", tags=["reddit"])
app.include_router(export.router, tags=["export"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
