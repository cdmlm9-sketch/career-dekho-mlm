import os
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) # SUPER_ADMIN or MEMBER

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Career Dekho MLM API")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

@app.get("/")
def home():
    return {"message": "Career Dekho Pvt Ltd MLM API is Live!"}

@app.post("/api/v1/auth/login")
def login(data: LoginRequest):
    # Unified Login Logic
    if data.username_or_email == "careerdekho247@gmail.com":
        return {"status": "SUCCESS", "role": "SUPER_ADMIN", "redirect": "/admin/control-center"}
    return {"status": "SUCCESS", "role": "MEMBER", "redirect": "/member/dashboard"}
