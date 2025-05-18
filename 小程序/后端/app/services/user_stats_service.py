from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from typing import Dict, Any
from fastapi import HTTPException, status

from app.models.user import User
from app.models.like_model import PostLike
from app.models.post_model import Post
from app.models.follow import Follow
from app.models.favorite import Favorite

# 设置日志
logger = logging.getLogger(__name__)

class UserStatsService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_user_stats(self, user_id: int) -> Dict[str, int]:
        """
        获取用户统计数据
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict[str, int]: 包含用户统计数据的字典
            
        Raises:
            HTTPException: 当操作失败时抛出异常
        """
        try:
            # 检查用户是否存在
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="用户不存在"
                )
            
            # 1. 获取用户获赞数 - 用户发布的所有文章获得的点赞总数
            posts_by_user = self.db.query(Post).filter(Post.user_id == user_id).all()
            likes_received = sum(post.likes_count for post in posts_by_user) if posts_by_user else 0
            
            # 2. 获取用户粉丝数 - 关注该用户的用户数量
            fans_count = self.db.query(Follow).filter(Follow.followed_id == user_id).count()
            
            # 3. 获取用户关注数 - 该用户关注的用户数量
            follow_count = self.db.query(Follow).filter(Follow.follower_id == user_id).count()
            
            # 4. 获取用户收藏数 - 用户收藏的帖子数量
            favorites_count = self.db.query(Favorite).filter(Favorite.user_id == user_id).count()
            
            # 尝试从用户表中直接获取统计数据，如果有的话
            if user.likes_received is not None:
                likes_received = user.likes_received
                
            if user.fans_count is not None:
                fans_count = user.fans_count
                
            if user.follow_count is not None:
                follow_count = user.follow_count
                
            if user.favorites_count is not None:
                favorites_count = user.favorites_count
            
            # 返回统计数据
            return {
                "likes_received": likes_received,
                "fans_count": fans_count,
                "follow_count": follow_count,
                "favorites_count": favorites_count
            }
        
        except HTTPException:
            # 直接向上传递HTTP异常
            raise
        except SQLAlchemyError as e:
            logger.error(f"查询用户统计数据时数据库错误: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="服务器错误，查询用户统计数据失败"
            )
        except Exception as e:
            logger.error(f"获取用户统计数据时出错: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"获取用户统计数据失败: {str(e)}"
            )
            
    async def update_user_stats(self, user_id: int) -> Dict[str, int]:
        """
        更新用户统计数据到用户表
        
        Args:
            user_id: 用户ID
            
        Returns:
            Dict[str, int]: 更新后的用户统计数据
            
        Raises:
            HTTPException: 当操作失败时抛出异常
        """
        try:
            # 先获取最新的统计数据
            stats = await self.get_user_stats(user_id)
            
            # 更新用户表中的统计数据
            user = self.db.query(User).filter(User.id == user_id).first()
            if user:
                user.likes_received = stats["likes_received"]
                user.fans_count = stats["fans_count"]
                user.follow_count = stats["follow_count"]
                user.favorites_count = stats["favorites_count"]
                
                self.db.commit()
            
            return stats
        except Exception as e:
            self.db.rollback()
            logger.error(f"更新用户统计数据时出错: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"更新用户统计数据失败: {str(e)}"
            ) 