from fastapi import APIRouter

router = APIRouter()

@router.get("/sectors")
def sectors():
    return {"message": "Sectors endpoint working"}