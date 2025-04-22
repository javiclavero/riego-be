from fastapi import APIRouter

router = APIRouter(prefix="/riegos", tags=["riegos"])

@router.get("/")
async def obtener_riegos():
    return {"riegos": []}  # Por ahora, devuelve una lista vacía