from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

# 基础用户信息
class UserBase(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    gender: Optional[int] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    language: Optional[str] = None

# 微信登录请求
class WechatLoginRequest(BaseModel):
    code: str
    user_info: Optional[Dict[str, Any]] = None

# 创建用户请求
class UserCreate(UserBase):
    openid: str
    session_key: str
    unionid: Optional[str] = None

# 登录响应
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    openid: str

# 用户响应
class User(UserBase):
    id: int
    openid: str
    created_at: datetime
    
    class Config:
        from_attributes = True
