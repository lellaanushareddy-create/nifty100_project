from fastapi import APIRouter

router = APIRouter()

@router.get("/screener")
def screener():
    return {"message": "Screener endpoint working"}