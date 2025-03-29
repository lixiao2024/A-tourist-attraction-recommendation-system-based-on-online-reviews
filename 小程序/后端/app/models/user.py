from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(100), unique=True, index=True)
    session_key = Column(String(100))
    unionid = Column(String(100), nullable=True)
    
    # 用户基本信息
    nickname = Column(String(100), nullable=True)
    avatar_url = Column(Text, nullable=True)
    gender = Column(Integer, nullable=True)  # 性别 0:未知 1:男 2:女
    country = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    city = Column(String(50), nullable=True)
    language = Column(String(20), nullable=True)
    
    # 记录创建时间
    created_at = Column(DateTime, server_default=func.now())
    
    # 是否活跃
    is_active = Column(Boolean, default=True)
    
    # 关联关系
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
