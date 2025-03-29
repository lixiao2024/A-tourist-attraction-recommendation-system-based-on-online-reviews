from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class PostBase(BaseModel):
    """博文基础模型"""
    title: str = Field(min_length=1, max_length=50)  # 标题
    content: str = Field(min_length=2)              # 正文，最小长度改为2
    images: List[str] = []                           # 图片URL列表
    tags: List[str] = []                             # 标签如["美食","旅行"]

class PostCreate(PostBase):
    """创建博文的请求模型"""
    location: Optional[str] = None                   # 位置信息
    cover_image: Optional[str] = None                # 封面图URL

class PostResponse(PostBase):
    """博文响应模型"""
    id: int
    user_id: int
    created_at: datetime
    location: Optional[str] = None
    cover_image: Optional[str] = None
    likes_count: int = 0
    comments_count: int = 0

    class Config:
        orm_mode = True

class PostUpdate(BaseModel):
    """更新博文的请求模型"""
    title: Optional[str] = Field(None, min_length=1, max_length=50)
    content: Optional[str] = Field(None, min_length=10)
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
    cover_image: Optional[str] = None

class PostBrief(BaseModel):
    """简要博文信息模型"""
    id: int
    title: str
    cover_image: Optional[str] = None
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0
    
    class Config:
        orm_mode = True 