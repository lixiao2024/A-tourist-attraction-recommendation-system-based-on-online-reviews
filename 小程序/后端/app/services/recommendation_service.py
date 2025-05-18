from sqlalchemy.orm import Session, joinedload
from typing import List, Optional, Dict, Any
import json
import math
import logging
from app.models.post_model import Post
from app.models.user import User

# 设置日志
logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db
        
        # 定义权重常量
        self.SAME_CITY_WEIGHT = 4.0      # 同城市权重
        self.INTEREST_SPOT_WEIGHT = 5.0  # 感兴趣景点权重
        self.OTHER_SPOT_WEIGHT = 2.0     # 同城市其他景点权重
        self.LIKES_BOOST = 0.5           # 点赞数量提升因子
        self.DEFAULT_WEIGHT = 1.0        # 默认权重

    def calculate_post_score(self, post: Post, user_interests: Dict[str, Any]) -> float:
        """
        计算每篇博文的推荐分数
        
        Args:
            post: 博文对象
            user_interests: 用户兴趣标签信息
        
        Returns:
            float: 推荐分数
        """
        # 初始分数
        score = self.DEFAULT_WEIGHT
        
        # 如果没有标签或用户没有兴趣偏好，返回默认分数
        if not post.tags or not user_interests:
            return score
        
        # 解析用户兴趣
        user_city = user_interests.get('city')
        user_attractions = set(user_interests.get('attractions', []))
        
        # 获取博文标签
        post_tags = set(post.tags)
        
        # 如果博文涉及用户感兴趣的城市，增加权重
        if user_city and user_city in post_tags:
            score += self.SAME_CITY_WEIGHT
            
            # 如果博文标签中包含用户感兴趣的景点，进一步增加权重
            for attraction in user_attractions:
                if attraction in post_tags:
                    score += self.INTEREST_SPOT_WEIGHT
                    break
            else:
                # 如果是同城市但不是感兴趣的景点，给一个较低的权重提升
                score += self.OTHER_SPOT_WEIGHT
        
        # 根据点赞数提升分数，使用对数函数避免热门帖子权重过高
        likes_boost = math.log(post.likes_count + 1) * self.LIKES_BOOST
        score += likes_boost
        
        return score

    async def get_recommended_posts(
        self,
        skip: int = 0,
        limit: int = 15,
        is_refresh: bool = False,
        current_user: Optional[User] = None
    ) -> List[Dict[str, Any]]:
        """
        获取推荐的博文列表
        
        Args:
            skip: 跳过的记录数
            limit: 返回的最大记录数
            is_refresh: 是否为刷新操作
            current_user: 当前用户对象
            
        Returns:
            List[Dict[str, Any]]: 推荐博文列表
        """
        # 构建基础查询
        query = self.db.query(Post).options(
            joinedload(Post.user)
        )
        
        # 获取所有博文
        all_posts = query.all()
        scored_posts = []
        
        # 如果用户已登录且设置了兴趣标签
        if current_user and current_user.interest_tags:
            try:
                # 解析用户兴趣标签
                user_interests = json.loads(current_user.interest_tags)
                logger.info(f"用户兴趣标签: {user_interests}")
                
                # 为每篇博文计算得分
                for post in all_posts:
                    score = self.calculate_post_score(post, user_interests)
                    scored_posts.append((post, score))
                
                # 按分数降序排序
                scored_posts.sort(key=lambda x: x[1], reverse=True)
                logger.info(f"已对博文进行评分排序，共 {len(scored_posts)} 条")
                
            except Exception as e:
                logger.error(f"解析用户兴趣标签失败: {str(e)}")
                # 发生错误时，退化为按点赞数排序
                scored_posts = [(post, post.likes_count) for post in all_posts]
                scored_posts.sort(key=lambda x: x[1], reverse=True)
        else:
            logger.info("用户未登录或没有兴趣标签，按点赞数排序")
            # 用户未登录或没有兴趣标签，按点赞数排序
            scored_posts = [(post, post.likes_count) for post in all_posts]
            scored_posts.sort(key=lambda x: x[1], reverse=True)
        
        # 应用分页
        paginated_posts = [post for post, score in scored_posts[skip:skip+limit]]
        
        # 构建响应
        result = []
        for post in paginated_posts:
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