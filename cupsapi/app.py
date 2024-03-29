""" The main app """

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cupsapi.routers.default import DefaultRouter

app = FastAPI(
    title="cupsApi",
    description="A REST API for printing to a CUPS printer.",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(DefaultRouter().router, tags=["Default"])