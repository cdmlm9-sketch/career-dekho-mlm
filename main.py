import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String, unique=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    mobile = Column(String)
    role = Column(String)
    left_count = Column(Integer, default=0)
    right_count = Column(Integer, default=0)
    pairs_today = Column(Integer, default=0)
    total_earnings = Column(Float, default=0.0)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Career Dekho MLM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    username_or_email: str
    password: str

@app.post("/api/v1/auth/login")
def login(data: LoginRequest):
    user_input = data.username_or_email.strip().lower()
    
    if user_input == "careerdekho247@gmail.com":
        return {
            "status": "SUCCESS",
            "role": "SUPER_ADMIN",
            "user": {"name": "Super Admin", "email": "careerdekho247@gmail.com"}
        }
    
    return {
        "status": "SUCCESS",
        "role": "MEMBER",
        "user": {
            "member_id": "CD10023",
            "name": "Rahul Sharma",
            "mobile": user_input,
            "left_count": 12,
            "right_count": 9,
            "pairs_today": 9,
            "max_pairs": 9,
            "gross_payout": 7200,
            "tds_deduction": 360,
            "admin_fee": 360,
            "net_payout": 6480
        }
    }
