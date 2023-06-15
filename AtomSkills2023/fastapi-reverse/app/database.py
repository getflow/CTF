import os

from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, Session


DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
session = sessionmaker(engine, class_=Session, expire_on_commit=False)
