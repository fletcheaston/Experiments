from fastapi import FastAPI

from src import router

PREFIX = "/experiments/advent-of-code-2023"

app = FastAPI(
    docs_url=f"{PREFIX}/docs",
    redoc_url=f"{PREFIX}/redoc",
)

app.include_router(router, prefix=PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="app:app",
        reload=True,
        proxy_headers=True,
        port=8001,
    )
