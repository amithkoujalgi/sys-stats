import logging

from fastapi import APIRouter
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = APIRouter()


class UserInfo(BaseModel):
    name: str


@router.get("/test")
def test():
    return [{"id": "x", "name": "y"}]


@router.post("/login")
def login(user_creds: UserInfo):
    return {"status": True, 'user': user_creds.name}


@router.get("/processes")
def test():
    return [{"id": 1, "name": "python"}, {"id": 2, "name": "java"}]
