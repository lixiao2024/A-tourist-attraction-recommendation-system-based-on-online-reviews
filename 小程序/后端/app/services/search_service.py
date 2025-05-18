from sqlalchemy.orm import Session, joinedload
from typing import List, Dict, Any, Optional
import logging
from sqlalchemy import or_
from app.models.post_model import Post
from app.models.user import User

# 设置日志
logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, db: Session):
        self.db = db

    async def search_posts(
        self,
        keyword: str,
        skip: int = 0,
        limit: int = 15,
        current_user: Optional[User] = None
    ) -> List[Dict[str, Any]]:
        """
        根据关键词搜索博文
        
        Args:
            keyword: 搜索关键词
            skip: 跳过的记录数
            limit: 返回的最大记录数
            current_user: 当前用户对象
            
        Returns:
            List[Dict[str, Any]]: 匹配的博文列表
        """
        try:
            # 构建查询
            query = self.db.query(Post).options(
                joinedload(Post.user)
            )
            
            # 如果关键词不为空，按标题搜索
            if keyword:
                query = query.filter(
                    or_(
                        Post.title.ilike(f"%{keyword}%"),  # 标题模糊匹配
                        Post.content.ilike(f"%{keyword}%")  # 内容模糊匹配
                    )
                )
            else:
                # 如果关键词为空，返回最新博文
                query = query.order_by(Post.created_at.desc())
            
            # 应用分页
            posts = query.offset(skip).limit(limit).all()
            
            logger.info(f"搜索关键词 '{keyword}' 找到 {len(posts)} 条结果")
            
            # 构建响应
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
                    "images": post.images,  # 包含图片数组
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
            logger.error(f"搜索博文时出错: {str(e)}")
            # 出错时返回空列表
            return [] 