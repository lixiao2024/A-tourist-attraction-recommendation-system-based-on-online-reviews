from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.schemas.like_schema import LikeStatus
from app.models.database import get_db
from app.auth.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.services.like_service import LikeService

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
        like_service = LikeService(db)
        return await like_service.toggle_like(post_id, current_user)
    except Exception as e:
        logger.error(f"点赞操作失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"点赞操作失败: {str(e)}"
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
        like_service = LikeService(db)
        return await like_service.get_like_status(post_id, current_user)
    except Exception as e:
        logger.error(f"获取点赞状态时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取点赞状态失败: {str(e)}"
        )
        
# 添加用户刷新获赞数的路由
user_router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)

@user_router.post("/me/refresh-likes", status_code=status.HTTP_200_OK)
async def refresh_my_likes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    重新计算当前用户的获赞总数，通常在"我的"页面刷新时调用
    
    返回:
        - 更新结果信息
    """
    try:
        like_service = LikeService(db)
        return await like_service.recalculate_user_likes(current_user.id)
    except Exception as e:
        logger.error(f"刷新用户获赞总数失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"刷新获赞总数失败: {str(e)}"
        ) 