from fastapi import FastAPI, HTTPException, status, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session, joinedload
import os
import uuid
import logging
import shutil
from sqlalchemy.exc import SQLAlchemyError

# 导入应用配置和数据库模型
from app.config.settings import settings
from app.models.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.post_model import Post
from app.schemas.post_schema import PostCreate, PostResponse, PostBrief
from app.auth.dependencies import get_current_user

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

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
            comments_count=0
        )
        
        # 保存到数据库
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        # 返回创建成功的博文信息
        return {
            "id": new_post.id,
            "title": new_post.title,
            "cover_image": new_post.cover_image,
            "created_at": new_post.created_at,
            "likes_count": 0,
            "comments_count": 0
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
    current_user: User = Depends(get_current_user)
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
    current_user: User = Depends(get_current_user)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 