from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from app.schemas.user_stats_schema import UserStatsResponse
from app.models.database import get_db
from app.auth.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.services.user_stats_service import UserStatsService

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/users",
    tags=["UserStats"]
)

@router.get("/me/stats", response_model=UserStatsResponse)
async def get_my_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前登录用户的统计数据
    
    - 返回:
        - 用户统计数据，包括获赞数、粉丝数、关注数和收藏数
    """
    try:
        user_stats_service = UserStatsService(db)
        return await user_stats_service.get_user_stats(current_user.id)
    except Exception as e:
        logger.error(f"获取用户统计数据时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计数据失败: {str(e)}"
        )

@router.get("/{user_id}/stats", response_model=UserStatsResponse)
async def get_user_stats(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_optional_current_user)
):
    """
    获取指定用户的统计数据
    
    - 参数:
        - user_id: 用户ID
    - 返回:
        - 用户统计数据，包括获赞数、粉丝数、关注数和收藏数
    """
    try:
        user_stats_service = UserStatsService(db)
        return await user_stats_service.get_user_stats(user_id)
    except Exception as e:
        logger.error(f"获取用户{user_id}的统计数据时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计数据失败: {str(e)}"
        ) 