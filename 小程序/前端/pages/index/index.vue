<template>
	<view class="page-container">
		<!-- 顶部搜索和标题 -->
		<view class="header">
			<view class="title-area">
				<text class="page-title">探索·灵感</text>
			</view>
			<view class="search-wrapper">
				<uni-icons type="search" size="20" color="#999"></uni-icons>
				<input 
					type="search" 
					class="search-bar" 
					placeholder="搜索目的地、景点、攻略"
					placeholder-class="placeholder-style"
				/>
			</view>
		</view>
		
		<!-- 分类标签 -->
		<scroll-view scroll-x class="category-tabs" show-scrollbar="false">
			<view 
				v-for="(category, index) in categories" 
				:key="index"
				:class="['category-item', {active: currentCategory === category}]"
				@click="switchCategory(category)"
			>
				{{ category }}
			</view>
		</scroll-view>
		
		<!-- 瀑布流内容区 -->
		<scroll-view 
			class="waterfall-scroll"
			scroll-y
			:show-scrollbar="false"
			@scrolltolower="loadMore"
			refresher-enabled
			@refresherrefresh="refreshComments"
			:refresher-triggered="isRefreshing"
		>
			<view class="waterfall-container">
				<view class="waterfall-column">
					<view 
						v-for="comment in leftColumn" 
						:key="comment.id"
						class="card-item"
						@click="navigateToDetail(comment.id)"
					>
						<!-- 图片区域 -->
						<image 
							v-if="comment.images && comment.images.length > 0"
							class="card-image" 
							:src="comment.images[0]" 
							mode="aspectFill"
							@error="handleImageError(comment)"
						></image>
						
						<!-- 内容区域 -->
						<view class="card-content">
							<text class="card-title" :class="{expanded: comment.expanded}">{{ comment.title || comment.content }}</text>
							
							<!-- 展开/收起控制 -->
							<view 
								v-if="showExpandControl(comment)"
								class="expand-control"
							>
								<text 
									v-if="!comment.expanded"
									class="expand-btn"
									@click.stop="toggleExpand(comment)"
								>展开</text>
							</view>
							
							<!-- 用户信息 -->
							<view class="user-info">
								<image class="user-avatar" :src="comment.avatar" mode="aspectFill"></image>
								<text class="user-name">{{ comment.nickname }}</text>
							</view>
							
							<!-- 互动栏 -->
							<view class="interaction-bar">
								<view class="action-btn like-btn" :class="{active: comment.isLiked}" @click.stop="toggleLike(comment.id)">
									<uni-icons :type="comment.isLiked ? 'heart-filled' : 'heart'" size="20" :color="comment.isLiked ? '#ff5656' : '#666'"></uni-icons>
									<text class="count">{{ comment.likeCount || '' }}</text>
								</view>
								<view class="action-btn comment-btn" @click.stop="showCommentInput(comment.id)">
									<uni-icons type="chat" size="20" color="#666"></uni-icons>
									<text class="count">{{ comment.commentCount || '' }}</text>
								</view>
								<view class="action-btn share-btn" @click.stop="shareComment(comment)">
									<uni-icons type="paperplane" size="20" color="#666"></uni-icons>
								</view>
							</view>
						</view>
					</view>
				</view>
				
				<view class="waterfall-column">
					<view 
						v-for="comment in rightColumn" 
						:key="comment.id"
						class="card-item"
						@click="navigateToDetail(comment.id)"
					>
						<!-- 图片区域 -->
						<image 
							v-if="comment.images && comment.images.length > 0"
							class="card-image" 
							:src="comment.images[0]" 
							mode="aspectFill"
							@error="handleImageError(comment)"
						></image>
						
						<!-- 内容区域 -->
						<view class="card-content">
							<text class="card-title" :class="{expanded: comment.expanded}">{{ comment.title || comment.content }}</text>
							
							<!-- 展开/收起控制 -->
							<view 
								v-if="showExpandControl(comment)"
								class="expand-control"
							>
								<text 
									v-if="!comment.expanded"
									class="expand-btn"
									@click.stop="toggleExpand(comment)"
								>展开</text>
							</view>
							
							<!-- 用户信息 -->
							<view class="user-info">
								<image class="user-avatar" :src="comment.avatar" mode="aspectFill"></image>
								<text class="user-name">{{ comment.nickname }}</text>
							</view>
							
							<!-- 互动栏 -->
							<view class="interaction-bar">
								<view class="action-btn like-btn" :class="{active: comment.isLiked}" @click.stop="toggleLike(comment.id)">
									<uni-icons :type="comment.isLiked ? 'heart-filled' : 'heart'" size="20" :color="comment.isLiked ? '#ff5656' : '#666'"></uni-icons>
									<text class="count">{{ comment.likeCount || '' }}</text>
								</view>
								<view class="action-btn comment-btn" @click.stop="showCommentInput(comment.id)">
									<uni-icons type="chat" size="20" color="#666"></uni-icons>
									<text class="count">{{ comment.commentCount || '' }}</text>
								</view>
								<view class="action-btn share-btn" @click.stop="shareComment(comment)">
									<uni-icons type="paperplane" size="20" color="#666"></uni-icons>
								</view>
							</view>
						</view>
					</view>
				</view>
			</view>
			
			<!-- 加载更多提示 -->
			<view class="loading-more" v-if="isLoading">
				<uni-icons type="spinner-cycle" size="20" color="#999"></uni-icons>
				<text>加载更多中...</text>
			</view>
		</scroll-view>
		
		<!-- 悬浮发布按钮 -->
		<view class="floating-button" @click="navigateToPublish">
			<uni-icons type="plusempty" size="24" color="#fff"></uni-icons>
		</view>
	</view>
</template>

<script>
import { getPosts } from '@/request/api.js'

export default {
	data() {
		return {
			comments: [],
			lastClickTime: 0,
			categories: ['推荐', '攻略', '美食', '酒店', '购物', '文化', '拍照'],
			currentCategory: '推荐',
			isRefreshing: false,
			isLoading: false,
			page: 1,
			pageSize: 10,
			hasMore: true
		}
	},
	computed: {
		// 左侧瀑布流列
		leftColumn() {
			return this.comments.filter((_, index) => index % 2 === 0);
		},
		// 右侧瀑布流列
		rightColumn() {
			return this.comments.filter((_, index) => index % 2 === 1);
		}
	},
	onLoad() {
		// 初始加载数据
		this.loadPostsFromApi();
	},
	methods: {
		// 切换分类
		switchCategory(category) {
			this.currentCategory = category;
			this.page = 1;
			this.comments = [];
			this.hasMore = true;
			// 根据分类加载不同内容
			this.loadPostsFromApi();
		},
		
		// 处理图片加载错误
		handleImageError(comment) {
			// 使用默认图片
			if (comment.images && comment.images.length > 0) {
				comment.images[0] = '/static/default-image.png';
			}
		},
		
		navigateToDetail(commentId) {
			uni.navigateTo({
				url: '/pages/detail/detail?id=' + commentId
			})
		},
		
		navigateToPublish() {
			uni.navigateTo({
				url: '/pages/post/post'
			});
		},
		
		toggleExpand(comment) {
			comment.expanded = !comment.expanded
		},
		
		// 判断是否显示展开控制按钮
		showExpandControl(comment) {
			// 判断文本长度，如果是title，则超过40字符显示展开按钮
			// 如果是content，则超过50字符显示展开按钮
			if (comment.title && comment.title.length > 40) {
				return true;
			}
			return comment && comment.content && comment.content.length > 50;
		},
		
		toggleLike(commentId) {
			// 防抖处理：300ms内禁止重复点击
			const now = Date.now()
			if (now - this.lastClickTime < 300) return
			this.lastClickTime = now
			
			const comment = this.comments.find(item => item.id === commentId)
			if (!comment) return
			
			if (!comment.isLiked) {
				comment.likeCount++
				comment.isLiked = true
			} else {
				comment.likeCount--
				comment.isLiked = false
			}
		},
		
		// 从API加载博文数据
		async loadPostsFromApi() {
			try {
				if (this.isLoading) return;
				this.isLoading = true;
				
				uni.showLoading({
					title: '加载中...'
				});
				
				let skip = (this.page - 1) * this.pageSize;
				// 如果不是"推荐"分类，则作为tag参数传递
				let tag = this.currentCategory !== '推荐' ? this.currentCategory : null;
				
				// 调用API获取数据
				let result;
				try {
					// 传递tag参数给后端
					result = await getPosts(skip, this.pageSize, tag);
					console.log('获取到的博文数据:', result);
				} catch (apiError) {
					console.error('API请求失败:', apiError);
					throw apiError;
				}
				
				if (result && Array.isArray(result)) {
					// 转换数据格式以适应前端展示
					const posts = result.map(post => {
						console.log('处理博文数据:', post);
						// 确保每个字段都有默认值
						return {
							id: post.id || Date.now() + Math.floor(Math.random() * 1000),
							avatar: post.user && post.user.avatar ? post.user.avatar : '/static/default-avatar.png',
							nickname: post.user && post.user.nickname ? post.user.nickname : post.user && post.user.username ? post.user.username : '旅行达人',
							content: post.content || '',
							title: post.title || '',
							expanded: false,
							likeCount: post.likes_count || 0,
							isLiked: false,
							commentCount: post.comments_count || 0,
							publishTime: this.formatPublishTime(post.created_at) || '刚刚',
							// 优先使用cover_image作为封面，如果没有则使用第一张图片，都没有则为空数组
							images: post.cover_image ? [post.cover_image] : (Array.isArray(post.images) && post.images.length > 0 ? [post.images[0]] : [])
						};
					});
					
					// 如果是第一页，替换数据；否则追加数据
					if (this.page === 1) {
						this.comments = posts;
					} else {
						this.comments = [...this.comments, ...posts];
					}
					
					// 判断是否还有更多数据
					this.hasMore = posts.length >= this.pageSize;
				} else {
					if (this.page === 1) {
						// 如果没有数据，显示默认模拟数据
						this.loadDefaultData();
					}
					this.hasMore = false;
				}
			} catch (error) {
				console.error('加载博文数据失败:', error);
				// 出错时加载默认数据
				if (this.page === 1 && (!this.comments || this.comments.length === 0)) {
					this.loadDefaultData();
				}
				uni.showToast({
					title: '加载失败，请重试',
					icon: 'none'
				});
			} finally {
				this.isLoading = false;
				uni.hideLoading();
				if (this.isRefreshing) {
					this.isRefreshing = false;
					uni.stopPullDownRefresh();
				}
			}
		},
		
		// 加载默认模拟数据
		loadDefaultData() {
			// 根据分类提供不同的模拟数据
			if (this.currentCategory === '推荐' || this.comments.length === 0) {
				this.comments = [
					{
						id: 1,
						avatar: '/static/default-avatar.png',
						nickname: '旅行达人',
						content: '这个景点非常值得一去，尤其是日落时分的景色美不胜收！建议下午4点时到达，可以慢慢欣赏天色变化。',
						expanded: false,
						likeCount: 128,
						isLiked: false,
						commentCount: 42,
						publishTime: '3小时前',
						images: ['/static/demo/scenic1.jpg']
					},
					{
						id: 2,
						nickname: '摄影师小王',
						avatar: '/static/default-avatar.png',
						content: '周末带着相机来到这里，随手一拍就是大片，光线超级棒！分享几张照片给大家参考，喜欢摄影的朋友一定不要错过。',
						expanded: false,
						likeCount: 256,
						isLiked: false,
						commentCount: 66,
						publishTime: '昨天',
						images: ['/static/demo/scenic2.jpg']
					}
				];
			} else if (this.currentCategory === '美食') {
				this.comments = [
					{
						id: 101,
						avatar: '/static/default-avatar.png',
						nickname: '吃货小分队',
						content: '发现一家隐藏在巷子里的网红店，排队1小时才吃到，但真的超级值得！招牌菜是蒜香排骨和爆炒鱿鱼，下次还会再来！',
						expanded: false,
						likeCount: 321,
						isLiked: false,
						commentCount: 89,
						publishTime: '刚刚更新',
						images: ['/static/demo/food1.jpg']
					}
				];
			} else {
				this.comments = [
					{
						id: 201,
						avatar: '/static/default-avatar.png',
						nickname: '分类达人',
						content: `这是${this.currentCategory}分类的热门内容，希望对你有帮助！后续会持续更新更多相关内容。`,
						expanded: false,
						likeCount: Math.floor(Math.random() * 200),
						isLiked: false,
						commentCount: Math.floor(Math.random() * 50),
						publishTime: '刚刚更新',
						images: ['/static/demo/scenic' + (Math.floor(Math.random() * 3) + 1) + '.jpg']
					}
				];
			}
		},
		
		// 格式化发布时间
		formatPublishTime(timeStr) {
			if (!timeStr) return '未知时间';
			
			const publishTime = new Date(timeStr);
			const now = new Date();
			const diffMs = now - publishTime;
			const diffSec = Math.floor(diffMs / 1000);
			const diffMin = Math.floor(diffSec / 60);
			const diffHour = Math.floor(diffMin / 60);
			const diffDay = Math.floor(diffHour / 24);
			
			if (diffSec < 60) {
				return '刚刚';
			} else if (diffMin < 60) {
				return `${diffMin}分钟前`;
			} else if (diffHour < 24) {
				return `${diffHour}小时前`;
			} else if (diffDay < 30) {
				return `${diffDay}天前`;
			} else {
				// 返回具体日期，如 2023-05-01
				return publishTime.toISOString().split('T')[0];
			}
		},
		
		// 加载更多评论
		loadMore() {
			if (this.isLoading || !this.hasMore) return;
			
			// 增加页码并加载更多数据
			this.page++;
			this.loadPostsFromApi();
		},
		
		// 下拉刷新评论
		refreshComments(e) {
			this.isRefreshing = true;
			this.page = 1;
			this.hasMore = true;
			this.loadPostsFromApi();
		},
		
		// 显示评论输入框
		showCommentInput(commentId) {
			console.log('显示评论输入框，评论ID:', commentId)
			uni.showToast({
				title: '评论功能开发中',
				icon: 'none'
			})
		},
		
		// 分享评论
		shareComment(comment) {
			console.log('分享评论:', comment.id)
			uni.showShareMenu({
				withShareTicket: true,
				success() {
					uni.showToast({
						title: '分享成功',
						icon: 'success'
					});
				}
			});
		}
	}
}
</script>

<style lang="scss">
.page-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background: #f5f5f5;
	position: relative;
}

.header {
	padding: 24rpx 30rpx;
	background: #fff;
	box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
	z-index: 10;
}

.title-area {
	margin-bottom: 24rpx;
	
	.page-title {
		font-size: 46rpx;
		font-weight: bold;
		color: #222;
		letter-spacing: 2rpx;
	}
}

.search-wrapper {
	position: relative;
	width: 100%;
	
	.uni-icons {
		position: absolute;
		left: 24rpx;
		top: 50%;
		transform: translateY(-50%);
		z-index: 1;
	}
}

.search-bar {
	width: 100%;
	height: 80rpx;
	border-radius: 40rpx;
	background: #f6f6f6;
	padding: 0 48rpx 0 62rpx;
	font-size: 28rpx;
	color: #333;
}

.placeholder-style {
	color: #999;
}

.category-tabs {
	white-space: nowrap;
	background: #fff;
	padding: 16rpx 20rpx;
	border-bottom: 1rpx solid #f0f0f0;
	box-shadow: 0 2rpx 6rpx rgba(0,0,0,0.03);
}

.category-item {
	display: inline-block;
	padding: 12rpx 32rpx;
	margin: 0 12rpx;
	font-size: 28rpx;
	color: #666;
	border-radius: 32rpx;
	transition: all 0.3s;
	
	&.active {
		background: #ff2442;
		color: #fff;
		font-weight: 500;
	}
}

.waterfall-scroll {
	flex: 1;
	padding: 20rpx;
}

.waterfall-container {
	display: flex;
	justify-content: space-between;
	width: 94%;
	margin: 0 auto;
}

.waterfall-column {
	width: 48%;
}

.card-item {
	margin-bottom: 24rpx;
	background: #fff;
	border-radius: 16rpx;
	overflow: hidden;
	box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.05);
	transition: all 0.3s;
	width: 100%;
	
	&:active {
		transform: scale(0.98);
	}
}

.card-image {
	width: 100%;
	height: 320rpx; /* 固定高度 */
	border-radius: 16rpx 16rpx 0 0;
	object-fit: cover; /* 确保图片完全填充容器并保持比例 */
}

.card-content {
	padding: 20rpx;
}

.card-title {
	font-size: 28rpx;
	color: #333;
	line-height: 1.5;
	margin-bottom: 16rpx;
	display: -webkit-box;
	-webkit-box-orient: vertical;
	overflow: hidden;
	text-overflow: ellipsis;
	
	&:not(.expanded) {
		-webkit-line-clamp: 4;
		line-clamp: 4;
		max-height: 6em;
	}
}

.expand-control {
	margin-top: 10rpx;
	text-align: right;
	
	.expand-btn {
		font-size: 24rpx;
		color: #ff2442;
		position: relative;
		padding-right: 16rpx;
		
		&::after {
			content: '';
			position: absolute;
			right: 0;
			top: 50%;
			width: 0;
			height: 0;
			border-left: 6rpx solid transparent;
			border-right: 6rpx solid transparent;
			border-top: 6rpx solid #ff2442;
			transform: translateY(-50%);
		}
	}
}

.user-info {
	display: flex;
	align-items: center;
	margin: 20rpx 0;
	
	.user-avatar {
		width: 50rpx;
		height: 50rpx;
		border-radius: 50%;
		margin-right: 12rpx;
	}
	
	.user-name {
		font-size: 24rpx;
		color: #666;
	}
}

.interaction-bar {
	display: flex;
	align-items: center;
	justify-content: flex-end;
	gap: 24rpx;
	
	.action-btn {
		display: flex;
		align-items: center;
		gap: 6rpx;
		
		.count {
			font-size: 24rpx;
			color: #666;
		}
		
		&.like-btn.active {
			.count {
				color: #ff5656;
			}
		}
	}
}

.loading-more {
	text-align: center;
	padding: 30rpx 0;
	color: #999;
	font-size: 26rpx;
	display: flex;
	align-items: center;
	justify-content: center;
	
	.uni-icons {
		margin-right: 12rpx;
	}
}

.floating-button {
	position: fixed;
	right: 40rpx;
	bottom: 100rpx;
	width: 100rpx;
	height: 100rpx;
	border-radius: 50%;
	background: linear-gradient(135deg, #ff2442, #ff6b81);
	display: flex;
	align-items: center;
	justify-content: center;
	box-shadow: 0 4rpx 16rpx rgba(255, 36, 66, 0.3);
	z-index: 100;
	
	&:active {
		transform: scale(0.95);
	}
}
</style>

