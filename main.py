from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="OpenAPI Backend Generator",
    version="0.1",
    description="Automatically generates a backend from OpenAPI specs with optional GPT-augmented logic."
)

# Allow CORS for testing/demo frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend Generator API is running."}
