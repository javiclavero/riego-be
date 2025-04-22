from fastapi import FastAPI
from app.routers import weather_router

app = FastAPI()
app.include_router(weather_router.router)

@app.get("/")
async def root():
    return {"message": "Backend de gestión de riegos"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)