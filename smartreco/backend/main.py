# Placeholder for FastAPI app entry point

from fastapi import FastAPI

app = FastAPI()

# Import and include routers here
# from api.routes import router
# app.include_router(router)

@app.get("/")
def root():
    return {"message": "SmartReco backend is running."}
