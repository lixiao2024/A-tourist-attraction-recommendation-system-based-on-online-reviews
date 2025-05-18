from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from app.models.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token
from app.config.settings import settings
from typing import Optional

# OAuth2 密码授权方案，用于获取 Bearer 令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/wechat-login", auto_error=False)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    根据 JWT 令牌获取当前用户
    
    Args:
        token: JWT 令牌
        db: 数据库会话
        
    Returns:
        当前用户
        
    Raises:
        HTTPException: 如果令牌无效或用户不存在
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的身份凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 解码 JWT 令牌
        payload = decode_access_token(token)
        openid: str = payload.get("sub")
        
        if openid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # 从数据库中获取用户
    user = db.query(User).filter(User.openid == openid).first()
    
    if user is None:
        raise credentials_exception
        
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        当前活跃用户
        
    Raises:
        HTTPException: 如果用户不活跃
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
        
    return current_user

async def get_optional_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    """
    根据JWT令牌获取当前用户，如果令牌无效或用户不存在则返回None
    
    Args:
        token: JWT令牌，可选
        db: 数据库会话
        
    Returns:
        当前用户，如果令牌无效或用户不存在则返回None
    """
    if not token:
        return None
    
    try:
        # 解码JWT令牌
        payload = decode_access_token(token)
        openid: str = payload.get("sub")
        
        if openid is None:
            return None
            
        # 从数据库中获取用户
        user = db.query(User).filter(User.openid == openid).first()
        
        return user
    except JWTError:
        return None
