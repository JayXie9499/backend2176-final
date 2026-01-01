from typing import Any
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from ..schemas import UserCreate, UserLogin
from ..database import get_db
from ..models import User
from ..security import hash_password, verify_password, generate_jwt_token
from ..dependencies import auth_dependency

router = APIRouter()


@router.post("/login")
async def user_login(
	data: UserLogin, response: Response, db: Session = Depends(get_db)
):
	data_dict = data.model_dump()
	username = data_dict["username"]
	password = data_dict["password"]
	user = db.query(User).where(User.username == username).first()
	correct_password = verify_password(password, user.hashed_pwd) if user else False  # type: ignore
	if not user or not correct_password:
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return {"message": "Invalid username or password"}

	token_exp = datetime.now(timezone.utc) + timedelta(hours=1)
	jwt_claims = {"sub": user.id, "exp": token_exp}
	token = generate_jwt_token(jwt_claims)
	if not token:
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return {"message": "An error occurred while generating JWT token"}

	response.set_cookie(
		"jwt_token", token, secure=True, httponly=True, expires=token_exp
	)
	return {"message": "Successfully generated JWT token"}


@router.post("/register")
async def user_register(
	data: UserCreate, response: Response, db: Session = Depends(get_db)
):
	data_dict = data.model_dump()
	username = data_dict["username"]
	password = data_dict["password"]
	existing_user = db.query(User).where(User.username == username).first()
	if existing_user:
		response.status_code = status.HTTP_400_BAD_REQUEST
		return {"message": "Username already taken"}

	hashed_pwd = hash_password(password)
	db.add(User(username=username, hashed_pwd=hashed_pwd))
	db.commit()

	return {"message": "Successfully registered"}


@router.post("/logout")
async def user_logout(response: Response, _: dict[str, Any] = Depends(auth_dependency)):
	response.delete_cookie(key="jwt_token")
	return {"message": "Successfully logged out"}
