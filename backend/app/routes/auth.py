from typing import Any
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from ..schemas import UserCreate
from ..database import get_db
from ..models import User
from ..security import hash_password
from ..dependencies import auth_dependency

router = APIRouter()


@router.post("/register")
async def user_register(
	data: UserCreate, response: Response, db: Session = Depends(get_db)
):
	data_dict = data.model_dump()
	username = data_dict["username"]
	password = data_dict["password"]
	existing_user = db.query(User).where(User.name == username).first()
	if existing_user:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return {"message": "Username already taken"}

	hashed_pwd = hash_password(password)
	db.add(User(name=username, hashed_pwd=hashed_pwd))
	db.commit()

	return {"message": "Successfully registered"}


@router.post("/logout")
async def user_logout(response: Response, _: dict[str, Any] = Depends(auth_dependency)):
	response.delete_cookie(key="jwt_token")
	return {"message": "Successfully logged out"}
