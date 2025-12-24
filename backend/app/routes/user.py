from typing import Any
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..database import get_db
from ..models import User
from ..dependencies import auth_dependency

router = APIRouter()


@router.get("/me")
async def read_current_user(
	response: Response,
	jwt_payload: dict[str, Any] = Depends(auth_dependency),
	db: Session = Depends(get_db),
):
	try:
		user = db.query(User).filter(User.id == jwt_payload["user_id"]).first()
		if not user:
			response.status_code = status.HTTP_404_NOT_FOUND
			return {"message": "User not found"}

		return {"message": "Successfully fetched user data", "data": user}
	except SQLAlchemyError as e:
		print(e)
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return {"message": "An error occurred while fetching user data"}


@router.get("/{id}")
async def read_user_by_id(id: int, response: Response, db: Session = Depends(get_db)):
	try:
		user = db.query(User).filter(User.id == id).first()
		if not user:
			response.status_code = status.HTTP_404_NOT_FOUND
			return {"message": "User not found"}

		return {"message": "Successfully fetched user data", "data": user}
	except SQLAlchemyError as e:
		print(e)
		response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
		return {"message": "An error occurred while fetching user data"}
