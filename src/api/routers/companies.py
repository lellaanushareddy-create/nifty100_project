from fastapi import APIRouter

router = APIRouter(tags=["Companies"])

@router.get("/companies")
def get_companies():
    return {
        "status": "success",
        "message": "Companies endpoint working"
    }