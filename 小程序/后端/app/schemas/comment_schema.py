from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# 创建评论请求模型
class CommentCreate(BaseModel):
    content: str = Field(..., description="评论内容")
    parent_id: Optional[int] = Field(None, description="父评论ID（回复评论时使用）")

# 用户基本信息
class UserBasic(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: Optional[str] = None
    
    class Config:
        orm_mode = True

# 评论响应模型
class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    parent_id: Optional[int] = None
    content: str
    created_at: datetime
    user: Optional[UserBasic] = None
    
    class Config:
        orm_mode = True
        
# 带回复的评论响应模型（用于嵌套回复）
class CommentWithReplies(CommentResponse):
    replies: Optional[List['CommentResponse']] = []
    
    class Config:
        orm_mode = True 