<template>
	<view class="page-container">
		<!-- 顶部搜索和标题 -->
		<view class="header">
			<view class="title-area">
				<text class="page-title">探索·灵感</text>
				<text class="recommendation-hint" v-if="isLoggedIn">基于您的兴趣为您推荐</text>
			</view>
			<view class="search-wrapper">
				<uni-icons type="search" size="20" color="#999"></uni-icons>
				<input 
					type="search" 
					class="search-bar" 
					placeholder="搜索目的地、景点、攻略"
					placeholder-class="placeholder-style"
					disabled
					@click="navigateToSearch"
				/>
			</view>
		</view>
		
		<!-- 使用瀑布流组件 -->
		<waterfall-flow
			:is-loading="isLoading"
			:is-refreshing="isRefreshing"
			:has-more="hasMore"
			:isEmpty="comments.length === 0"
			@load-more="loadMore"
			@refresh="refreshComments"
		>
			<!-- 左侧列 -->
			<template #left-column>
				<travel-note-card
						v-for="comment in leftColumn" 
						:key="comment.id"
					:note="comment"
					@card-click="navigateToDetail"
					@like="toggleLike"
					@comment="showCommentInput"
					@share="shareComment"
				/>
			</template>
							
			<!-- 右侧列 -->
			<template #right-column>
				<travel-note-card
						v-for="comment in rightColumn" 
						:key="comment.id"
					:note="comment"
					@card-click="navigateToDetail"
					@like="toggleLike"
					@comment="showCommentInput"
					@share="shareComment"
				/>
			</template>
		</waterfall-flow>
		
		<!-- 悬浮发布按钮 -->
		<view class="floating-button" @click="navigateToPublish">
			<uni-icons type="plusempty" size="24" color="#fff"></uni-icons>
		</view>
	</view>
</template>

<script>
import { getRecommendedPosts } from '@/request/api.js'
import TravelNoteCard from '@/components/TravelNoteCard.vue'
import WaterfallFlow from '@/components/WaterfallFlow.vue'

export default {
	components: {
		TravelNoteCard,
		WaterfallFlow
	},
	data() {
		return {
			comments: [],
			lastClickTime: 0,
			isRefreshing: false,
			isLoading: false,
			page: 1,
			pageSize: 15,
			hasMore: true,
			isLoggedIn: false,
			requestCount: 0  // 添加请求计数器
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
		// 检查用户登录状态
		this.checkLoginStatus();
		// 初始加载数据
		this.loadPostsFromApi();
		// 检查用户是否设置过兴趣标签 - 只在首次登录时检查一次
		// this.checkUserInterests();
	},
	
	// 支持页面滚动到底部的生命周期
	onReachBottom() {
		console.log('页面滚动到底部触发 onReachBottom');
		// 调用加载更多方法
		this.loadMore();
	},
	
	// 支持页面下拉刷新的生命周期
	onPullDownRefresh() {
		console.log('页面下拉刷新触发 onPullDownRefresh');
		// 调用刷新方法
		this.refreshComments();
	},
	
	methods: {
		// 检查用户是否设置过兴趣标签 - 只在首次登录时调用，不再每次刷新都调用
		checkUserInterests() {
			// 只有在登录状态下才检查
			if (this.isLoggedIn) {
				// 检查本地是否有兴趣标签配置记录
				const hasSetInterests = uni.getStorageSync('has_set_interests');
				
				// 如果没有设置过，提示用户去设置
				if (!hasSetInterests) {
					setTimeout(() => {
						uni.showModal({
							title: '完善您的兴趣',
							content: '设置您感兴趣的景点和城市，我们将为您推荐相关内容',
							confirmText: '去设置',
							cancelText: '稍后',
							success: (res) => {
								if (res.confirm) {
									// 导航到兴趣设置页面
									uni.navigateTo({
										url: '/pages/mine/interests'
									});
								} else {
									// 稍后提醒，先标记为已提示过
									uni.setStorageSync('interests_reminded', true);
								}
							}
						});
					}, 1500);
				}
			}
		},
		
		// 检查用户登录状态
		checkLoginStatus() {
			const token = uni.getStorageSync('token');
			this.isLoggedIn = !!token;
			
			// 只在用户首次登录时检查兴趣设置
			if (this.isLoggedIn) {
				const isFirstLogin = !uni.getStorageSync('login_checked');
				if (isFirstLogin) {
					// 标记已检查登录状态
					uni.setStorageSync('login_checked', true);
					// 检查用户是否设置过兴趣标签
					this.checkUserInterests();
				}
			}
		},
		
		// 前往登录页
		goToLogin() {
			uni.navigateTo({
				url: '/pages/login/login'
			});
		},
		
		navigateToDetail(commentId) {
			uni.navigateTo({
				url: '/pages/detail/detail?id=' + commentId
			})
		},
		
		navigateToPublish() {
			// 如果用户未登录，提示登录
			if (!this.isLoggedIn) {
				uni.showToast({
					title: '请先登录后再发布',
					icon: 'none'
				});
				setTimeout(() => {
					this.goToLogin();
				}, 1500);
				return;
			}
			
			uni.navigateTo({
				url: '/pages/post/post'
			});
		},
		
		toggleLike(commentId) {
			// 如果用户未登录，提示登录
			if (!this.isLoggedIn) {
				uni.showToast({
					title: '请先登录后再点赞',
					icon: 'none'
				});
				setTimeout(() => {
					this.goToLogin();
				}, 1500);
				return;
			}
			
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
		
		// 加载更多评论
		loadMore() {
			if (this.isLoading || !this.hasMore) {
				console.log('加载更多被阻止:', this.isLoading ? '正在加载中' : '没有更多数据');
				return;
			}
			
			console.log('触发加载更多，当前页码:', this.page, '是否还有更多:', this.hasMore);
			
			// 增加页码并加载更多数据
			this.page++;
			this.loadPostsFromApi();
		},
		
		// 下拉刷新评论
		refreshComments(e) {
			if (this.isRefreshing) {
				console.log('已经在刷新中，忽略重复刷新请求');
				return;
			}
			
			console.log('触发下拉刷新');
			this.isRefreshing = true;
			this.page = 1;
			this.hasMore = true;
			// 下拉刷新时显示提示
			uni.showToast({
				title: '正在为您推荐新内容',
				icon: 'none',
				duration: 1500
			});
			// 强制设置刷新标志
			this.loadPostsFromApi(true);
		},
		
		// 从API加载博文数据
		async loadPostsFromApi(forceRefresh = false) {
			// 增加请求计数，用于调试
			const requestId = ++this.requestCount;
			
			try {
				if (this.isLoading) {
					console.log(`[请求${requestId}] 已有请求正在进行中，忽略本次请求`);
					return;
				}
				
				this.isLoading = true;
				console.log(`[请求${requestId}] 开始加载数据，页码:${this.page}, 强制刷新:${forceRefresh}`);
				
				uni.showLoading({
					title: '加载中...'
				});
				
				let skip = (this.page - 1) * this.pageSize;
				
				// 判断是否为刷新操作，强制刷新或页面刷新都算
				let isRefresh = forceRefresh || (this.page === 1 && this.isRefreshing);
				
				console.log(`[请求${requestId}] 参数 - skip:${skip}, limit:${this.pageSize}, isRefresh:${isRefresh}`);
				
				// 调用API获取数据
				let result;
				try {
					// 只使用推荐API
						console.log(`[请求${requestId}] 使用推荐API获取数据`);
						result = await getRecommendedPosts(skip, this.pageSize, isRefresh);
					console.log(`[请求${requestId}] 获取到博文数据:${Array.isArray(result) ? result.length : 0}条`);
				} catch (apiError) {
					console.error(`[请求${requestId}] API请求失败:`, apiError);
					throw apiError;
				}
				
				if (result && Array.isArray(result)) {
					// 转换数据格式以适应前端展示
					const posts = result.map(post => {
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
							// 处理图片数组，确保格式正确
							images: this.processImages(post),
							// 添加情感分析类型: positive(种草) 或 negative(避雷)
							sentimentType: post.sentiment_type || null
						};
					});
					
					console.log(`[请求${requestId}] 处理后的博文数据:${posts.length}条, 当前页码:${this.page}`);
					
					if (posts.length === 0) {
						console.log(`[请求${requestId}] 服务器返回空数据`);
						this.hasMore = false;
						
						// 如果是第一页且没有数据，加载默认数据
						if (this.page === 1) {
							if (!isRefresh || forceRefresh) {
								console.log(`[请求${requestId}] 首页无数据，加载默认内容`);
								this.loadDefaultData();
							}
						}
						
						if (isRefresh) {
							uni.showToast({
								title: '暂无新内容，请稍后再试',
								icon: 'none'
							});
						}
					} else {
						// 如果是第一页，替换数据；否则追加数据
						if (this.page === 1) {
							this.comments = posts;
							console.log(`[请求${requestId}] 替换全部数据，新数据量:${posts.length}`);
						} else {
							this.comments = [...this.comments, ...posts];
							console.log(`[请求${requestId}] 追加数据，当前总数据量:${this.comments.length}`);
						}
						
						// 判断是否还有更多数据
						this.hasMore = posts.length >= this.pageSize;
						
						if (posts.length < this.pageSize) {
							console.log(`[请求${requestId}] 返回数据少于每页条数(${posts.length}<${this.pageSize})，已无更多数据`);
							this.hasMore = false;
						}
					}
				} else {
					console.log(`[请求${requestId}] 返回非数组结果或空结果`);
					
					if (this.page === 1) {
						// 如果没有数据，显示默认模拟数据
						console.log(`[请求${requestId}] 首页加载失败，使用默认数据`);
						this.loadDefaultData();
					}
					this.hasMore = false;
				}
				
				console.log(`[请求${requestId}] 请求完成，还有更多数据:${this.hasMore}, 总数据量:${this.comments.length}`);
			} catch (error) {
				console.error(`[请求${requestId}] 加载博文数据失败:`, error);
				// 出错时加载默认数据
				if (this.page === 1 && (!this.comments || this.comments.length === 0)) {
					console.log(`[请求${requestId}] 请求出错，加载默认数据`);
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
					console.log(`[请求${requestId}] 刷新完成，停止下拉刷新`);
				}
			}
		},
		
		// 添加处理图片的辅助方法
		processImages(post) {
			// 首先检查是否有完整的images数组可用
			if (post.images && Array.isArray(post.images) && post.images.length > 0) {
				return post.images;
			} 
			// 然后检查是否有封面图
			else if (post.cover_image) {
				return [post.cover_image];
			}
			// 最后返回空数组
			return [];
		},
		
		// 加载默认模拟数据
		loadDefaultData() {
			// 只提供推荐数据
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
						images: ['/static/demo/scenic1.jpg'],
						sentimentType: 'positive'
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
						images: ['/static/demo/scenic2.jpg'],
						sentimentType: 'positive'
					}
				];
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
		
		// 显示评论输入框
		showCommentInput(commentId) {
			// 如果用户未登录，提示登录
			if (!this.isLoggedIn) {
				uni.showToast({
					title: '请先登录后再评论',
					icon: 'none'
				});
				setTimeout(() => {
					this.goToLogin();
				}, 1500);
				return;
			}
			
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
		},
		
		// 导航到搜索页面
		navigateToSearch() {
			uni.navigateTo({
				url: '/pages/search/search'
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
	
	.recommendation-hint {
		font-size: 24rpx;
		color: #ff6b81;
		margin-left: 20rpx;
		background-color: rgba(255, 107, 129, 0.1);
		padding: 4rpx 12rpx;
		border-radius: 16rpx;
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

