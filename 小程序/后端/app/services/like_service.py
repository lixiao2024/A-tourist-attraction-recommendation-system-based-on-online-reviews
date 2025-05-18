from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging
from typing import Dict, Any, List

from app.models.like_model import PostLike
from app.models.post_model import Post
from app.models.user import User
from fastapi import HTTPException, status

# 设置日志
logger = logging.getLogger(__name__)

class LikeService:
    def __init__(self, db: Session):
        self.db = db
    
    async def toggle_like(self, post_id: int, current_user: User) -> Dict[str, Any]:
        """
        切换帖子点赞状态（点赞/取消点赞）
        
        Args:
            post_id: 帖子ID
            current_user: 当前用户对象
            
        Returns:
            Dict[str, Any]: 包含点赞状态和总点赞数的字典
            
        Raises:
            HTTPException: 当操作失败时抛出异常
        """
        try:
            # 检查帖子是否存在
            post = self.db.query(Post).filter(Post.id == post_id).first()
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="帖子不存在"
                )
            
            # 获取帖子作者信息
            post_author = self.db.query(User).filter(User.id == post.user_id).first()
            if not post_author:
                logger.error(f"帖子 {post_id} 的作者不存在，用户ID: {post.user_id}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"帖子 {post_id} 的作者不存在"
                )
                
            # 查询用户是否已对此帖子点赞
            existing_like = self.db.query(PostLike).filter(
                PostLike.post_id == post_id,
                PostLike.user_id == current_user.id
            ).first()
            
            is_liked = False
            
            # 如果已点赞，则取消点赞
            if existing_like:
                self.db.delete(existing_like)
                # 更新帖子点赞数
                post.likes_count = max(0, post.likes_count - 1)  # 确保不为负数
                
                # 更新帖子作者的获赞总数
                post_author.likes_received = max(0, post_author.likes_received - 1)  # 确保不为负数
                
                is_liked = False
                logger.info(f"用户 {current_user.id} 取消了对帖子 {post_id} 的点赞，作者 {post_author.id} 的获赞总数减1")
            # 否则，添加点赞
            else:
                new_like = PostLike(
                    post_id=post_id,
                    user_id=current_user.id
                )
                self.db.add(new_like)
                
                # 更新帖子点赞数
                post.likes_count += 1
                
                # 更新帖子作者的获赞总数
                post_author.likes_received += 1
                
                is_liked = True
                logger.info(f"用户 {current_user.id} 对帖子 {post_id} 点赞，作者 {post_author.id} 的获赞总数加1")
            
            self.db.commit()
            
            # 返回更新后的点赞状态和数量
            return {
                "is_liked": is_liked,
                "likes_count": post.likes_count
            }
        
        except HTTPException:
            # 直接向上传递HTTP异常
            raise
        except IntegrityError as e:
            self.db.rollback()
            logger.error(f"点赞操作出现完整性错误: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="点赞操作失败，请检查输入数据"
            )
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"点赞操作数据库错误: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="服务器错误，点赞操作失败"
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"点赞操作未预期错误: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"发生未知错误: {str(e)}"
            )
    
    async def get_like_status(self, post_id: int, current_user: User) -> Dict[str, Any]:
        """
        获取用户对指定帖子的点赞状态
        
        Args:
            post_id: 帖子ID
            current_user: 当前用户对象
            
        Returns:
            Dict[str, Any]: 包含点赞状态和总点赞数的字典
            
        Raises:
            HTTPException: 当操作失败时抛出异常
        """
        try:
            # 检查帖子是否存在
            post = self.db.query(Post).filter(Post.id == post_id).first()
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="帖子不存在"
                )
            
            # 查询用户是否已对此帖子点赞
            is_liked = self.db.query(PostLike).filter(
                PostLike.post_id == post_id,
                PostLike.user_id == current_user.id
            ).first() is not None
            
            # 返回点赞状态和数量
            return {
                "is_liked": is_liked,
                "likes_count": post.likes_count
            }
        
        except HTTPException:
            # 直接向上传递HTTP异常
            raise
        except Exception as e:
            logger.error(f"获取点赞状态时出错: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="获取点赞状态失败"
            )
            
    async def recalculate_user_likes(self, user_id: int = None) -> Dict[str, Any]:
        """
        重新计算用户的获赞总数
        
        Args:
            user_id: 用户ID，如果为None则重新计算所有用户的获赞总数
            
        Returns:
            Dict[str, Any]: 包含更新结果的字典
            
        Raises:
            HTTPException: 当操作失败时抛出异常
        """
        try:
            users_updated = 0
            
            # 如果指定了用户ID，则只更新该用户
            if user_id:
                user = self.db.query(User).filter(User.id == user_id).first()
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"用户 {user_id} 不存在"
                    )
                    
                users_to_update = [user]
            else:
                # 否则更新所有用户
                users_to_update = self.db.query(User).all()
            
            # 遍历需要更新的用户
            for user in users_to_update:
                # 查询用户的所有帖子
                posts = self.db.query(Post).filter(Post.user_id == user.id).all()
                
                # 计算所有帖子的点赞总数
                total_likes = sum(post.likes_count for post in posts)
                
                # 如果计算结果与当前值不同，则更新
                if user.likes_received != total_likes:
                    logger.info(f"用户 {user.id} 的获赞总数从 {user.likes_received} 更新为 {total_likes}")
                    user.likes_received = total_likes
                    users_updated += 1
            
            # 提交更改
            self.db.commit()
            
            return {
                "message": "获赞总数重新计算完成",
                "users_updated": users_updated,
                "total_users": len(users_to_update)
            }
                
        except HTTPException:
            # 直接向上传递HTTP异常
            raise
        except Exception as e:
            self.db.rollback()
            logger.error(f"重新计算用户获赞总数时出错: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"重新计算用户获赞总数失败: {str(e)}"
            ) 