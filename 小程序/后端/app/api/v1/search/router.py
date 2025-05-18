from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.schemas.post_schema import PostBrief
from app.models.database import get_db
from app.auth.dependencies import get_optional_current_user
from app.models.user import User
from app.services.search_service import SearchService

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/search",
    tags=["Search"]
)

@router.get("/posts", response_model=List[PostBrief])
async def search_posts(
    keyword: str = Query(..., min_length=1, description="搜索关键词"),
    skip: int = 0, 
    limit: int = 15,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    搜索博文
    
    - 参数:
        - keyword: 搜索关键词，必填参数
        - skip: 跳过的记录数，默认为0
        - limit: 返回的最大记录数，默认为15
    - 返回:
        - 匹配关键词的博文列表
    """
    try:
        search_service = SearchService(db)
        return await search_service.search_posts(
            keyword=keyword,
            skip=skip,
            limit=limit,
            current_user=current_user
        )
    except Exception as e:
        logger.error(f"搜索博文时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="搜索博文失败"
        ) 