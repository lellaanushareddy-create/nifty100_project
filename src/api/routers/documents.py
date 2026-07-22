from fastapi import APIRouter

router = APIRouter()

@router.get("/documents")
def documents():
    return {"message": "Documents endpoint working"}