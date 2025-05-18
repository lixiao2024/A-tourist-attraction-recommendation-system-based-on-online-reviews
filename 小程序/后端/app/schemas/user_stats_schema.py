from pydantic import BaseModel
from typing import Optional

class UserStatsResponse(BaseModel):
    """用户统计数据响应模型"""
    likes_received: int = 0  # 获赞数
    fans_count: int = 0  # 粉丝数
    follow_count: int = 0  # 关注数
    favorites_count: int = 0  # 收藏数
    
    class Config:
        orm_mode = True 