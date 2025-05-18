## 1.完成首页推荐系统设计

基于多维权重的旅游景点智能推荐算法设计与实现 ✅

1.  算法概述
    本研究设计并实现了一种基于多维权重的旅游景点智能推荐算法，该算法融合了基于内容的推荐和基于流行度的推荐策略，通过分析用户兴趣标签与旅游笔记内容的匹配度，结合点赞数据作为社会化信号，为用户提供个性化的旅游景点推荐。
2.  算法理论基础
    2.1 多维特征权重模型
    本算法采用多维特征权重模型，将推荐问题转化为对不同特征维度赋予不同权重的计算过程。该模型考虑了以下维度：
    地域匹配维度：用户感兴趣的城市与内容标签的匹配程度
    景点兴趣维度：用户感兴趣的具体景点与内容标签的匹配程度
    内容流行度维度：基于点赞数量的社会认可度
    通过设定合理的权重系数，使算法能够平衡个性化与内容质量，提高推荐结果的相关性和多样性。
    2.2 对数变换处理热度信号
    为避免热门内容过度主导推荐结果，算法对点赞数进行了对数变换处理：
    $$\text{likes\boost} = \log(likes\_count + 1) \times LIKES\_BOOST$$
    这种处理方式能够有效平滑热度数据的影响，使得点赞数量的增长对推荐分数的贡献呈对数增长关系，而非线性关系。
3.  算法设计与实现
    3.1 权重系数设计
    算法定义了一组精心调整的权重常量：
    Apply to README5.3tas...
    SAME_CITY_WEIGHT = 4.0 # 同城市权重
    INTEREST_SPOT_WEIGHT = 5.0 # 感兴趣景点权重
    OTHER_SPOT_WEIGHT = 2.0 # 同城市其他景点权重
    LIKES_BOOST = 0.5 # 点赞数量提升因子
    DEFAULT_WEIGHT = 1.0 # 默认权重
    这些权重反映了不同匹配条件的重要性：
    用户感兴趣的景点获得最高权重(5.0)
    用户感兴趣的城市获得次高权重(4.0)
    同城市但非兴趣景点的内容获得较低权重(2.0)
    点赞数通过乘以 0.5 的系数进行适度调整
    3.2 评分函数实现
    算法核心是评分函数 calculate_post_score，它计算每篇旅游笔记的推荐得分：
    Apply to README5.3tas...
    def calculate_post_score(post, user_interests): # 初始分数
    score = DEFAULT_WEIGHT # 如果没有标签或用户没有兴趣偏好，返回默认分数
    if not post.tags or not user_interests:
    return score

        # 解析用户兴趣
        user_city = user_interests.get('city')
        user_attractions = set(user_interests.get('attractions', []))

        # 获取博文标签
        post_tags = set(post.tags)

        # 如果博文涉及用户感兴趣的城市，增加权重
        if user_city and user_city in post_tags:
            score += SAME_CITY_WEIGHT

            # 如果博文标签中包含用户感兴趣的景点，进一步增加权重
            for attraction in user_attractions:
                if attraction in post_tags:
                    score += INTEREST_SPOT_WEIGHT
                    break
            else:
                # 如果是同城市但不是感兴趣的景点，给一个较低的权重提升
                score += OTHER_SPOT_WEIGHT

        # 根据点赞数提升分数，使用对数函数避免热门帖子权重过高
        likes_boost = math.log(post.likes_count + 1) * LIKES_BOOST
        score += likes_boost

        return score

    这个函数实现了一个级联条件评分机制：
    首先判断是否匹配用户感兴趣的城市
    如果匹配城市，进一步判断是否匹配用户感兴趣的景点
    最后融合点赞数带来的社会化信号影响
    3.3 多层次回退策略
    算法设计了多层次回退策略，保证系统的鲁棒性：
    Apply to README5.3tas...

# 如果用户已登录且设置了兴趣标签

if current_user and current_user.interest_tags:
try: # 解析用户兴趣标签并计算个性化推荐 # ...
except Exception as e: # 发生错误时，退化为按点赞数排序
scored_posts = [(post, post.likes_count) for post in all_posts]
scored_posts.sort(key=lambda x: x[1], reverse=True)
else: # 用户未登录或没有兴趣标签，按点赞数排序
scored_posts = [(post, post.likes_count) for post in all_posts]
scored_posts.sort(key=lambda x: x[1], reverse=True)
该策略确保:
当用户有兴趣标签时，提供个性化推荐
当系统无法获取或处理用户兴趣标签时，自动退化为基于点赞数的热门内容推荐
当用户未登录时，提供基于流行度的通用推荐 4. 算法优势与创新点
4.1 理论创新
多维度权重整合：有机结合用户地域兴趣、景点偏好和社会认可度
对数变换处理：使用对数函数平滑热度数据，避免热门内容垄断
级联条件评分：设计了细粒度的匹配条件，针对不同匹配程度赋予差异化权重
4.2 实用价值
流量精准分配：通过调整点赞数量，可有效控制内容的曝光量，实现流量精准干预
冷启动问题解决：对于无兴趣标签的新用户，提供了基于流行度的内容推荐
算法可解释性：权重模型使推荐结果具有良好的可解释性，易于理解和调整
4.3 技术实现优势
内存计算模式：通过内存计算而非复杂 SQL 查询，获得更高的计算效率
优雅降级机制：在各种异常情况下能够自动降级，保证系统稳定性
分页处理优化：实现了高效的内存分页，保证页面响应速度 5. 系统架构与工程实现
5.1 模块化设计
推荐算法被设计为独立模块，便于维护和扩展：
Apply to README5.3tas...

# 推荐模块 API 注册

router = APIRouter(
prefix="/api/recommendations",
tags=["Recommendations"]
)

# API 端点定义

@router.get("/posts", response_model=List[PostBrief])
async def get_recommended_posts(...): # 推荐逻辑实现
5.2 前后端交互
后端提供推荐 API，前端根据场景调用不同接口：
Apply to README5.3tas...
// 前端推荐 API 调用
export function getRecommendedPosts(skip = 0, limit = 15, isRefresh = false) {
// 构建查询参数
let url = `/api/recommendations/posts?skip=${skip}&limit=${limit}`;

// 添加刷新参数
if (isRefresh) {
url += `&is_refresh=true`;
}

// 请求处理...
}

// 在首页根据分类选择不同 API
if (this.currentCategory === '推荐') {
// 使用推荐 API
result = await getRecommendedPosts(skip, this.pageSize, isRefresh);
} else {
// 使用常规博文 API，传递 tag 参数
result = await getPosts(skip, this.pageSize, tag, isRefresh);
}
5.3 数据结构设计
算法利用以下数据结构：
用户兴趣标签: {"city": "城市名", "attractions": ["景点 1", "景点 2", ...]}
博文标签: ["城市名", "景点名", ...]
评分结果: [(post, score), ...] - 博文对象与分数的元组列表 6. 未来优化方向
算法还可在以下方面进一步优化：
时间衰减因子：引入基于发布时间的衰减因子，平衡内容新鲜度与相关性
用户行为权重：整合用户点赞、评论、分享等行为数据，构建更精准的兴趣模型
负反馈机制：引入用户对内容的负面反馈，优化推荐结果
情感分析整合：利用现有的情感分析结果，根据用户偏好推荐正面或负面评价
基于协同过滤的补充：引入基于相似用户的协同过滤推荐，进一步丰富推荐结果 7. 结论
本研究设计并实现了一种基于多维权重的旅游景点智能推荐算法，通过精细化的权重设计和对数变换处理，成功平衡了个性化推荐与内容质量。该算法在考虑用户地域兴趣和景点偏好的同时，巧妙融合社会化信号，实现了精准的内容推荐。算法的多层次回退策略和优雅降级机制保证了系统的鲁棒性，为旅游领域的个性化推荐提供了一种有效解决方案。

## 2.完成默认头像路径问题 ✅

## 3.修改首页每次刷新都要重新让用户选兴趣标签的缺陷 ✅

## 4.论文第三部分完成
