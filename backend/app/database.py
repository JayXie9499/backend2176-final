import os
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

if not os.path.exists("./data"):
	os.mkdir("./data")

engine = create_engine(
	"sqlite:///./data/db.sqlite", connect_args={"check_same_thread": False}
)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, _):
	cursor = dbapi_connection.cursor()
	cursor.execute("PRAGMA journal_mode=WAL")
	cursor.execute("PRAGMA foreign_keys=ON")
	cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
