from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import requests
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.models.database import get_db
from app.models.user import User
from app.schemas.user import WechatLoginRequest, Token, User as UserSchema
from app.config.settings import settings
from app.auth.service import wechat_login
from app.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/auth", tags=["auth"])

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/wechat-login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_wechat_session_key(code: str):
    """Get WeChat session key from code"""
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": settings.WECHAT_APPID,
        "secret": settings.WECHAT_SECRET,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

@router.post("/wechat-login", response_model=Token)
async def login_wechat(login_data: WechatLoginRequest, db: Session = Depends(get_db)):
    """
    微信小程序登录接口
    
    Args:
        login_data: 包含微信登录临时 code 的请求体
        db: 数据库会话
        
    Returns:
        访问令牌
        
    Raises:
        HTTPException: 如果登录失败
    """
    result = wechat_login(db, login_data)
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("message", "登录失败"),
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {
        "access_token": result.get("access_token"),
        "token_type": result.get("token_type"),
        "expires_in": result.get("expires_in"),
        "openid": result.get("openid")
    }

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    获取当前登录用户信息
    
    Args:
        current_user: 当前活跃用户
        
    Returns:
        用户信息
    """
    return current_user
