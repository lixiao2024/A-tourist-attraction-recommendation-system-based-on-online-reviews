from fastapi import FastAPI, HTTPException, status, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session, joinedload
import os
import uuid
import logging
import shutil
from sqlalchemy.exc import SQLAlchemyError
from fastapi.security import OAuth2PasswordBearer
import httpx  # 添加httpx库用于异步HTTP请求
import traceback
import json
import math

# 导入应用配置和数据库模型
from app.config.settings import settings
from app.models.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.post_model import Post
from app.models.comment import Comment  # 导入评论模型
from app.schemas.post_schema import PostCreate, PostResponse, PostBrief
from app.schemas.comment_schema import CommentCreate, CommentResponse  # 导入评论Schema
from app.auth.dependencies import get_optional_current_user, get_current_user
from app.utils.sentiment_analysis import analyze_sentiment  # 导入情感分析函数

# 导入推荐模块路由
from app.api.v1.recommendations.router import router as recommendations_router

# 导入点赞模块路由
from app.api.v1.likes.router import router as likes_router, user_router as likes_user_router

# 导入用户统计模块路由
from app.api.v1.user_stats.router import router as user_stats_router

# 导入用户手机号绑定模块路由
from app.api.v1.user.router import router as user_phone_router

# 导入智能助手模块路由
from app.api.v1.assistant.router import router as assistant_router

# 导入搜索模块路由
from app.api.v1.search.router import router as search_router

# 导入调度器模块
from app.scheduler import setup_scheduler, shutdown_scheduler

# 自定义OAuth2方案，使用正确的token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/wechat-login", auto_error=False)

# 设置日志
logger = logging.getLogger(__name__)

# 确保数据库表已创建
Base.metadata.create_all(bind=engine)

# 确保上传目录存在
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

# 使用配置中的设置
WECHAT_APPID = settings.WECHAT_APPID
WECHAT_SECRET = settings.WECHAT_SECRET
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# 设置常量
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# 从环境变量中读取Ollama API地址，如果未设置则使用默认值
OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
MODEL_NAME = "shiroi/qwen7b-q4:latest"

print(f"使用Ollama API地址: {OLLAMA_API_BASE}")

# Initialize FastAPI app
app = FastAPI(
    title="旅游景点智能推荐系统API",
    description="基于在线评论的旅游景点智能推荐系统后端API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册静态文件服务
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# 注册推荐模块路由
app.include_router(recommendations_router)

# 注册点赞模块路由
app.include_router(likes_router)
app.include_router(likes_user_router)

# 注册用户统计模块路由
app.include_router(user_stats_router)

# 注册用户手机号绑定模块路由
app.include_router(user_phone_router)

# 注册智能助手模块路由
app.include_router(assistant_router)

# 注册搜索模块路由
app.include_router(search_router)

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 自定义获取当前用户函数
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
    
    # 检查令牌是否为空
    if token is None:
        raise credentials_exception
    
    try:
        # 解码 JWT 令牌
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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

# Models
class WechatLogin(BaseModel):
    code: str
    user_info: Optional[Dict[str, Any]] = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    openid: str
    user_id: Optional[int] = None

# 文件上传配置
# 允许的文件类型
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
# 允许的最大文件大小 (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# 获取文件扩展名
def get_file_extension(filename):
    if not filename:
        return ""
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""

# 检查文件类型是否允许
def allowed_file(filename):
    if not filename:
        return False
    return get_file_extension(filename) in ALLOWED_EXTENSIONS

# 创建用户上传目录
def create_user_upload_dir(user_id):
    user_dir = os.path.join(UPLOADS_DIR, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, exist_ok=True)
    return user_dir

# Utility functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_wechat_session_key(code: str):
    """Get WeChat session key from code"""
    url = "https://api.weixin.qq.com/sns/jscode2session"
    params = {
        "appid": WECHAT_APPID,
        "secret": WECHAT_SECRET,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Routes
@app.get("/")
async def root():
    return {"message": "欢迎使用旅游景点智能推荐系统API"}

@app.post("/api/wechat-login", response_model=Token)
async def wechat_login(login_data: WechatLogin, db: Session = Depends(get_db)):
    """WeChat Mini Program login endpoint"""
    # Get session key and openid from WeChat
    result = get_wechat_session_key(login_data.code)
    
    if "errcode" in result and result["errcode"] != 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"微信登录失败: {result.get('errmsg', '未知错误')}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    openid = result.get("openid")
    session_key = result.get("session_key")
    
    # 检查用户是否存在
    user = db.query(User).filter(User.openid == openid).first()
    
    # 如果用户不存在，创建新用户
    if not user:
        print(f"创建新用户，openid: {openid}")
        user = User(
            openid=openid,
            session_key=session_key
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        print(f"用户已存在，更新session_key，用户ID: {user.id}")
        # 更新session_key
        user.session_key = session_key
        db.commit()
        db.refresh(user)
    
    # 如果请求中包含用户信息，则更新用户资料
    if login_data.user_info:
        print(f"更新用户信息: {login_data.user_info}")
        user_info = login_data.user_info
        user.nickname = user_info.get("nickname")
        user.avatar_url = user_info.get("avatar_url")
        user.gender = user_info.get("gender")
        user.country = user_info.get("country")
        user.province = user_info.get("province")
        user.city = user_info.get("city")
        user.language = user_info.get("language")
        db.commit()
        db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": openid},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "openid": openid,
        "user_id": user.id
    }

# 文件上传API
@app.post("/api/upload", status_code=status.HTTP_201_CREATED, response_description="上传图片")
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"接收到上传请求，用户ID: {current_user.id}，文件名: {file.filename}")
    
    try:
        # 检查文件是否上传
        if not file:
            logger.error("未提供文件")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="未提供文件"
            )
            
        # 检查文件名
        if not file.filename:
            logger.error("文件名为空")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件名为空"
            )
            
        # 检查Content-Type
        content_type = file.content_type
        logger.info(f"文件Content-Type: {content_type}")
        
        # 检查文件类型
        if not allowed_file(file.filename):
            logger.error(f"不支持的文件类型: {file.filename}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只允许上传PNG和JPEG格式的图片"
            )
        
        # 检查文件大小
        file_size = 0
        # 先将文件读入内存以检查大小
        file_content = await file.read()
        file_size = len(file_content)
        
        logger.info(f"文件大小: {file_size} 字节")
        
        # 重置文件指针以便后续操作
        await file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            logger.error(f"文件大小超过限制: {file_size} > {MAX_FILE_SIZE}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件大小不能超过5MB"
            )
        
        # 创建用户目录
        user_dir = create_user_upload_dir(current_user.id)
        
        # 生成唯一文件名
        file_extension = get_file_extension(file.filename)
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(user_dir, unique_filename)
        
        logger.info(f"准备保存文件到: {file_path}")
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # 构造文件访问URL
        file_url = f"{settings.API_URL}/uploads/{current_user.id}/{unique_filename}"
        
        logger.info(f"文件上传成功，URL: {file_url}")
        
        return {"url": file_url, "filename": unique_filename}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"文件上传过程出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器处理文件时出错: {str(e)}"
        )

@app.post("/api/upload/multiple", status_code=status.HTTP_201_CREATED, response_description="上传多张图片")
async def upload_multiple_images(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"接收到多文件上传请求，用户ID: {current_user.id}，文件数量: {len(files)}")
    
    try:
        if len(files) > 9:
            logger.error(f"文件数量超过限制: {len(files)} > 9")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="一次最多只能上传9张图片"
            )
        
        uploaded_files = []
        
        for index, file in enumerate(files):
            logger.info(f"处理第 {index+1}/{len(files)} 个文件: {file.filename}")
            
            # 检查文件类型
            if not allowed_file(file.filename):
                logger.error(f"不支持的文件类型: {file.filename}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"文件 {file.filename} 格式不支持，只允许上传PNG和JPEG格式的图片"
                )
            
            # 检查文件大小
            file_content = await file.read()
            file_size = len(file_content)
            
            logger.info(f"文件大小: {file_size} 字节")
            
            # 重置文件指针
            await file.seek(0)
            
            if file_size > MAX_FILE_SIZE:
                logger.error(f"文件大小超过限制: {file_size} > {MAX_FILE_SIZE}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"文件 {file.filename} 超过5MB大小限制"
                )
            
            # 创建用户目录
            user_dir = create_user_upload_dir(current_user.id)
            
            # 生成唯一文件名
            file_extension = get_file_extension(file.filename)
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(user_dir, unique_filename)
            
            logger.info(f"准备保存文件到: {file_path}")
            
            # 保存文件
            with open(file_path, "wb") as buffer:
                buffer.write(file_content)
            
            # 构造文件访问URL
            file_url = f"{settings.API_URL}/uploads/{current_user.id}/{unique_filename}"
            
            logger.info(f"文件上传成功，URL: {file_url}")
            
            uploaded_files.append({
                "url": file_url,
                "filename": unique_filename
            })
        
        logger.info(f"所有文件上传成功，总数: {len(uploaded_files)}")
        
        return {"files": uploaded_files}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"多文件上传过程出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器处理文件时出错: {str(e)}"
        )

# 博文发布API
@app.post("/api/posts", response_model=PostBrief, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新博文
    
    - 参数:
        - post: 博文创建模型，包含标题、内容、图片和标签等
    - 返回:
        - 创建成功的博文简要信息，包含ID和标题
    """
    try:
        # 确保images和tags是列表类型
        images = list(post.images) if post.images else []
        tags = list(post.tags) if post.tags else []
        
        # 使用BERT模型进行情感分析
        try:
            sentiment_result = analyze_sentiment(post.content)
            logger.info(f"情感分析结果: {sentiment_result}")
        except Exception as e:
            logger.error(f"情感分析出错，使用默认值'neutral': {str(e)}")
            sentiment_result = "neutral"  # 如果情感分析失败，使用默认值
        
        # 创建新的博文对象
        new_post = Post(
            title=post.title,
            content=post.content,
            images=images,  # 确保是列表
            tags=tags,      # 确保是列表
            location=post.location,
            cover_image=post.cover_image,
            user_id=current_user.id,
            created_at=datetime.utcnow(),
            likes_count=0,
            comments_count=0,
            sentiment_type=sentiment_result  # 添加情感分析结果
        )
        
        # 保存到数据库
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        # 返回创建成功的博文信息
        return {
            "id": new_post.id,
            "title": new_post.title,
            "content": new_post.content,
            "cover_image": new_post.cover_image,
            "created_at": new_post.created_at,
            "likes_count": 0,
            "comments_count": 0,
            "sentiment_type": new_post.sentiment_type,  # 返回情感分析结果
            "user": {
                "id": current_user.id,
                "username": current_user.nickname,
                "nickname": current_user.nickname,
                "avatar": current_user.avatar_url
            }
        }
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"创建博文失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器错误，博文创建失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"未预期的错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发生未知错误: {str(e)}"
        )

@app.get("/api/posts", response_model=List[PostBrief])
async def get_posts(
    skip: int = 0, 
    limit: int = 10,
    user_id: Optional[int] = None,
    tag: Optional[str] = None, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    获取博文列表
    
    - 参数:
        - skip: 跳过的记录数，默认为0
        - limit: 返回的最大记录数，默认为10
        - user_id: 可选，按用户ID筛选
        - tag: 可选，按标签筛选
    - 返回:
        - 博文简要信息列表
    """
    try:
        # 构建查询
        query = db.query(Post).options(
            # 加载用户关系
            joinedload(Post.user)
        )
        
        # 如果提供了用户ID，则只返回该用户的博文
        if user_id:
            query = query.filter(Post.user_id == user_id)
            
        # 如果提供了标签，则筛选包含该标签的博文
        if tag:
            # 注意：这种实现方式取决于你的数据库引擎对JSON的支持
            # PostgreSQL实现方式
            query = query.filter(Post.tags.contains([tag]))
            
        # 获取结果
        posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()
        
        # 处理结果，手动添加用户信息
        result = []
        for post in posts:
            post_dict = {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "cover_image": post.cover_image,
                "created_at": post.created_at,
                "likes_count": post.likes_count,
                "comments_count": post.comments_count,
                "sentiment_type": post.sentiment_type,  # 添加情感分析结果
                "user": None
            }
            
            # 如果有用户信息，添加到结果中
            if post.user:
                post_dict["user"] = {
                    "id": post.user.id,
                    "username": post.user.nickname,
                    "nickname": post.user.nickname,
                    "avatar": post.user.avatar_url
                }
            
            result.append(post_dict)
        
        return result
    except Exception as e:
        logger.error(f"获取博文列表时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取博文列表失败"
        )

@app.get("/api/posts/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    获取单个博文详情
    
    - 参数:
        - post_id: 博文ID
    - 返回:
        - 博文完整信息
    """
    try:
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="博文不存在"
            )
        
        return post
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取博文详情时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取博文详情失败"
        )

@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除博文
    
    - 参数:
        - post_id: 需要删除的博文ID
    - 返回:
        - 204状态码，无内容返回
    """
    try:
        # 查询博文是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="博文不存在"
            )
        
        # 检查当前用户是否有权限删除该博文
        if post.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="没有权限删除此博文"
            )
        
        # 执行删除操作
        db.delete(post)
        db.commit()
        
        # 返回成功但无内容
        return None
    
    except HTTPException:
        # 直接向上传递HTTP异常
        raise
    except SQLAlchemyError as e:
        # 数据库错误
        db.rollback()
        logger.error(f"删除博文时数据库错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"数据库错误: {str(e)}"
        )
    except Exception as e:
        # 其他未预期的错误
        logger.error(f"删除博文时发生未知错误: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除博文失败"
        )

@app.post("/api/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    post_id: int, 
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为指定博文创建评论
    
    - 参数:
        - post_id: 博文ID
        - comment: 评论内容
    - 返回:
        - 创建的评论信息
    """
    try:
        # 检查博文是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="博文不存在")
        
        # 创建新评论
        new_comment = Comment(
            post_id=post_id,
            user_id=current_user.id,
            parent_id=comment.parent_id,
            content=comment.content,
            created_at=datetime.utcnow()
        )
        
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
        # 更新博文的评论计数
        post.comments_count += 1
        db.commit()
        
        # 构造响应数据
        result = {
            "id": new_comment.id,
            "post_id": new_comment.post_id,
            "user_id": new_comment.user_id,
            "parent_id": new_comment.parent_id,
            "content": new_comment.content,
            "created_at": new_comment.created_at,
            "user": {
                "id": current_user.id,
                "username": current_user.nickname,
                "nickname": current_user.nickname,
                "avatar": current_user.avatar_url
            }
        }
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"创建评论失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建评论失败: {str(e)}")

@app.get("/api/posts/{post_id}/comments", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: int, 
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    获取指定博文的评论列表
    
    - 参数:
        - post_id: 博文ID
        - skip: 跳过的记录数，默认为0
        - limit: 返回的最大记录数，默认为10
    - 返回:
        - 评论列表
    """
    try:
        # 检查博文是否存在
        post = db.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise HTTPException(status_code=404, detail="博文不存在")
        
        # 获取评论列表，按创建时间降序排序
        comments = db.query(Comment).filter(
            Comment.post_id == post_id,
            Comment.parent_id == None  # 仅获取顶级评论
        ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
        
        # 构造响应数据
        result = []
        for comment in comments:
            # 获取评论用户信息
            user = db.query(User).filter(User.id == comment.user_id).first()
            
            comment_dict = {
                "id": comment.id,
                "post_id": comment.post_id,
                "user_id": comment.user_id,
                "parent_id": comment.parent_id,
                "content": comment.content,
                "created_at": comment.created_at,
                "user": None
            }
            
            # 如果有用户信息，添加到结果中
            if user:
                comment_dict["user"] = {
                    "id": user.id,
                    "username": user.nickname,
                    "nickname": user.nickname,
                    "avatar": user.avatar_url
                }
            
            result.append(comment_dict)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取评论列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取评论列表失败: {str(e)}")

# 用户兴趣标签请求体
class InterestTagsRequest(BaseModel):
    tags: str

@app.post("/api/update-interests", status_code=status.HTTP_200_OK)
async def update_user_interests(
    interest_data: InterestTagsRequest, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新用户兴趣标签
    
    Args:
        interest_data: 包含用户选择的兴趣标签
        db: 数据库会话
        current_user: 当前活跃用户
        
    Returns:
        成功信息
    """
    try:
        # 更新用户兴趣标签
        current_user.interest_tags = interest_data.tags
        db.commit()
        db.refresh(current_user)
        
        logger.info(f"用户 {current_user.id} 的兴趣标签已更新为: {interest_data.tags}")
        
        return {"message": "兴趣标签更新成功"}
    except Exception as e:
        db.rollback()
        logger.error(f"更新兴趣标签失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"更新兴趣标签失败: {str(e)}")

# 添加Qwen API请求模型
class QwenRequest(BaseModel):
    question: str
    history: Optional[List[Dict[str, str]]] = None

# 添加Qwen API响应模型
class QwenResponse(BaseModel):
    response: str
    history: List[Dict[str, str]]

# 添加Qwen API端点
@app.post("/api/qwen-chat")
async def chat_with_qwen(request: QwenRequest):
    """
    与Qwen模型对话的接口
    """
    try:
        print(f"收到问题: {request.question}")
        print(f"历史记录: {request.history if request.history else '[]'}")
        
        # 准备发送给Ollama的消息
        history = request.history if request.history else []
        user_message = {"role": "user", "content": request.question}
        
        # 直接使用generate API，避免使用chat API
        # 构建完整提示词
        full_prompt = ""
        for msg in history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                full_prompt += f"用户: {content}\n"
            elif role == "assistant":
                full_prompt += f"助手: {content}\n"
        
        # 添加当前用户问题
        full_prompt += f"用户: {request.question}\n助手: "
        
        print(f"准备发送请求到 {OLLAMA_API_BASE}/api/generate")
        print(f"提示词: {full_prompt}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OLLAMA_API_BASE}/api/generate",
                json={
                    "model": MODEL_NAME,
                    "prompt": full_prompt,
                    "stream": False
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"收到Ollama响应: {result}")
                
                # 直接从generate接口获取response字段
                bot_response = result.get("response", "")
                if not bot_response:
                    bot_response = "抱歉，我暂时无法回答您的问题。"
                
                # 更新对话历史
                new_history = history + [
                    user_message,
                    {"role": "assistant", "content": bot_response}
                ]
                
                return QwenResponse(response=bot_response, history=new_history)
            else:
                print(f"Generate API 返回错误: {response.status_code}")
                print(f"错误详情: {response.text}")
                raise HTTPException(status_code=500, detail=f"与Qwen模型交互时出错: {response.text}")
    except httpx.RequestError as e:
        print(f"请求Ollama API时出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"与Qwen模型交互时出错: {str(e)}")
    except Exception as e:
        print(f"处理请求时出错: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"与Qwen模型交互时出错: {str(e)}")

@app.get("/api/users/{user_id}")
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    根据用户ID获取用户信息
    
    参数:
        - user_id: 用户ID
    返回:
        - 用户信息
    """
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return {
            "id": user.id,
            "nickname": user.nickname,
            "avatar_url": user.avatar_url,
            "gender": user.gender,
            "country": user.country,
            "province": user.province,
            "city": user.city,
            "language": user.language,
            "created_at": user.created_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取用户信息时出错: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )

if __name__ == "__main__":
    import uvicorn
    
    # 设置并启动定时任务调度器
    setup_scheduler()
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    finally:
        # 应用关闭时关闭调度器
        shutdown_scheduler() 