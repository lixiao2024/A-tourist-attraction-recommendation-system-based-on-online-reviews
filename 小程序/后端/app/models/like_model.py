from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class PostLike(Base):
    """帖子点赞表模型"""
    __tablename__ = "post_likes"
    
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 关联关系
    post = relationship("Post", backref="likes")
    user = relationship("User", backref="post_likes")
    
    # 确保一个用户只能给一个帖子点一次赞
    __table_args__ = (
        UniqueConstraint('post_id', 'user_id', name='unique_post_user_like'),
    )
    
    def __repr__(self):
        return f"<PostLike(post_id={self.post_id}, user_id={self.user_id})>" 