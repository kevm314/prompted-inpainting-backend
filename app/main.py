import os

if __name__ == "__main__":
    # for dev purposes only
    from dotenv import load_dotenv
    import pathlib
    load_dotenv(dotenv_path=pathlib.Path('./dev.env'))

import uvicorn
from fastapi import FastAPI
from mangum import Mangum
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from core.config import settings



app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
    root_path=os.environ["API_ROOT_URL"]
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": "active"}

handler = Mangum(app)

if __name__ == "__main__":
    # for dev purposes only
    uvicorn.run(app, host="0.0.0.0", port=8000)