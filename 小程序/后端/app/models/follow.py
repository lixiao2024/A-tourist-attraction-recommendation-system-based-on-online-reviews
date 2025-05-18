from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Follow(Base):
    """用户关注关系表模型"""
    __tablename__ = "user_follows"
    
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 关注者ID
    followed_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 被关注者ID
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 关联关系
    follower = relationship("User", foreign_keys=[follower_id], backref="following")
    followed = relationship("User", foreign_keys=[followed_id], backref="followers")
    
    # 确保一个用户不能重复关注同一个用户
    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id', name='unique_follower_followed'),
    )
    
    def __repr__(self):
        return f"<Follow(follower_id={self.follower_id}, followed_id={self.followed_id})>" 