import os
import uuid
import shutil
import logging
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form, Request
from fastapi.responses import JSONResponse
from typing import List, Optional
from ...auth.dependencies import get_current_user
from ...models.user import User
from ...config.settings import settings

# 设置日志
logger = logging.getLogger(__name__)

# 创建路由
router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)

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
    user_dir = os.path.join(settings.UPLOADS_DIR, str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, exist_ok=True)
    return user_dir

@router.post("/", status_code=status.HTTP_201_CREATED, response_description="上传图片")
async def upload_image(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
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
        
        # 记录请求头信息，用于调试
        headers = dict(request.headers)
        logger.info(f"请求头: {headers}")
        
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

@router.post("/multiple/", status_code=status.HTTP_201_CREATED, response_description="上传多张图片")
async def upload_multiple_images(
    request: Request,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    logger.info(f"接收到多文件上传请求，用户ID: {current_user.id}，文件数量: {len(files)}")
    
    try:
        if len(files) > 9:
            logger.error(f"文件数量超过限制: {len(files)} > 9")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="一次最多只能上传9张图片"
            )
        
        # 记录请求头信息，用于调试
        headers = dict(request.headers)
        logger.info(f"请求头: {headers}")
        
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