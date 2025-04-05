from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
import logging
import datetime
import sqlalchemy

from app.schemas.post_schema import PostCreate, PostResponse, PostBrief
from app.models.post_model import Post
from app.models.database import get_db
from app.auth.dependencies import get_current_user, get_optional_current_user
from app.models.user import User
from app.models.comment import Comment
from app.schemas.comment_schema import CommentCreate, CommentResponse

# 设置日志
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"]
)

@router.post("/", response_model=PostBrief, status_code=status.HTTP_201_CREATED)
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
        
        # 创建新的博文对象，明确指定字段
        new_post = Post(
            title=post.title,
            content=post.content,
            images=images,  # 确保是列表
            tags=tags,      # 确保是列表
            location=post.location,
            cover_image=post.cover_image,
            user_id=current_user.id,
            created_at=datetime.datetime.utcnow(),
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
            "content": new_post.content,
            "cover_image": new_post.cover_image,
            "created_at": new_post.created_at,
            "likes_count": 0,
            "comments_count": 0,
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

@router.get("/", response_model=List[PostBrief])
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
            sqlalchemy.orm.joinedload(Post.user)
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

@router.get("/{post_id}", response_model=PostResponse)
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

@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    post_id: int, 
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    为指定帖子创建评论或回复评论
    """
    # 检查帖子是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    
    # 创建新评论
    new_comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        parent_id=comment.parent_id,
        content=comment.content
    )
    
    try:
        # 将评论添加到数据库
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
        # 更新帖子的评论计数
        post.comments_count = post.comments_count + 1 if post.comments_count else 1
        db.commit()
        
        # 构建响应数据
        response_data = {
            "id": new_comment.id,
            "post_id": new_comment.post_id,
            "user_id": new_comment.user_id,
            "parent_id": new_comment.parent_id,
            "content": new_comment.content,
            "created_at": new_comment.created_at,
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "nickname": current_user.nickname,
                "avatar": current_user.avatar
            }
        }
        
        return response_data
    
    except Exception as e:
        db.rollback()
        logger.error(f"创建评论时发生错误: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建评论失败: {str(e)}")

@router.get("/{post_id}/comments", response_model=List[CommentResponse])
async def get_post_comments(
    post_id: int, 
    skip: int = 0, 
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    """
    获取指定帖子的评论列表
    """
    # 检查帖子是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")
    
    # 查询评论（一级评论，parent_id 为 NULL）
    comments = db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.parent_id == None
    ).order_by(Comment.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for comment in comments:
        # 获取评论作者
        user = db.query(User).filter(User.id == comment.user_id).first()
        
        comment_data = {
            "id": comment.id,
            "post_id": comment.post_id,
            "user_id": comment.user_id,
            "parent_id": comment.parent_id,
            "content": comment.content,
            "created_at": comment.created_at,
            "user": {
                "id": user.id if user else None,
                "username": user.username if user else "已删除用户",
                "nickname": user.nickname if user else "已删除用户",
                "avatar": user.avatar if user else None
            }
        }
        result.append(comment_data)
    
    return result 
