from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from datetime import datetime
import os

#创建数据库引擎
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

#创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#创建基类
Base  = declarative_base()

#用户模型类
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class EmailCode(Base):
    __tablename__ = "email_codes"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), nullable=False, index=True)
    code = Column(String(6), nullable=False)
    expire_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))

#创建所有表
def create_tables():
    Base.metadata.create_all(bind=engine)

#获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

