from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging
from typing import Optional
from pydantic import BaseModel

from app.models.database import get_db
from app.auth.dependencies import get_current_user, get_current_active_user
from app.models.user import User
from app.services.assistant_service import AssistantService

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/assistant",
    tags=["Assistant"]
)

# 请求体模型
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

# 响应体模型
class ChatResponse(BaseModel):
    text: str
    session_id: Optional[str] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    与阿里百炼智能助手聊天
    
    Args:
        request: 聊天请求，包含用户消息和可选的会话ID
        db: 数据库会话
        current_user: 当前登录用户
        
    Returns:
        助手回复和会话ID
    """
    try:
        logger.info(f"用户 {current_user.id} 发送消息: {request.message}")
        
        # 创建助手服务
        assistant_service = AssistantService(db)
        
        # 调用阿里百炼API
        result = await assistant_service.chat_with_assistant(
            user_message=request.message,
            session_id=request.session_id
        )
        
        logger.info(f"获取到助手回复，会话ID: {result.get('session_id')}")
        
        return {
            "text": result.get("text", ""),
            "session_id": result.get("session_id", "")
        }
    
    except Exception as e:
        logger.error(f"与智能助手通信时发生错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"与智能助手通信失败: {str(e)}"
        ) 