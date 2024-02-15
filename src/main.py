"""Entrypoint file for the affils service.

Set up API routes.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """A cheeky hello world route."""
    return {"message": "Look on my Affiliations Service, ye Mighty, and despair!"}
