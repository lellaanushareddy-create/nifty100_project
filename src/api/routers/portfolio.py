from fastapi import APIRouter

router = APIRouter()

@router.get("/portfolio")
def portfolio():
    return {"message": "Portfolio endpoint working"}