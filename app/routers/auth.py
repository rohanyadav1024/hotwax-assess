from fastapi import APIRouter, status, Depends, HTTPException, Request
from ..oauth import create_access_token

router = APIRouter(prefix='/authentication', tags=["Authentication"])


@router.get("/token", status_code=status.HTTP_201_CREATED)
def get_token(request: Request):
    token = create_access_token(data={"user_id": "user123"})
    return {"access_token": token}