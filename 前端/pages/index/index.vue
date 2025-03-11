<template>
	<view class="page-container">
		<!-- 搜索栏 -->
		<view class="search-wrapper">
			<uni-icons type="search" size="20" color="#999"></uni-icons>
			<input 
				type="search" 
				class="search-bar" 
				placeholder="搜索评论"
				placeholder-class="placeholder-style"
			/>
		</view>
		
		<!-- 评论滚动区 -->
		<scroll-view 
			class="comment-scroll"
			scroll-y
			:show-scrollbar="false"
			@scrolltolower="loadMore"
			refresher-enabled
			@refresherrefresh="refreshComments"
		>
			<view class="comment-list">
				<view 
					v-for="comment in comments" 
					:key="comment.id"
					class="comment-item"
					@click="navigateToDetail(comment.id)"
				>
					<view class="comment-left">
						<image 
							class="avatar"
							:src="comment.avatar || '/static/default-avatar.png'"
							mode="aspectFill"
							@error="comment.avatar = '/static/default-avatar.png'"
						></image>
					</view>
					
					<view class="comment-right">
						<text class="nickname">{{ comment.nickname }}</text>
						<text class="publish-time">{{ comment.publishTime }}</text>
						
						<view class="content-box">
							<text 
								class="content-text"
								:class="{expanded: comment.expanded}"
								@click="toggleExpand(comment)"
							>{{ comment.content }}</text>
							
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
								<text 
									v-else
									class="collapse-btn"
									@click.stop="toggleExpand(comment)"
								>收起</text>
							</view>
						</view>
						
						<!-- 互动功能区 -->
						<view class="interaction-bar">
							<button class="action-btn like-btn" :class="{active: comment.isLiked}" @click="toggleLike(comment.id)">
								<text class="iconfont icon-like">♥</text>
								<text class="count" v-if="comment.likeCount > 0">{{ comment.likeCount }}</text>
							</button>
							<button class="action-btn comment-btn" @click="showCommentInput(comment.id)">
								<text class="iconfont icon-comment">💬</text>
								<text class="count" v-if="comment.commentCount > 0">{{ comment.commentCount }}</text>
							</button>
							<button class="action-btn share-btn" @click="shareComment(comment)">
								<text class="iconfont icon-share">↗</text>
							</button>
						</view>
					</view>
				</view>
			</view>
			</scroll-view>
		</view>
	</template>
</template>

<script>
	export default {
		data() {
			return {
				comments: [
					{
						id: 1,
						avatar: '/static/default-avatar.png',
						nickname: '旅行达人',
						content: '这个景点非常值得一去，尤其是日落时分的景色美不胜收！建议下午4点时到达，可以慢慢欣赏天色变化。',
						expanded: false,
						likeCount: 0,
						isLiked: false
					},
					{
						id: 2,
						nickname: '游客007',
						content: '一般般，人太多',
						expanded: false,
						likeCount: 0,
						isLiked: false
					}
				],
				lastClickTime: 0
			}
		},
		onLoad() {

		},
		methods: {
			navigateToDetail(commentId) {
				uni.navigateTo({
					url: '/pages/detail/detail?commentId=' + commentId
				})
			},
			toggleExpand(comment) {
				comment.expanded = !comment.expanded
			},
			showExpandControl(comment) {
				// 简单判断文本长度，实际应通过计算文本高度
				return comment.content.length > 50
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
			// 加载更多评论
			loadMore() {
				// 模拟加载更多数据
				console.log('加载更多评论')
				// 实际项目中应调用API获取下一页数据
				setTimeout(() => {
					const newComments = [
						{
							id: this.comments.length + 1,
							avatar: '/static/default-avatar.png',
							nickname: '新用户' + (this.comments.length + 1),
							content: '这是加载的新评论' + (this.comments.length + 1),
							expanded: false,
							likeCount: 0,
							isLiked: false,
							publishTime: '刚刚',
							commentCount: 0
						}
					]
					this.comments = [...this.comments, ...newComments]
				}, 500)
			},
			// 下拉刷新评论
			refreshComments(e) {
				console.log('刷新评论列表')
				// 模拟刷新数据
				setTimeout(() => {
					// 重置评论数据
					this.comments = [
						{
							id: 1,
							avatar: '/static/default-avatar.png',
							nickname: '旅行达人',
							content: '这个景点非常值得一去，尤其是日落时分的景色美不胜收！建议下午4点时到达，可以慢慢欣赏天色变化。',
							expanded: false,
							likeCount: Math.floor(Math.random() * 10),
							isLiked: false,
							publishTime: '刚刚更新',
							commentCount: 2
						},
						{
							id: 2,
							nickname: '游客007',
							avatar: '/static/default-avatar.png',
							content: '一般般，人太多',
							expanded: false,
							likeCount: Math.floor(Math.random() * 5),
							isLiked: false,
							publishTime: '刚刚更新',
							commentCount: 1
						}
					]
					// 停止下拉刷新动画
					uni.stopPullDownRefresh()
					e.stopPullDownRefresh()
				}, 1000)
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
				uni.showToast({
					title: '分享功能开发中',
					icon: 'none'
				})
			}
		}
	}
</script>

<style lang="scss">
.page-container {
	display: flex;
	flex-direction: column;
	height: 100vh;
	background: #f8f8f8;
}

.search-wrapper {
	position: relative;
	width: 92%;
	margin: 16px auto;
	
	.uni-icons {
		position: absolute;
		left: 16px;
		top: 50%;
		transform: translateY(-50%);
		z-index: 1;
	}
}

.search-bar {
	width: 100%;
	height: 44px;
	border-radius: 22px;
	background: #fff;
	padding: 0 48px;
	font-size: 14px;
	box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.comment-scroll {
	flex: 1;
	height: calc(100vh - 76px);
}

.comment-list {
	padding: 8px 4%;
}

.comment-item {
	margin-bottom: 16px;
	background: #fff;
	border-radius: 16px;
	box-shadow: 0 2px 12px rgba(0,0,0,0.08);
	padding: 16px;
	transform: translateZ(0);
	transition: transform 0.2s;
	position: relative;
	
	&:active {
		transform: translateZ(0) scale(0.98);
	}
}

.comment-left {
	width: 20%;
	padding: 8px;
	
	.avatar {
		width: 48px;
		height: 48px;
		border-radius: 24px;
		background: #eee;
	}
}

.comment-right {
	width: 80%;
	padding-left: 8px;
	padding-right: 20px;
	
	.nickname {
		font-size: 16px;
		color: #333;
		margin-bottom: 4px;
		display: block;
		font-weight: 500;
	}
	
	.publish-time {
		font-size: 12px;
		color: #999;
		margin-bottom: 8px;
		display: block;
	}
}

.content-box {
	position: relative;
	
	.content-text {
		display: -webkit-box;
		-webkit-box-orient: vertical;
		overflow: hidden;
		text-overflow: ellipsis;
		line-height: 1.5em;
		font-size: 14px;
		color: #666;
		
		&:not(.expanded) {
			-webkit-line-clamp: 3;
			line-clamp: 3;
			max-height: 4.5em;
		}
	}
}

.expand-control {
	position: relative;
	margin-top: 8px;
	text-align: right;
	
	.expand-btn {
		position: absolute;
		bottom: 0;
		right: 0;
		padding: 4px 12px;
		background: linear-gradient(90deg, transparent, #fff 30%);
		color: #007AFF;
		font-size: 12px;
		border-radius: 4px;
	}
	
	.collapse-btn {
		display: inline-block;
		padding: 4px 12px;
		background: #007AFF;
		color: white;
		border-radius: 4px;
		font-size: 12px;
	}
}

.placeholder-style {
	color: #999;
}

/* 点赞容器样式 */
.interaction-bar {
	position: absolute;
	bottom: 8px;
	right: 12px;
	display: flex;
	align-items: center;
	gap: 8px;
	
	.action-btn {
		display: flex;
		align-items: center;
		gap: 2px;
		background: transparent;
		border: none;
		padding: 4px;
		cursor: pointer;
		height: 24px;
		
		.iconfont {
			font-size: 14px;
			color: #666;
			transition: all 0.2s;
		}
		
		.count {
			font-size: 12px;
			color: #666;
			transition: color 0.2s;
		}
		
		&.like-btn.active {
			.iconfont {
				color: #ff5656;
			}
			.count {
				color: #ff5656;
			}
		}
		
		&:active {
			transform: scale(0.9);
		}
	}
}
</style>
