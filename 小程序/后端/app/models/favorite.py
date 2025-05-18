from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Favorite(Base):
    """用户收藏表模型"""
    __tablename__ = "user_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 关联关系
    user = relationship("User", backref="favorites")
    post = relationship("Post", backref="favorited_by")
    
    # 确保一个用户不能重复收藏同一个帖子
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='unique_user_post_favorite'),
    )
    
    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, post_id={self.post_id})>" 