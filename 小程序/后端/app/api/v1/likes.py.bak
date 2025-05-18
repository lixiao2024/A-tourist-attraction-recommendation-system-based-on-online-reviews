from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

from app.schemas.like_schema import LikeStatus
from app.models.like_model import PostLike
from app.models.post_model import Post
from app.models.database import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/posts",
    tags=["Likes"]
)

@router.post("/{post_id}/likes", response_model=LikeStatus)
async def toggle_like(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    切换帖子点赞状态（点赞/取消点赞）
    
    - 参数:
        - post_id: 帖子ID
    - 返回:
        - 点赞状态和总点赞数
    """
    try:
        # 检查帖子是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # 查询用户是否已对此帖子点赞
        existing_like = db.query(PostLike).filter(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id
        ).first()
        
        is_liked = False
        
        # 如果已点赞，则取消点赞
        if existing_like:
            db.delete(existing_like)
            post.likes_count = max(0, post.likes_count - 1)  # 确保不为负数
            is_liked = False
        # 否则，添加点赞
        else:
            new_like = PostLike(
                post_id=post_id,
                user_id=current_user.id
            )
            db.add(new_like)
            post.likes_count += 1
            is_liked = True
        
        db.commit()
        
        # 返回更新后的点赞状态和数量
        return {
            "is_liked": is_liked,
            "likes_count": post.likes_count
        }
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"点赞操作出现完整性错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="点赞操作失败，请检查输入数据"
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"点赞操作数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器错误，点赞操作失败"
        )
    except Exception as e:
        db.rollback()
        logger.error(f"点赞操作未预期错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发生未知错误: {str(e)}"
        )

@router.get("/{post_id}/likes/status", response_model=LikeStatus)
async def get_like_status(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户对指定帖子的点赞状态
    
    - 参数:
        - post_id: 帖子ID
    - 返回:
        - 点赞状态和总点赞数
    """
    try:
        # A.检查帖子是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="帖子不存在"
            )
        
        # B.查询用户是否已对此帖子点赞
        is_liked = db.query(PostLike).filter(
            PostLike.post_id == post_id,
            PostLike.user_id == current_user.id
        ).first() is not None
        
        # C.返回点赞状态和数量
        return {
            "is_liked": is_liked,
            "likes_count": post.likes_count
        }
    
    except Exception as e:
        logger.error(f"获取点赞状态时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取点赞状态失败"
        ) 