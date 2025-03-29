from sqlalchemy.orm import Session
from datetime import timedelta
from app.models.user import User
from app.schemas.user import UserCreate, WechatLoginRequest
from app.utils.wechat import get_session_key
from app.utils.security import create_access_token
from app.config.settings import settings
from typing import Dict, Any

def wechat_login(db: Session, login_data: WechatLoginRequest) -> Dict[str, Any]:
    """
    微信小程序登录流程
    
    Args:
        db: 数据库会话
        login_data: 登录请求数据，包含微信临时 code 和可选的用户信息
        
    Returns:
        登录结果，包含 token 或错误信息
    """
    # 调用微信 API 获取 session_key 和 openid
    wx_result = get_session_key(login_data.code)
    
    if not wx_result.get("success"):
        return {
            "success": False,
            "message": wx_result.get("message", "微信登录失败"),
            "error_code": wx_result.get("error_code", -1)
        }
    
    openid = wx_result.get("openid")
    session_key = wx_result.get("session_key")
    unionid = wx_result.get("unionid")
    
    # 根据 openid 查找用户
    user = db.query(User).filter(User.openid == openid).first()
    
    # 如果用户不存在，创建新用户
    if not user:
        user = User(
            openid=openid,
            session_key=session_key,
            unionid=unionid
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        # 更新 session_key
        user.session_key = session_key
        db.commit()
        db.refresh(user)
    
    # 如果请求中包含用户信息，则更新用户资料
    if login_data.user_info:
        update_user_info(db, user, login_data.user_info)
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.openid}, 
        expires_delta=access_token_expires
    )
    
    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "user_id": user.id,
        "openid": user.openid
    }

def update_user_info(db: Session, user: User, user_info: Dict[str, Any]) -> User:
    """
    更新用户信息
    
    Args:
        db: 数据库会话
        user: 用户实例
        user_info: 用户信息字典
        
    Returns:
        更新后的用户实例
    """
    if "nickName" in user_info:
        user.nickname = user_info.get("nickName")
    if "avatarUrl" in user_info:
        user.avatar_url = user_info.get("avatarUrl")
    if "gender" in user_info:
        user.gender = user_info.get("gender")
    if "country" in user_info:
        user.country = user_info.get("country")
    if "province" in user_info:
        user.province = user_info.get("province")
    if "city" in user_info:
        user.city = user_info.get("city")
    if "language" in user_info:
        user.language = user_info.get("language")
    
    db.commit()
    db.refresh(user)
    return user
