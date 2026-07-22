from fastapi import APIRouter

router = APIRouter()

@router.get("/peers")
def peers():
    return {"message": "Peers endpoint working"}