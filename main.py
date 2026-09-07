import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Career Dekho MLM API")

# Enable CORS for Local & Live Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

@app.get("/")
def home():
    return {"message": "Career Dekho Pvt Ltd MLM API is Live!"}

@app.post("/api/v1/auth/login")
def login(data: LoginRequest):
    user_input = data.username_or_email.strip().lower()
    
    # Super Admin Check
    if user_input == "careerdekho247@gmail.com":
        return {
            "status": "SUCCESS",
            "role": "SUPER_ADMIN",
            "message": "Super Admin Authentication Successful"
        }
    
    # Member Check
    return {
        "status": "SUCCESS",
        "role": "MEMBER",
        "message": "Member Authentication Successful"
    }
