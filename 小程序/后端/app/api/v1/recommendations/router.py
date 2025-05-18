from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.schemas.post_schema import PostBrief
from app.models.database import get_db
from app.auth.dependencies import get_optional_current_user
from app.models.user import User
from app.services.recommendation_service import RecommendationService

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/recommendations",
    tags=["Recommendations"]
)

@router.get("/posts", response_model=List[PostBrief])
async def get_recommended_posts(
    skip: int = 0, 
    limit: int = 15,
    is_refresh: Optional[bool] = False,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    获取推荐的博文列表
    
    - 参数:
        - skip: 跳过的记录数，默认为0
        - limit: 返回的最大记录数，默认为15
        - is_refresh: 是否为刷新操作
    - 返回:
        - 博文简要信息列表，按推荐得分排序
    """
    try:
        recommendation_service = RecommendationService(db)
        return await recommendation_service.get_recommended_posts(
            skip=skip,
            limit=limit,
            is_refresh=is_refresh,
            current_user=current_user
        )
    except Exception as e:
        logger.error(f"获取推荐博文列表时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取推荐博文失败"
        ) 