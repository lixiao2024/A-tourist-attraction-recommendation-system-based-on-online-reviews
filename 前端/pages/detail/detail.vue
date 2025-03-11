<template>
    <view class="detail-container">
      <!-- 主评论区域 -->
      <scroll-view class="main-comment" scroll-y>
        <view class="comment-card">
          <image class="avatar" :src="detail.avatar" mode="aspectFill"></image>
          <view class="content-box">
            <text class="nickname">{{ detail.nickname }}</text>
            <text class="publish-time">{{ detail.publishTime }}</text>
            <text class="content-text">{{ detail.content }}</text>
            
            <!-- 互动功能区 -->
            <view class="interaction-bar">
              <button class="action-btn like-btn" :class="{active: detail.isLiked}" @click="toggleLike">
                <text class="iconfont icon-like">♥</text>
                <text class="count" v-if="detail.likeCount > 0">{{ detail.likeCount }}</text>
              </button>
              <button class="action-btn comment-btn" @click="showCommentInput">
                <text class="iconfont icon-comment">💬</text>
                <text class="count" v-if="detail.commentCount > 0">{{ detail.commentCount }}</text>
              </button>
              <button class="action-btn collect-btn" :class="{active: detail.isCollected}" @click="toggleCollect">
                <text class="iconfont icon-star">★</text>
                <text class="count" v-if="detail.collectCount > 0">{{ detail.collectCount }}</text>
              </button>
              <button class="action-btn follow-btn" :class="{active: detail.isFollowed}" @click="toggleFollow">
                <text class="iconfont icon-follow">+</text>
              </button>
            </view>
          </view>
        </view>
      </scroll-view>
  
      <!-- 回复列表区域 -->
      <scroll-view class="reply-list" scroll-y @scrolltolower="onScrollToLower">
        <view v-for="reply in replies" :key="reply.id" class="reply-item">
          <image class="reply-avatar" :src="reply.avatar" mode="aspectFill"></image>
          <view class="reply-content">
            <text class="reply-nickname">{{ reply.nickname }}</text>
            <text class="reply-text">{{ reply.content }}</text>
            <text class="reply-time">{{ reply.publishTime }}</text>
          </view>
        </view>
      </scroll-view>
      
      <!-- 评论输入框 -->
      <view class="comment-input-area" v-if="showCommentBox">
        <input 
          class="comment-input" 
          v-model="replyContent" 
          placeholder="写下你的评论..."
          focus
          confirm-type="send"
          @confirm="submitComment"
        />
        <button class="send-btn" @click="submitComment">发送</button>
      </view>
    </view>
  </template>
  
  <script>
  export default {
    data() {
      return {
        commentId: null,
        detail: {
          id: 1,
          avatar: '/static/default-avatar.png',
          nickname: '旅行达人',
          content: '这个景点非常值得一去，尤其是日落时分的景色美不胜收！建议下午4点时到达，可以慢慢欣赏天色变化。',
          publishTime: '3小时前',
          likeCount: 12,
          commentCount: 5,
          collectCount: 3,
          isLiked: false,
          isCollected: false,
          isFollowed: false
        },
        replies: [
          {
            id: 1,
            avatar: '/static/default-avatar.png',
            nickname: '用户A',
            content: '感谢分享！周末就去看看',
            publishTime: '1小时前'
          }
        ],
        page: 1,
        pageSize: 10,
        hasMore: true,
        loading: false,
        showCommentBox: false,
        replyContent: ''
      };
    },
    onLoad(options) {
      // 获取传递的评论ID参数
      this.commentId = options.commentId || null;
      if (this.commentId) {
        this.loadCommentDetail();
        this.loadReplies();
      }
      
      // 检查用户状态
      this.checkUserInteractionStatus();
    },
    methods: {
      // 加载评论详情
      loadCommentDetail() {
        // 模拟API请求，实际项目中应替换为真实接口调用
        console.log('加载评论ID:', this.commentId);
        // 这里模拟根据ID获取不同的评论详情
        if (this.commentId == 2) {
          this.detail = {
            id: 2,
            avatar: '/static/default-avatar.png',
            nickname: '游客007',
            content: '一般般，人太多',
            publishTime: '5小时前',
            likeCount: 5,
            commentCount: 2,
            collectCount: 1,
            isLiked: false,
            isCollected: false,
            isFollowed: false
          };
        }
        // 其他ID保持默认数据
      },
      
      // 加载回复列表
      loadReplies() {
        if (this.loading || !this.hasMore) return;
        
        this.loading = true;
        
        // 模拟API请求延迟
        setTimeout(() => {
          // 模拟分页数据
          if (this.commentId == 2) {
            // 为ID为2的评论添加特定回复
            if (this.page === 1) {
              this.replies = [
                {
                  id: 2,
                  avatar: '/static/default-avatar.png',
                  nickname: '本地用户',
                  content: '同意，周末人确实很多',
                  publishTime: '2小时前'
                }
              ];
            } else {
              // 第二页没有更多数据
              this.hasMore = false;
            }
          } else if (this.page > 1) {
            // 为其他评论ID模拟加载更多数据
            const moreReplies = [
              {
                id: this.replies.length + 1,
                avatar: '/static/default-avatar.png',
                nickname: '用户' + (this.page + 1),
                content: '这是加载的第' + this.page + '页回复',
                publishTime: Math.floor(Math.random() * 24) + '小时前'
              }
            ];
            
            this.replies = [...this.replies, ...moreReplies];
            
            // 模拟数据到第3页结束
            if (this.page >= 3) {
              this.hasMore = false;
            }
          }
          
          this.page++;
          this.loading = false;
        }, 500);
      },
      
      // 滚动到底部加载更多
      onScrollToLower() {
        if (!this.loading && this.hasMore) {
          this.loadReplies();
        }
      },
      
      // 检查用户交互状态
      checkUserInteractionStatus() {
        // 从本地存储获取用户交互状态
        const userInfo = uni.getStorageSync('userInfo');
        if (!userInfo) return;
        
        // 获取用户的点赞、收藏、关注状态
        const likedPosts = uni.getStorageSync('likedPosts') || [];
        const collectedPosts = uni.getStorageSync('collectedPosts') || [];
        const followedUsers = uni.getStorageSync('followedUsers') || [];
        
        // 更新当前帖子状态
        this.detail.isLiked = likedPosts.includes(this.detail.id);
        this.detail.isCollected = collectedPosts.includes(this.detail.id);
        this.detail.isFollowed = followedUsers.includes(this.detail.nickname);
      },
      
      // 点赞功能
      toggleLike() {
        if (!this.checkLoginStatus()) return;
        
        // 更新点赞状态
        this.detail.isLiked = !this.detail.isLiked;
        
        // 更新点赞数量
        if (this.detail.isLiked) {
          this.detail.likeCount++;
          this.updateUserStats('获赞', 1);
        } else {
          this.detail.likeCount--;
          this.updateUserStats('获赞', -1);
        }
        
        // 保存点赞状态到本地
        this.saveInteractionStatus('likedPosts', this.detail.id, this.detail.isLiked);
        
        // 提示用户
        uni.showToast({
          title: this.detail.isLiked ? '已点赞' : '已取消点赞',
          icon: 'none'
        });
      },
      
      // 收藏功能
      toggleCollect() {
        if (!this.checkLoginStatus()) return;
        
        // 更新收藏状态
        this.detail.isCollected = !this.detail.isCollected;
        
        // 更新收藏数量
        if (this.detail.isCollected) {
          this.detail.collectCount++;
          this.updateUserStats('收藏', 1);
        } else {
          this.detail.collectCount--;
          this.updateUserStats('收藏', -1);
        }
        
        // 保存收藏状态到本地
        this.saveInteractionStatus('collectedPosts', this.detail.id, this.detail.isCollected);
        
        // 提示用户
        uni.showToast({
          title: this.detail.isCollected ? '已收藏' : '已取消收藏',
          icon: 'none'
        });
      },
      
      // 关注功能
      toggleFollow() {
        if (!this.checkLoginStatus()) return;
        
        // 更新关注状态
        this.detail.isFollowed = !this.detail.isFollowed;
        
        // 更新用户统计数据
        if (this.detail.isFollowed) {
          this.updateUserStats('关注', 1);
          this.updateAuthorStats('粉丝', 1);
        } else {
          this.updateUserStats('关注', -1);
          this.updateAuthorStats('粉丝', -1);
        }
        
        // 保存关注状态到本地
        this.saveInteractionStatus('followedUsers', this.detail.nickname, this.detail.isFollowed);
        
        // 提示用户
        uni.showToast({
          title: this.detail.isFollowed ? '已关注' : '已取消关注',
          icon: 'none'
        });
      },
      
      // 显示评论输入框
      showCommentInput() {
        if (!this.checkLoginStatus()) return;
        this.showCommentBox = true;
      },
      
      // 提交评论
      submitComment() {
        if (!this.replyContent.trim()) {
          uni.showToast({
            title: '评论内容不能为空',
            icon: 'none'
          });
          return;
        }
        
        // 获取用户信息
        const userInfo = uni.getStorageSync('userInfo') || {
          nickname: '游客',
          avatar: '/static/default-avatar.png'
        };
        
        // 创建新评论
        const newReply = {
          id: this.replies.length + 1,
          avatar: userInfo.avatar,
          nickname: userInfo.nickname,
          content: this.replyContent,
          publishTime: '刚刚'
        };
        
        // 添加到评论列表
        this.replies.unshift(newReply);
        
        // 更新评论数
        this.detail.commentCount++;
        
        // 清空输入框并隐藏
        this.replyContent = '';
        this.showCommentBox = false;
        
        // 提示用户
        uni.showToast({
          title: '评论成功',
          icon: 'success'
        });
      },
      
      // 检查登录状态
      checkLoginStatus() {
        const userInfo = uni.getStorageSync('userInfo');
        if (!userInfo) {
          uni.showToast({
            title: '请先登录',
            icon: 'none'
          });
          return false;
        }
        return true;
      },
      
      // 保存交互状态到本地
      saveInteractionStatus(key, id, status) {
        let items = uni.getStorageSync(key) || [];
        
        if (status) {
          // 添加ID到列表
          if (!items.includes(id)) {
            items.push(id);
          }
        } else {
          // 从列表中移除ID
          items = items.filter(item => item !== id);
        }
        
        uni.setStorageSync(key, items);
      },
      
      // 更新用户统计数据
      updateUserStats(type, value) {
        // 获取用户统计数据
        let statsData = uni.getStorageSync('userStatsData') || [
          { label: '粉丝', value: 0 },
          { label: '获赞', value: 0 },
          { label: '关注', value: 0 },
          { label: '收藏', value: 0 }
        ]
        
        // 查找并更新对应类型的统计数据
        const statItem = statsData.find(item => item.label === type);
        if (statItem) {
          statItem.value += value;
          if (statItem.value < 0) statItem.value = 0;
        }
        
        // 保存更新后的统计数据
        uni.setStorageSync('userStatsData', statsData);
      },
      
      // 更新作者统计数据
      updateAuthorStats(type, value) {
        // 获取作者统计数据
        let authorStatsData = uni.getStorageSync(`authorStats_${this.detail.nickname}`) || [
          { label: '粉丝', value: 0 },
          { label: '获赞', value: 0 }
        ];
        
        // 查找并更新对应类型的统计数据
        const statItem = authorStatsData.find(item => item.label === type);
        if (statItem) {
          statItem.value += value;
          if (statItem.value < 0) statItem.value = 0;
        }
        
        // 保存更新后的统计数据
        uni.setStorageSync(`authorStats_${this.detail.nickname}`, authorStatsData);
      }
    }
  };
  </script>
  
  <style lang="scss">
  .detail-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #f8fafc;
    
    .main-comment {
      flex: 1;
      padding: 24rpx;
      border-bottom: 1px solid rgba(0,0,0,0.05);
      position: relative;
      
      &:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 15%;
        right: 15%;
        height: 1px;
        background: linear-gradient(to right, transparent, rgba(0,0,0,0.1), transparent);
      }
  
      .comment-card {
        display: flex;
        padding: 36rpx;
        background: #fff;
        border-radius: 24rpx;
        box-shadow: 0 4rpx 24rpx rgba(0, 0, 0, 0.04);
        margin-bottom: 24rpx;
        transition: all 0.3s ease;
  
        .avatar {
          width: 96rpx;
          height: 96rpx;
          border-radius: 48rpx;
          margin-right: 28rpx;
          border: 4rpx solid #fff;
          box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.08);
        }
  
        .content-box {
          flex: 1;
  
          .nickname {
            font-size: 34rpx;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 8rpx;
            letter-spacing: 0.5rpx;
          }
  
          .publish-time {
            font-size: 24rpx;
            color: #999;
            margin-bottom: 16rpx;
          }
  
          .content-text {
            font-size: 32rpx;
            color: #2d3748;
            line-height: 1.7;
            margin: 20rpx 0;
            letter-spacing: 0.5rpx;
          }
          
          .interaction-bar {
            display: flex;
            align-items: center;
            gap: 28rpx;
            margin-top: 24rpx;
            
            .action-btn {
              display: flex;
              align-items: center;
              gap: 8rpx;
              background: rgba(247, 250, 252, 0.8);
              border: none;
              padding: 14rpx 24rpx;
              border-radius: 36rpx;
              transition: all 0.25s ease;
              
              &:active {
                transform: scale(0.95);
              }
              
              &.like-btn.active {
                background: rgba(255, 86, 86, 0.1);
                .iconfont, .count {
                  color: #ff5656;
                }
              }
              
              &.collect-btn.active {
                background: rgba(255, 193, 7, 0.1);
                .iconfont, .count {
                  color: #ffc107;
                }
              }
              
              &.follow-btn.active {
                background: rgba(0, 122, 255, 0.1);
                .iconfont {
                  color: #007AFF;
                }
              }
              
              .iconfont {
                font-size: 34rpx;
                color: #4a5568;
              }
              
              .count {
                font-size: 26rpx;
                color: #4a5568;
                font-weight: 500;
              }
            }
          }
        }
      }
    }
  
    .reply-list {
      flex: 2;
      padding: 28rpx;
      position: relative;
      
      &:before {
        content: '';
        position: absolute;
        top: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80rpx;
        height: 6rpx;
        background: #e2e8f0;
        border-radius: 3rpx;
        margin-top: 10rpx;
      }
      background: #f1f5f9;
  
      .reply-item {
        display: flex;
        padding: 28rpx;
        margin-bottom: 24rpx;
        background: #fff;
        border-radius: 20rpx;
        box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.03);
        transition: transform 0.25s ease;
        
        &:active {
          transform: translateX(4rpx);
        }
  
        .reply-avatar {
          width: 68rpx;
          height: 68rpx;
          border-radius: 34rpx;
          margin-right: 20rpx;
          border: 2rpx solid #fff;
        }
  
        .reply-content {
          flex: 1;
  
          .reply-nickname {
            font-size: 28rpx;
            font-weight: 600;
            color: #1a202c;
            margin-bottom: 8rpx;
            letter-spacing: 0.3rpx;
          }
  
          .reply-text {
            font-size: 28rpx;
            color: #4a5568;
            margin-bottom: 10rpx;
            line-height: 1.5;
          }
  
          .reply-time {
            font-size: 22rpx;
            color: #95a5a6;
            font-style: italic;
          }
        }
      }
    }
    
    .comment-input-area {
      display: flex;
      padding: 28rpx 36rpx;
      background: #fff;
      border-top: 1px solid #e2e8f0;
      box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.04);
      
      .comment-input {
        flex: 1;
        height: 80rpx;
        background: #f1f5f9;
        border-radius: 40rpx;
        padding: 0 32rpx;
        font-size: 30rpx;
        color: #2d3748;
        transition: all 0.3s ease;
        box-shadow: inset 0 1rpx 3rpx rgba(0, 0, 0, 0.08);
        
        &:focus {
          background: #fff;
          box-shadow: inset 0 1rpx 5rpx rgba(0, 0, 0, 0.15);
        }
        margin-right: 20rpx;
      }
      
      .send-btn {
        width: 160rpx;
        height: 80rpx;
        line-height: 80rpx;
        text-align: center;
        background: linear-gradient(135deg, #3182ce, #0056b3);
        color: #fff;
        border-radius: 40rpx;
        font-size: 30rpx;
        font-weight: 500;
        transition: all 0.3s ease;
        
        &:active {
          transform: scale(0.95);
          background: linear-gradient(135deg, #0056b3, #007AFF);
        }
      }
    }
  }
  </style>