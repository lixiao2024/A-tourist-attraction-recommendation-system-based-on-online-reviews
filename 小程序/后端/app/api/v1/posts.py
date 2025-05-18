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
from app.utils.sentiment_analysis import analyze_sentiment  # 导入情感分析函数

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
        
        # 使用BERT模型进行情感分析
        try:
            sentiment_result = analyze_sentiment(post.content)
            logger.debug(f"情感分析结果: {sentiment_result}, 文本内容: {post.content[:50]}...")
        except Exception as e:
            logger.error(f"情感分析出错，使用默认值'neutral': {str(e)}")
            sentiment_result = "neutral"  # 如果情感分析失败，使用默认值
        
        # 确保sentiment_result不为None
        if not sentiment_result:
            sentiment_result = "neutral"
        
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
            comments_count=0,
            sentiment_type=sentiment_result  # 添加情感分析结果
        )
        
        # 保存到数据库
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        # 打印调试信息
        logger.debug(f"已保存博文，ID: {new_post.id}, 情感类型: {new_post.sentiment_type}")
        
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
        logger.error(f"未预期的错误: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发生未知错误: {str(e)}"
        )

@router.get("/", response_model=List[PostBrief])
async def get_posts(
    skip: int = 0, 
    limit: int = 15,  # 修改默认限制为15条
    user_id: Optional[int] = None,
    tag: Optional[str] = None, 
    is_refresh: Optional[bool] = False,  # 添加刷新参数
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)  # 可选认证
):
    """
    获取博文列表，支持基于用户兴趣标签的推荐
    
    - 参数:
        - skip: 跳过的记录数，默认为0
        - limit: 返回的最大记录数，默认为15
        - user_id: 可选，按用户ID筛选
        - tag: 可选，按标签筛选
        - is_refresh: 可选，是否为下拉刷新操作
    - 返回:
        - 博文简要信息列表
    """
    try:
        import json
        import random
        from sqlalchemy import func, or_
        
        # 构建查询
        query = db.query(Post).options(
            # 加载用户关系
            sqlalchemy.orm.joinedload(Post.user)
        )
        
        # 如果提供了用户ID，则只返回该用户的博文
        if user_id:
            query = query.filter(Post.user_id == user_id)
        # 如果当前用户已登录且没有指定tag和user_id，使用用户的兴趣标签做推荐
        elif current_user and not tag:
            try:
                # 解析用户兴趣标签（JSON格式）
                if current_user.interest_tags:
                    user_interests = json.loads(current_user.interest_tags)
                    
                    # 构建查询条件
                    interest_conditions = []
                    
                    # 添加城市条件
                    if "city" in user_interests and user_interests["city"]:
                        interest_conditions.append(
                            Post.tags.contains([user_interests["city"]])
                        )
                    
                    # 添加景点条件
                    if "attractions" in user_interests and user_interests["attractions"]:
                        # 使用OR条件组合所有景点标签
                        for attraction in user_interests["attractions"]:
                            interest_conditions.append(
                                Post.tags.contains([attraction])
                            )
                    
                    # 如果有兴趣标签，则使用OR组合所有条件
                    if interest_conditions:
                        query = query.filter(or_(*interest_conditions))
                        logger.debug(f"应用用户兴趣标签过滤: {user_interests}")
            except Exception as e:
                # 如果解析兴趣标签失败，记录错误但继续执行
                logger.error(f"解析用户兴趣标签失败: {str(e)}")
            
        # 如果提供了标签，则筛选包含该标签的博文
        if tag:
            # 注意：这种实现方式取决于你的数据库引擎对JSON的支持
            query = query.filter(Post.tags.contains([tag]))
        
        # 如果是刷新操作，随机排序以提供新内容
        if is_refresh:
            query = query.order_by(func.random())
        else:
            # 否则按创建时间倒序排列
            query = query.order_by(Post.created_at.desc())
            
        # 获取结果
        posts = query.offset(skip).limit(limit).all()
        
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
                "sentiment_type": post.sentiment_type,
                "user": None
            }
            
            # 如果有用户信息，添加到结果中
            if post.user:
                post_dict["user"] = {
                    "id": post.user.id,
                    "username": post.user.nickname if post.user.nickname else "用户" + str(post.user.id),
                    "nickname": post.user.nickname if post.user.nickname else "用户" + str(post.user.id),
                    "avatar": post.user.avatar_url if post.user.avatar_url else None
                }
            else:
                # 如果没有用户信息，添加默认值
                post_dict["user"] = {
                    "id": 0,
                    "username": "未知用户",
                    "nickname": "未知用户",
                    "avatar": None
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

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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
