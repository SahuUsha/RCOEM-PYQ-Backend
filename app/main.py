from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import upload, search, filter_routes, auth_routes, contact_routes
from app.services.qdrant_service import create_collection

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development, allow all. You can restrict this later.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    create_collection()

app.include_router(auth_routes.router, tags=["Authentication"])
app.include_router(upload.router, tags=["Upload"])
app.include_router(search.router, tags=["Search"])
app.include_router(filter_routes.router, tags=["Filters"])
app.include_router(contact_routes.router, tags=["Contact"])

