from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "¡Hola desde el backend de gestión de riegos!"}

# ... otras rutas y lógica ...