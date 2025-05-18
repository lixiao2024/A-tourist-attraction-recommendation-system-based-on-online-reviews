from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LikeBase(BaseModel):
    """点赞基础模型"""
    post_id: int
    user_id: int

class LikeCreate(BaseModel):
    """点赞创建模型"""
    pass  # 不需要额外字段，用户ID会从当前登录用户获取，post_id从URL获取

class LikeResponse(LikeBase):
    """点赞响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class LikeStatus(BaseModel):
    """点赞状态响应模型"""
    is_liked: bool
    likes_count: int 