import bcrypt
from jose import jwt
from .config import config


def hash_password(password: str):
	return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_jwt_token(token: str):
	try:
		payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
		return payload
	except:
		return None


def verify_password(password: str, hash: str):
	pwd_bytes = password.encode("utf-8")
	hash_bytes = hash.encode("utf-8")
	return bcrypt.checkpw(pwd_bytes, hash_bytes)


def generate_jwt_token(data: dict):
	try:
		return jwt.encode(data, config.JWT_SECRET, algorithm="HS256")
	except:
		return None
