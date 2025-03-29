from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Post(Base):
    """博文表模型"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    images = Column(JSON, default=list)  # 存储图片URL列表
    tags = Column(JSON, default=list)    # 存储标签列表
    location = Column(String(100), nullable=True)
    cover_image = Column(String(255), nullable=True)  # 封面图URL
    likes_count = Column(Integer, default=0)
    
    # 关联关系
    user = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', user_id={self.user_id})>" 