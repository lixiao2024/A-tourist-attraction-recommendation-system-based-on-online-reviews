<template>
    <view class="container">
      <!-- 主评论区域 -->
      <view class="comment-section">
        <view class="comment-card" v-if="isDataLoaded">
          <view class="user-info">
            <image class="avatar" :src="detail.avatar" mode="aspectFill"></image>
            <view class="user-meta">
              <text class="nickname">{{ detail.nickname }}</text>
              <text class="publish-time">{{ detail.publishTime }}</text>
            </view>
          </view>
          
          <view class="content-wrapper">
            <text class="content-text">{{ detail.content }}</text>
            
            <!-- 添加图片展示 -->
            <view class="images-container" v-if="detail.images && detail.images.length > 0">
              <image 
                v-for="(image, index) in detail.images" 
                :key="index"
                :src="image" 
                mode="widthFix" 
                class="content-image"
                @tap="previewImage(image, detail.images)"
                @error="handleImageError(index)"
              ></image>
            </view>
          </view>
          
          <!-- 互动功能区 -->
          <view class="interaction-bar">
            <view class="interaction-button" :class="{active: detail.isLiked}" @click="toggleLike">
              <uni-icons :type="detail.isLiked ? 'heart-filled' : 'heart'" size="24" :color="detail.isLiked ? '#ff5656' : '#666'"></uni-icons>
              <text class="button-text" :class="{active: detail.isLiked}">{{ detail.likeCount > 0 ? detail.likeCount : '点赞' }}</text>
            </view>
            
            <view class="interaction-button" @click="showCommentInput">
              <uni-icons type="chatbubble" size="24" color="#666"></uni-icons>
              <text class="button-text">{{ detail.commentCount > 0 ? detail.commentCount : '评论' }}</text>
            </view>
            
            <view class="interaction-button" :class="{active: detail.isCollected}" @click="toggleCollect">
              <uni-icons :type="detail.isCollected ? 'star-filled' : 'star'" size="24" :color="detail.isCollected ? '#ffc107' : '#666'"></uni-icons>
              <text class="button-text" :class="{active: detail.isCollected}">{{ detail.isCollected ? '已收藏' : '收藏' }}</text>
            </view>
            
            <view class="interaction-button" :class="{active: detail.isFollowed}" @click="toggleFollow">
              <uni-icons :type="detail.isFollowed ? 'plusempty' : 'plus'" size="24" :color="detail.isFollowed ? '#3182ce' : '#666'"></uni-icons>
              <text class="button-text" :class="{active: detail.isFollowed}">{{ detail.isFollowed ? '已关注' : '关注' }}</text>
            </view>
          </view>
        </view>
        
        <view class="loading-indicator" v-if="!isDataLoaded">
          <uni-icons type="spinner-cycle" size="30" color="#3182ce"></uni-icons>
          <text class="loading-text">加载中...</text>
        </view>
      </view>
  
      <!-- 评论列表标题 -->
      <view class="replies-header">
        <text class="replies-title">全部评论 ({{ detail.commentCount || 0 }})</text>
        <text class="sort-button">最新</text>
      </view>
  
      <!-- 回复列表区域 -->
      <scroll-view 
        class="reply-list" 
        scroll-y 
        @scrolltolower="onScrollToLower"
        :refresher-enabled="true"
        @refresherrefresh="refreshComments"
        :refresher-triggered="isRefreshing"
      >
        <view class="reply-container" v-if="replies.length > 0">
          <view 
            v-for="(reply, index) in replies" 
            :key="reply.id" 
            class="reply-item"
            :class="{'reply-item-hover': replyHoverId === reply.id}"
            hover-class="reply-item-hover"
            @touchstart="replyHoverId = reply.id"
            @touchend="replyHoverId = null"
          >
            <image class="reply-avatar" :src="reply.avatar" mode="aspectFill"></image>
            <view class="reply-content">
              <view class="reply-header">
                <text class="reply-nickname">{{ reply.nickname }}</text>
                <text class="reply-time">{{ reply.publishTime }}</text>
              </view>
              <text class="reply-text">{{ reply.content }}</text>
              <view class="reply-actions">
                <view class="reply-like" @click.stop="toggleReplyLike(index)">
                  <uni-icons :type="reply.isLiked ? 'heart-filled' : 'heart'" size="16" :color="reply.isLiked ? '#ff5656' : '#999'"></uni-icons>
                  <text :class="{'liked-text': reply.isLiked}">{{ reply.likeCount || '点赞' }}</text>
                </view>
                <view class="reply-comment" @click.stop="replyToComment(reply)">
                  <uni-icons type="chatbubble" size="16" color="#999"></uni-icons>
                  <text>回复</text>
                </view>
              </view>
            </view>
          </view>
        </view>
        
        <view v-else-if="!loading" class="empty-replies">
          <uni-icons type="info" size="60" color="#cccccc"></uni-icons>
          <text class="empty-text">暂无评论，快来发表第一条评论吧</text>
        </view>
        
        <view class="loading-more" v-if="loading">
          <uni-icons type="spinner-cycle" size="20" color="#999"></uni-icons>
          <text>加载中...</text>
        </view>
        
        <view class="no-more" v-if="!hasMore && replies.length > 0">
          <text>没有更多评论了</text>
        </view>
      </scroll-view>
      
      <!-- 评论输入框 -->
      <view class="comment-input-area" v-if="showCommentBox">
        <view class="input-wrapper">
          <input 
            class="comment-input" 
            v-model="replyContent" 
            :placeholder="replyPlaceholder"
            focus
            cursor-spacing="20"
            confirm-type="send"
            maxlength="200"
            @confirm="submitComment"
          />
          <text class="word-count">{{ replyContent.length }}/200</text>
        </view>
        <button 
          class="send-btn" 
          :class="{'send-btn-active': replyContent.trim().length > 0}"
          :disabled="replyContent.trim().length === 0"
          @click="submitComment"
        >发送</button>
      </view>
      
      <!-- 底部评论按钮 -->
      <view class="bottom-comment-btn" v-if="!showCommentBox" @click="showCommentInput">
        <uni-icons type="chatboxes" size="20" color="#FFFFFF"></uni-icons>
        <text>写评论...</text>
      </view>
      
      <!-- 登录弹窗 -->
      <view class="login-modal" v-if="showLoginPopup" @click.self="closeLoginModal">
        <view class="login-container" :class="{show: showLoginPopup}" @click.stop>
          <view class="login-header">
            <text class="login-title">{{ loginStep === 1 ? '微信登录' : '完善资料' }}</text>
            <view class="close-btn" @click="closeLoginModal">
              <uni-icons type="closeempty" size="24" color="#666"></uni-icons>
            </view>
          </view>
          <view class="login-content">
            <!-- 步骤1: 获取用户基本信息 -->
            <template v-if="loginStep === 1">
              <image class="login-avatar" src="/static/wechat-login.png" mode="aspectFit"></image>
              <text class="login-desc">登录后才能点赞、评论和收藏哦</text>
              <button class="login-btn" @click="getUserProfile">微信一键登录</button>
            </template>
            
            <!-- 步骤2: 完善用户头像昵称 -->
            <template v-else-if="loginStep === 2">
              <text class="form-title">完善头像和昵称</text>
              
              <!-- 选择头像按钮 -->
              <button class="avatar-wrapper" open-type="chooseAvatar" @chooseavatar="onChooseAvatar">
                <image class="avatar-preview" :src="tempAvatarUrl || '/static/default-avatar.png'" mode="aspectFill"></image>
                <text class="avatar-tip">点击选择头像</text>
              </button>
              
              <!-- 输入昵称 -->
              <view class="nickname-wrapper">
                <text class="label">昵称</text>
                <input 
                  type="nickname" 
                  class="nickname-input" 
                  placeholder="请输入昵称" 
                  v-model="tempNickName"
                  @change="onInputNickname" 
                />
              </view>
              
              <!-- 保存信息按钮 -->
              <button class="save-button" @click="saveUserInfo">保存</button>
            </template>
          </view>
        </view>
      </view>
    </view>
  </template>
  
  <script>
  import { getPostDetail, submitComment, getComments, getUserById, togglePostLike, getPostLikeStatus } from '@/request/api.js'

  export default {
    // 移除不必要的配置，使用pages.json中的配置
    data() {
      return {
        commentId: null,
        sourceType: 'post',
        // 初始化空对象，避免渲染时获取不到属性
        detail: {
          id: 0,
          avatar: '/static/default-avatar.png',
          nickname: '',
          content: '',
          publishTime: '',
          likeCount: 0,
          commentCount: 0,
          collectCount: 0,
          isLiked: false,
          isCollected: false,
          isFollowed: false
        },
        replies: [],
        page: 1,
        pageSize: 10,
        hasMore: true,
        loading: false,
        isDataLoaded: false,
        isRefreshing: false,
        showCommentBox: false,
        replyContent: '',
        replyPlaceholder: '写下你的评论...',
        replyHoverId: null,
        replyToUser: null,  // 回复某个具体用户
        showLoginPopup: false, // 登录弹窗显示状态
        actionAfterLogin: null, // 登录后要执行的动作
        isLoggedIn: false, // 新增的登录状态
        // 新增登录相关的状态
        loginStep: 1,
        canIUseGetUserProfile: false,
        tempAvatarUrl: '',
        tempNickName: ''
      };
    },
    // 响应导航栏按钮点击
    onNavigationBarButtonTap(e) {
      this.shareComment();
    },
    onLoad(options) {
      // 获取传递的评论ID参数
      this.commentId = options.id || null;
      // 获取传递的类型参数（评论或笔记）
      this.contentType = options.type || 'comment';
      
      // 检查是否支持getUserProfile
      if (wx.getUserProfile) {
        this.canIUseGetUserProfile = true;
      }
      
      // 尝试从App全局状态获取登录信息
      const app = getApp();
      if (app.globalData && app.globalData.isLoggedIn) {
        console.log('从App全局状态获取登录信息');
        this.isLoggedIn = true;
      }
      
      // 添加登录状态变化监听
      uni.$on('loginStatusChanged', this.handleLoginStatusChanged);
      
      if (this.contentType === 'note') {
        // 从本地存储获取笔记数据
        this.loadNoteData();
      } else {
        // 正常加载场景，获取传入的参数
        this.commentId = options.id;
        this.sourceType = options.type || 'post';
        
        // 根据不同类型处理不同的数据
        if (this.sourceType === 'note') {
          // 加载笔记数据
          this.loadNoteData();
        } else {
          // 加载评论数据（博文）
          this.initData();
        }
      }
    },
    // 在页面卸载时移除事件监听
    onUnload() {
      uni.$off('loginStatusChanged', this.handleLoginStatusChanged);
    },
    methods: {
      // 加载笔记数据
      async loadNoteData() {
        try {
          // 显示加载中
          uni.showLoading({
            title: '加载中...',
            mask: true
          });
          
          // 从本地存储获取当前笔记
          const noteData = uni.getStorageSync('currentNote');
          
          if (noteData) {
            // 检查笔记是否在服务器上存在
            if (noteData.id && Number.isInteger(Number(noteData.id))) {
              try {
                // 尝试从服务器获取笔记数据
                await getPostDetail(noteData.id);
              } catch (error) {
                // 如果服务器上找不到该笔记，说明已被管理员删除
                if (error.statusCode === 404) {
                  uni.hideLoading();
                  uni.showModal({
                    title: '提示',
                    content: '笔记不存在或已被删除',
                    showCancel: false,
                    success: () => {
                      // 从本地存储中也删除这条笔记
                      const userNotes = uni.getStorageSync('userNotes') || [];
                      const updatedNotes = userNotes.filter(note => note.id !== noteData.id);
                      
                      // 如果有变化，更新本地存储
                      if (updatedNotes.length !== userNotes.length) {
                        uni.setStorageSync('userNotes', updatedNotes);
                      }
                      
                      // 返回上一页
                      uni.navigateBack();
                    }
                  });
                  return;
                }
              }
            }
            
            // 处理图片URL，确保URL正确
            let images = [];
            if (noteData.images && noteData.images.length > 0) {
              images = noteData.images.filter(img => img && typeof img === 'string');
              console.log('处理后的图片数组:', images);
            }
            
            // 优先使用笔记中已包含的用户信息
            let userAvatar = '/static/default-avatar.png';
            let userNickname = '匿名用户';
            
            // 1. 首先，尝试从note.user对象获取用户信息
            if (noteData.user) {
              console.log('从笔记user对象获取用户信息:', noteData.user);
              userAvatar = noteData.user.avatar || noteData.user.avatar_url || userAvatar;
              userNickname = noteData.user.nickname || noteData.user.username || userNickname;
            } 
            // 2. 如果有avatar和nickname直接属性，使用它们
            else if (noteData.avatar || noteData.nickname) {
              userAvatar = noteData.avatar || userAvatar;
              userNickname = noteData.nickname || userNickname;
            }
            // 3. 如果有user_id但没有完整用户信息，尝试从API获取
            else if (noteData.user_id) {
              try {
                const userInfo = await getUserById(noteData.user_id);
                if (userInfo && userInfo.avatar_url) {
                  userAvatar = userInfo.avatar_url;
                }
                if (userInfo && userInfo.nickname) {
                  userNickname = userInfo.nickname;
                }
                console.log('从API获取到笔记用户信息:', userInfo);
              } catch (userError) {
                console.error('获取笔记用户信息失败:', userError);
                // 失败时使用当前登录用户信息作为后备
                const currentUserInfo = uni.getStorageSync('userInfo');
                if (currentUserInfo) {
                  userAvatar = currentUserInfo.avatar_url || currentUserInfo.avatar || userAvatar;
                  userNickname = currentUserInfo.nickname || userNickname;
                }
              }
            }
            
            console.log('最终使用的用户信息 - 头像:', userAvatar, '昵称:', userNickname);
            
            // 格式化笔记数据为详情页需要的格式
            this.detail = {
              id: noteData.id,
              avatar: userAvatar,
              nickname: userNickname,
              content: noteData.content,
              publishTime: noteData.createTime,
              likeCount: noteData.likeCount || 0,
              commentCount: noteData.commentCount || 0,
              isLiked: noteData.isLiked || false,
              isCollected: noteData.isCollected || false,
              isFollowed: false,
              images: images
            };
            
            // 如果有评论数据，加载评论
            if (noteData.replies && noteData.replies.length > 0) {
              this.replies = noteData.replies;
              this.hasMore = false;
            } else {
              this.replies = [];
              this.hasMore = false;
            }
            
            this.isDataLoaded = true;
          } else {
            // 没有找到笔记数据
            uni.showToast({
              title: '笔记不存在',
              icon: 'none'
            });
            setTimeout(() => {
              uni.navigateBack();
            }, 1500);
          }
        } catch (error) {
          console.error('加载笔记数据失败:', error);
          uni.showToast({
            title: '加载失败',
            icon: 'none'
          });
        } finally {
          uni.hideLoading();
        }
      },
      
      // 初始化数据
      async initData() {
        if (this.isDataLoaded) return;
        
        // 确保有评论ID
        if (!this.commentId) {
          uni.showToast({
            title: '参数错误',
            icon: 'none'
          });
          return;
        }
        
        try {
          uni.showLoading({
            title: '加载中...',
            mask: true
          });
          
          // 加载评论详情
          if (this.commentId) {
            try {
              // 从API获取帖子详情
              const postDetail = await getPostDetail(this.commentId);
              console.log('获取到的帖子详情:', postDetail);
              
              // 检查用户是否已登录
              const isLoggedIn = !!uni.getStorageSync('token');
              this.isLoggedIn = isLoggedIn;
              
              if (postDetail && postDetail.id) {
                // 尝试获取用户信息
                let userAvatar = '/static/default-avatar.png';
                let userNickname = '旅行达人';
                
                if (postDetail.user_id) {
                  try {
                    // 使用新添加的API获取用户信息
                    const userInfo = await getUserById(postDetail.user_id);
                    if (userInfo && userInfo.avatar_url) {
                      userAvatar = userInfo.avatar_url;
                    }
                    if (userInfo && userInfo.nickname) {
                      userNickname = userInfo.nickname;
                    }
                    console.log('获取到的用户信息:', userInfo);
                  } catch (userError) {
                    console.error('获取用户信息失败:', userError);
                    // 如果获取用户信息失败，使用帖子中的用户信息（如果有）
                    if (postDetail.user && postDetail.user.avatar) {
                      userAvatar = postDetail.user.avatar;
                    }
                    if (postDetail.user && postDetail.user.nickname) {
                      userNickname = postDetail.user.nickname;
                    }
                  }
                }
                
                // 转换数据格式以适应前端展示
                this.detail = {
                  id: postDetail.id,
                  avatar: userAvatar,
                  nickname: userNickname,
                  content: postDetail.content || '内容获取失败',
                  publishTime: this.formatPublishTime(postDetail.created_at) || '未知时间',
                  likeCount: postDetail.likes_count || 0,
                  commentCount: postDetail.comments_count || 0,
                  collectCount: postDetail.collects_count || 0,
                  isLiked: false,
                  isCollected: false,
                  isFollowed: false,
                  images: postDetail.images || []
                };
                
                // 加载评论回复
                await this.loadCommentReplies();
                
                // 设置用户交互状态
                if (isLoggedIn) {
                  this.checkUserInteractions();
                }
              } else {
                // 如果API返回空对象，则加载模拟数据
                await this.loadMockData();
              }
            } catch (error) {
              console.error('API请求失败:', error);
              // API请求失败时，加载模拟数据
              await this.loadMockData();
            }
          }
          
          this.isDataLoaded = true;
        } catch (error) {
          console.error('初始化数据失败:', error);
          uni.showToast({
            title: '加载失败，请重试',
            icon: 'none'
          });
        } finally {
          uni.hideLoading();
        }
      },
      
      // 加载模拟数据（当API请求失败时使用）
      async loadMockData() {
        await Promise.all([
          this.loadCommentDetail(),
          this.loadCommentReplies()
        ]);
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
      
      // 加载评论详情
      loadCommentDetail() {
        return new Promise((resolve) => {
          // 模拟API请求，实际项目中应替换为真实接口调用
          console.log('加载评论ID:', this.commentId);
          
          setTimeout(() => {
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
            } else {
              // 其他ID使用默认数据
              this.detail = {
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
              };
            }
            
            // 数据加载完成
            resolve();
          }, 300);
        });
      },
      
      // 加载评论回复
      loadCommentReplies() {
        if (this.loading || !this.hasMore) return Promise.resolve();
        
        this.loading = true;
        
        return new Promise(async (resolve) => {
          try {
            // 如果是显示本地笔记，使用本地模拟数据
            if (this.contentType === 'note') {
              await this.loadReplies();
              resolve();
              return;
            }
            
            // 从服务器获取评论
            const skip = (this.page - 1) * this.pageSize;
            const comments = await getComments(this.commentId, this.page, this.pageSize);
            
            if (Array.isArray(comments) && comments.length > 0) {
              // 处理每条评论，获取用户信息
              const processedComments = await Promise.all(comments.map(async (comment) => {
                let userAvatar = '/static/default-avatar.png';
                let userNickname = '游客';
                
                if (comment.user_id) {
                  try {
                    // 使用新添加的API获取用户信息
                    const userInfo = await getUserById(comment.user_id);
                    if (userInfo && userInfo.avatar_url) {
                      userAvatar = userInfo.avatar_url;
                    }
                    if (userInfo && userInfo.nickname) {
                      userNickname = userInfo.nickname;
                    }
                  } catch (userError) {
                    console.error('获取评论用户信息失败:', userError);
                    // 如果获取用户信息失败，使用评论中的用户信息（如果有）
                    if (comment.user && comment.user.avatar) {
                      userAvatar = comment.user.avatar;
                    }
                    if (comment.user && comment.user.nickname) {
                      userNickname = comment.user.nickname;
                    }
                  }
                }
                
                return {
                  id: comment.id,
                  avatar: userAvatar,
                  nickname: userNickname,
                  content: comment.content,
                  publishTime: this.formatPublishTime(comment.created_at),
                  likeCount: 0, // 暂不支持评论点赞
                  isLiked: false
                };
              }));
              
              // 如果是第一页，替换评论列表；否则追加
              if (this.page === 1) {
                this.replies = processedComments;
              } else {
                this.replies = [...this.replies, ...processedComments];
              }
              
              // 更新页码和状态
              this.page++;
              this.hasMore = comments.length >= this.pageSize;
            } else {
              // 没有更多评论了
              if (this.page > 1) {
                this.hasMore = false;
              } else if (this.page === 1) {
                // 第一页就没有数据
                this.replies = [];
                this.hasMore = false;
              }
            }
          } catch (error) {
            console.error('获取评论列表失败:', error);
            // 如果API请求失败，回退到模拟数据
            await this.loadReplies();
          } finally {
            this.loading = false;
            resolve();
          }
        });
      },
      
      // 备用方法：加载模拟评论数据
      loadReplies() {
        return new Promise((resolve) => {
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
                    publishTime: '2小时前',
                    likeCount: 3,
                    isLiked: false
                  }
                ];
              } else {
                // 第二页没有更多数据
                this.hasMore = false;
              }
            } else if (this.page === 1) {
              // 第一页数据
              this.replies = [
                {
                  id: 1,
                  avatar: '/static/default-avatar.png',
                  nickname: '用户A',
                  content: '感谢分享！周末就去看看',
                  publishTime: '1小时前',
                  likeCount: 5,
                  isLiked: false
                }
              ];
            } else if (this.page > 1) {
              // 为其他评论ID模拟加载更多数据
              const moreReplies = [
                {
                  id: this.replies.length + 1,
                  avatar: '/static/default-avatar.png',
                  nickname: '用户' + (this.page + 1),
                  content: '这是加载的第' + this.page + '页回复',
                  publishTime: Math.floor(Math.random() * 24) + '小时前',
                  likeCount: Math.floor(Math.random() * 10),
                  isLiked: false
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
            resolve();
          }, 500);
        });
      },
      
      // 刷新评论
      refreshComments(e) {
        this.isRefreshing = true;
        this.page = 1;
        this.hasMore = true;
        this.replies = [];
        
        // 根据内容类型选择加载方法
        if (this.sourceType === 'note') {
          // 刷新笔记评论
          this.loadNoteData().then(() => {
            this.isRefreshing = false;
            uni.stopPullDownRefresh();
            if (e && typeof e.stopPullDownRefresh === 'function') {
              e.stopPullDownRefresh();
            }
          });
        } else {
          // 刷新评论回复
          this.loadCommentReplies().then(() => {
            this.isRefreshing = false;
            uni.stopPullDownRefresh();
            if (e && typeof e.stopPullDownRefresh === 'function') {
              e.stopPullDownRefresh();
            }
          });
        }
      },
      
      // 滚动到底部加载更多
      onScrollToLower() {
        if (!this.loading && this.hasMore) {
          this.loadCommentReplies();
        }
      },
      
      // 检查用户交互状态
      async checkUserInteractions() {
        await this.checkUserInteractionStatus();
      },
      
      // 详细检查用户交互状态的实现
      async checkUserInteractionStatus() {
        try {
          // 获取博文点赞状态
          if (this.detail && this.detail.id) {
            const likeStatus = await getPostLikeStatus(this.detail.id);
            this.detail.isLiked = likeStatus.is_liked;
            this.detail.likeCount = likeStatus.likes_count;
            console.log(`获取到点赞状态: 已${this.detail.isLiked ? '点赞' : '未点赞'}, 点赞数: ${this.detail.likeCount}`);
          }
          
          // 评论点赞状态暂不支持，使用本地存储
          const likedReplies = uni.getStorageSync('likedReplies') || [];
          this.replies.forEach(reply => {
            reply.isLiked = likedReplies.includes(reply.id);
          });
          
          // 收藏和关注状态目前仍使用本地存储
          const collectedPosts = uni.getStorageSync('collectedPosts') || [];
          const followedUsers = uni.getStorageSync('followedUsers') || [];
          
          this.detail.isCollected = collectedPosts.includes(this.detail.id);
          this.detail.isFollowed = followedUsers.includes(this.detail.nickname);
        } catch (error) {
          console.error('获取交互状态失败:', error);
        }
      },
      
      // 检查登录状态
      checkLoginStatus() {
        // 使用组件的isLoggedIn属性
        if (!this.isLoggedIn) {
          // 显示登录弹窗，而不是提示
          this.showLoginPopup = true;
          return false;
        }
        return true;
      },
      
      // 处理登录事件
      handleLogin() {
        // 检查是否支持getUserProfile
        if (!this.canIUseGetUserProfile) {
          this.canIUseGetUserProfile = wx.getUserProfile ? true : false;
        }
        
        if (this.canIUseGetUserProfile) {
          this.getUserProfile();
        } else {
          // 旧版微信，需要使用open-type="getUserInfo"的按钮
          uni.showToast({
            title: '当前微信版本过低，请升级微信版本',
            icon: 'none'
          });
        }
      },
      
      // 获取用户个人信息
      getUserProfile() {
        console.log('调用getUserProfile获取用户信息');
        uni.showLoading({ title: '登录中...' });
        
        // 调用wx.getUserProfile获取用户信息
        wx.getUserProfile({
          desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，会展示在弹窗中
          success: (res) => {
            console.log('获取到用户个人信息:', res.userInfo);
            
            // 保存微信原始用户信息，以便后续使用
            uni.setStorageSync('wx_user_info', res.userInfo);
            
            // 预填充临时头像和昵称
            this.tempAvatarUrl = res.userInfo.avatarUrl;
            this.tempNickName = res.userInfo.nickName;
            
            // 如果获取到的是"微信用户"或默认头像，则进入完善信息步骤
            if (res.userInfo.nickName === '微信用户' || !res.userInfo.avatarUrl) {
              console.log('获取到默认昵称或头像，进入完善信息步骤');
              this.loginStep = 2;
              uni.hideLoading();
            } else {
              // 否则直接使用获取到的信息登录
              // 获取到用户信息后，继续获取微信code并调用后端API
              this.loginWithWechat(res.userInfo);
            }
          },
          fail: (err) => {
            console.error('用户拒绝授权:', err);
            uni.hideLoading();
            uni.showToast({ 
              title: '需要授权才能登录',
              icon: 'none'
            });
          }
        });
      },
      
      // 使用微信登录
      loginWithWechat(userInfo) {
        // 获取微信code
        uni.login({
          provider: 'weixin',
          success: async (loginRes) => {
            try {
              console.log('获取到微信登录code:', loginRes.code);
              
              // 保存微信登录信息到本地，即使后端不可用也能显示头像和昵称
              const localUserInfo = {
                nickname: userInfo.nickName,
                avatar: userInfo.avatarUrl,
                gender: userInfo.gender,
                country: userInfo.country,
                province: userInfo.province,
                city: userInfo.city,
                language: userInfo.language
              };
              uni.setStorageSync('userInfo', localUserInfo);
              
              // 更新登录状态
              this.isLoggedIn = true;
              
              // 调用后端API进行登录验证
              console.log('准备向后端发送登录请求...');
              
              // 使用实际IP地址替换localhost
              // const backendUrl = 'http://localhost:8000/api/wechat-login';
              const backendUrl = 'http://192.168.1.10:8000/api/wechat-login'; // 替换为您的实际IP
              
              try {
                const result = await uni.request({
                  url: backendUrl,
                  method: 'POST',
                  data: {
                    code: loginRes.code,
                    user_info: {
                      nickname: userInfo.nickName,
                      avatar_url: userInfo.avatarUrl,
                      gender: userInfo.gender,
                      country: userInfo.country,
                      province: userInfo.province,
                      city: userInfo.city,
                      language: userInfo.language
                    }
                  },
                  header: {
                    'content-type': 'application/json'
                  },
                  timeout: 10000 // 增加超时时间
                });
                
                console.log('收到后端响应:', result);
                
                // 检查请求是否成功
                if (result.statusCode === 200) {
                  const data = result.data;
                  console.log('登录成功, 获取到token和openid:', {
                    token: data.access_token,
                    openid: data.openid,
                    user_id: data.user_id
                  });
                  
                  // 保存登录状态
                  uni.setStorageSync('token', data.access_token);
                  uni.setStorageSync('openid', data.openid);
                  uni.setStorageSync('user_id', data.user_id);
                  
                  // 记录日志，确认token是否保存成功
                  const savedToken = uni.getStorageSync('token');
                  console.log('保存并验证token成功:', savedToken ? '√ 已保存' : '× 未保存');
                  console.log('保存的本地userInfo:', localUserInfo);
                  
                  // 发布全局登录成功事件，通知其他页面更新状态
                  uni.$emit('loginSuccess', {
                    isLoggedIn: true,
                    userInfo: localUserInfo,
                    token: data.access_token // 显式包含token
                  });
                  
                  uni.showToast({ title: '登录成功' });
                  
                  // 如果有登录后要执行的动作，执行它
                  if (this.actionAfterLogin) {
                    const action = this.actionAfterLogin;
                    this.actionAfterLogin = null; // 清除动作
                    setTimeout(() => {
                      action(); // 执行之前保存的动作
                    }, 500); // 延迟一下执行，避免连续操作
                  }
                } else {
                  console.error('登录失败:', result.data);
                  uni.showToast({ 
                    title: result.data?.detail || '登录失败',
                    icon: 'none'
                  });
                }
              } catch (e) {
                console.error('登录请求异常:', e);
                uni.showToast({ 
                  title: '登录请求失败，但本地已记录',
                  icon: 'none',
                  duration: 2000
                });
                
                // 如果有登录后要执行的动作，执行它
                if (this.actionAfterLogin) {
                  const action = this.actionAfterLogin;
                  this.actionAfterLogin = null; // 清除动作
                  setTimeout(() => {
                    action(); // 执行之前保存的动作
                  }, 500); // 延迟一下执行，避免连续操作
                }
              }
            } catch (e) {
              console.error('登录过程出现异常:', e);
              uni.showToast({ 
                title: '登录处理失败',
                icon: 'none'
              });
            } finally {
              // 关闭登录弹窗
              this.showLoginPopup = false;
              uni.hideLoading();
            }
          },
          fail: (err) => {
            console.error('获取微信code失败:', err);
            uni.hideLoading();
            uni.showToast({ 
              title: '微信登录失败',
              icon: 'none'
            });
          }
        });
      },
      
      // 点赞主评论
      async toggleLike() {
        // 检查登录状态
        if (!this.checkLoginStatus()) {
          // 保存要执行的操作，登录成功后执行
          this.actionAfterLogin = this.toggleLike;
          return;
        }
        
        try {
          // 显示加载
          uni.showLoading({ title: '处理中...' });
          
          // 调用后端API切换点赞状态
          const result = await togglePostLike(this.detail.id);
          
          // 更新界面显示
          if (result) {
            this.detail.isLiked = result.is_liked;
            this.detail.likeCount = result.likes_count;
            
            // 提示用户
            uni.showToast({
              title: this.detail.isLiked ? '已点赞' : '已取消点赞',
              icon: 'none'
            });
          }
        } catch (error) {
          console.error('点赞失败:', error);
          uni.showToast({
            title: '操作失败，请重试',
            icon: 'none'
          });
        } finally {
          uni.hideLoading();
        }
      },
      
      // 点赞回复
      toggleReplyLike(index) {
        const execute = () => {
          const reply = this.replies[index];
          if (!reply) return;
          
          // 更新点赞状态
          reply.isLiked = !reply.isLiked;
          
          // 更新点赞数量
          if (reply.likeCount === undefined) reply.likeCount = 0;
          
          if (reply.isLiked) {
            reply.likeCount++;
          } else {
            reply.likeCount--;
            if (reply.likeCount < 0) reply.likeCount = 0;
          }
          
          // 保存点赞状态到本地
          this.saveInteractionStatus('likedReplies', reply.id, reply.isLiked);
        };
        
        // 检查登录状态
        if (!this.checkLoginStatus()) {
          // 保存要执行的操作，登录成功后执行
          this.actionAfterLogin = execute;
          return;
        }
        
        execute();
      },
      
      // 收藏功能
      toggleCollect() {
        const execute = () => {
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
        };
        
        // 检查登录状态
        if (!this.checkLoginStatus()) {
          // 保存要执行的操作，登录成功后执行
          this.actionAfterLogin = execute;
          return;
        }
        
        execute();
      },
      
      // 关注功能
      toggleFollow() {
        const execute = () => {
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
        };
        
        // 检查登录状态
        if (!this.checkLoginStatus()) {
          // 保存要执行的操作，登录成功后执行
          this.actionAfterLogin = execute;
          return;
        }
        
        execute();
      },
      
      // 显示评论输入框
      showCommentInput() {
        // 检查登录状态
        if (!this.checkLoginStatus()) {
          // 保存要执行的操作，登录成功后执行
          this.actionAfterLogin = () => {
            this.replyToUser = null;
            this.replyPlaceholder = '写下你的评论...';
            this.showCommentBox = true;
          };
          return;
        }
        
        this.replyToUser = null;
        this.replyPlaceholder = '写下你的评论...';
        this.showCommentBox = true;
      },
      
      // 回复特定评论
      replyToComment(reply) {
        // 检查登录状态
        if (!this.checkLoginStatus()) {
          // 保存要执行的操作，登录成功后执行
          this.actionAfterLogin = () => {
            this.replyToUser = reply;
            this.replyPlaceholder = `回复 ${reply.nickname}：`;
            this.showCommentBox = true;
          };
          return;
        }
        
        this.replyToUser = reply;
        this.replyPlaceholder = `回复 ${reply.nickname}：`;
        this.showCommentBox = true;
      },
      
      // 提交评论
      async submitComment() {
        if (!this.replyContent.trim()) {
          uni.showToast({
            title: '评论内容不能为空',
            icon: 'none'
          });
          return;
        }
        
        try {
          // 显示加载提示
          uni.showLoading({
            title: '发送中...',
            mask: true
          });
          
          // 获取用户信息
          const userInfo = uni.getStorageSync('userInfo') || {
            nickname: '游客',
            avatar: '/static/default-avatar.png'
          };
          
          // 获取当前登录用户ID
          const userId = uni.getStorageSync('user_id');
          
          // 构建评论数据
          const commentData = {
            content: this.replyContent,
            parent_id: this.replyToUser ? this.replyToUser.id : null
          };
          
          // 发送评论到后端
          let result;
          if (this.contentType === 'note') {
            // 本地笔记评论，只保存在本地
            const noteId = this.commentId;
            result = {
              success: true,
              id: Date.now(), // 使用时间戳作为临时ID
              created_at: new Date().toISOString(),
              user: {
                nickname: userInfo.nickname,
                avatar: userInfo.avatar
              },
              user_id: userId // 添加用户ID
            };
          } else {
            // 发送到服务器
            result = await submitComment(this.commentId, commentData);
          }
          
          if (result && (result.success || result.id)) {
            // 尝试获取最新的用户信息
            let avatarUrl = userInfo.avatar;
            let nickname = userInfo.nickname;
            
            if (userId) {
              try {
                const latestUserInfo = await getUserById(userId);
                if (latestUserInfo) {
                  if (latestUserInfo.avatar_url) {
                    avatarUrl = latestUserInfo.avatar_url;
                  }
                  if (latestUserInfo.nickname) {
                    nickname = latestUserInfo.nickname;
                  }
                }
              } catch (error) {
                console.error('获取最新用户信息失败:', error);
              }
            }
            
            // 创建新评论对象
            const newReply = {
              id: result.id,
              avatar: avatarUrl,
              nickname: nickname,
              content: this.replyContent,
              publishTime: '刚刚',
              likeCount: 0,
              isLiked: false
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
          } else {
            // 评论失败
            uni.showToast({
              title: '评论失败，请重试',
              icon: 'none'
            });
          }
        } catch (error) {
          console.error('提交评论失败:', error);
          uni.showToast({
            title: '评论失败，请重试',
            icon: 'none'
          });
        } finally {
          uni.hideLoading();
        }
      },
      
      // 分享评论
      shareComment() {
        uni.showShareMenu({
          withShareTicket: true,
          success: () => {
            uni.showToast({
              title: '分享成功',
              icon: 'success'
            });
          }
        });
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
        ];
        
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
      },
      
      // 处理图片加载错误
      handleImageError(index) {
        if (this.detail.images && this.detail.images.length > index) {
          console.log('图片加载失败:', this.detail.images[index]);
          this.detail.images[index] = '/static/default-img.png';
        }
      },
      
      // 预览图片
      previewImage(current, urls) {
        uni.previewImage({
          current: current,
          urls: urls
        });
      },
      
      // 关闭登录弹窗
      closeLoginModal() {
        this.showLoginPopup = false;
        // 重置登录步骤
        this.loginStep = 1;
        this.tempNickName = '';
        this.tempAvatarUrl = '';
      },
      
      // 选择头像
      onChooseAvatar(e) {
        console.log('选择头像:', e.detail.avatarUrl);
        this.tempAvatarUrl = e.detail.avatarUrl;
      },
      
      // 输入昵称
      onInputNickname(e) {
        console.log('输入昵称:', e.detail.value);
        this.tempNickName = e.detail.value;
      },
      
      // 保存用户信息
      saveUserInfo() {
        if (!this.tempNickName.trim()) {
          uni.showToast({
            title: '请输入昵称',
            icon: 'none'
          });
          return;
        }
        
        if (!this.tempAvatarUrl) {
          uni.showToast({
            title: '请选择头像',
            icon: 'none'
          });
          return;
        }
        
        console.log('保存用户信息:', this.tempNickName, this.tempAvatarUrl);
        
        // 创建用户信息对象
        const userInfo = {
          nickname: this.tempNickName,
          avatar: this.tempAvatarUrl,
          // 保持兼容性
          nickName: this.tempNickName,
          avatarUrl: this.tempAvatarUrl
        };
        
        // 保存到本地存储
        uni.setStorageSync('userInfo', userInfo);
        
        // 更新页面显示的用户信息
        this.isLoggedIn = true;
        
        // 创建一个临时token (如果没有真实的后端token)
        const tempToken = 'temp_' + new Date().getTime();
        uni.setStorageSync('token', tempToken);
        
        // 记录日志，确认token是否保存成功
        const savedToken = uni.getStorageSync('token');
        console.log('手动设置profile后验证token:', savedToken ? '√ 已保存' : '× 未保存');
        console.log('保存的本地userInfo:', userInfo);
        
        // 发布全局登录成功事件，通知其他页面更新状态
        uni.$emit('loginSuccess', {
          isLoggedIn: true,
          userInfo: userInfo,
          token: tempToken
        });
        
        // 关闭登录弹窗
        this.showLoginPopup = false;
        
        // 如果有登录后要执行的动作，执行它
        if (this.actionAfterLogin) {
          const action = this.actionAfterLogin;
          this.actionAfterLogin = null; // 清除动作
          setTimeout(() => {
            action(); // 执行之前保存的动作
          }, 500); // 延迟一下执行，避免连续操作
        }
        
        // 提示用户
        uni.showToast({
          title: '登录成功',
          icon: 'success'
        });
      },
      
      // 处理登录状态变化
      handleLoginStatusChanged(data) {
        console.log('收到登录状态变化事件', data);
        
        if (data && data.isLoggedIn) {
          this.isLoggedIn = data.isLoggedIn;
          
          // 更新用户交互状态
          if (this.isDataLoaded) {
            this.checkUserInteractions();
          }
        }
      }
    }
  };
  </script>
  
  <style lang="scss">
  .container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background-color: #f6f7f9;
    padding-bottom: 120rpx; /* 为底部评论按钮留出空间 */
  }
  
  .comment-section {
    padding: 30rpx;
    background-color: #fff;
    margin-bottom: 20rpx;
    box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
  }
  
  .comment-card {
    padding: 10rpx 0;
    
    .user-info {
      display: flex;
      align-items: center;
      margin-bottom: 30rpx;
      
      .avatar {
        width: 90rpx;
        height: 90rpx;
        border-radius: 50%;
        margin-right: 24rpx;
        border: 2rpx solid #f1f1f1;
        box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.08);
      }
      
      .user-meta {
        display: flex;
        flex-direction: column;
        
        .nickname {
          font-size: 34rpx;
          font-weight: 600;
          color: #333;
          margin-bottom: 8rpx;
        }
        
        .publish-time {
          font-size: 24rpx;
          color: #999;
        }
      }
    }
    
    .content-wrapper {
      margin-bottom: 40rpx;
      
      .content-text {
        font-size: 34rpx;
        color: #333;
        line-height: 1.7;
        letter-spacing: 1rpx;
      }
      
      .images-container {
        display: flex;
        flex-wrap: wrap;
        margin-top: 20rpx;
        
        .content-image {
          width: 33.33%;
          height: auto;
          margin-bottom: 10rpx;
          border-radius: 4rpx;
          overflow: hidden;
          margin-right: 10rpx;
          
          &:nth-child(3n) {
            margin-right: 0;
          }
        }
      }
    }
  }
  
  .interaction-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20rpx 0;
    border-top: 1px solid rgba(0,0,0,0.05);
    
    .interaction-button {
      display: flex;
      align-items: center;
      padding: 16rpx 0;
      transition: all 0.2s ease;
      
      &:active {
        transform: scale(0.95);
      }
      
      .button-text {
        font-size: 26rpx;
        color: #666;
        margin-left: 8rpx;
        
        &.active {
          &:nth-child(1) {
            color: #ff5656;
          }
        }
      }
      
      &.active {
        .button-text {
          &:nth-child(1) {
            color: #ff5656;
          }
          
          &:nth-child(3) {
            color: #ffc107;
          }
          
          &:nth-child(4) {
            color: #3182ce;
          }
        }
      }
    }
  }
  
  .loading-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200rpx;
    
    .loading-text {
      font-size: 28rpx;
      color: #999;
      margin-top: 16rpx;
    }
  }
  
  .replies-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24rpx 30rpx;
    background: #fff;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    
    .replies-title {
      font-size: 30rpx;
      font-weight: 600;
      color: #333;
    }
    
    .sort-button {
      font-size: 26rpx;
      color: #666;
      display: flex;
      align-items: center;
      
      &::after {
        content: "";
        display: inline-block;
        width: 0;
        height: 0;
        border-left: 10rpx solid transparent;
        border-right: 10rpx solid transparent;
        border-top: 10rpx solid #666;
        margin-left: 8rpx;
      }
    }
  }
  
  .reply-list {
    flex: 1;
    background: #fff;
    height: calc(100vh - 400rpx); /* 动态计算高度，确保列表区域合适 */
  }
  
  .reply-container {
    padding: 0 30rpx;
  }
  
  .reply-item {
    display: flex;
    padding: 30rpx 0;
    border-bottom: 1px solid rgba(0,0,0,0.05);
    transition: background-color 0.3s;
    
    &:last-child {
      border-bottom: none;
    }
  }
  
  .reply-item-hover {
    background-color: rgba(0,0,0,0.02);
  }
  
  .reply-avatar {
    width: 70rpx;
    height: 70rpx;
    border-radius: 50%;
    margin-right: 20rpx;
    border: 2rpx solid #f1f1f1;
  }
  
  .reply-content {
    flex: 1;
  }
  
  .reply-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10rpx;
  }
  
  .reply-nickname {
    font-size: 28rpx;
    font-weight: 500;
    color: #333;
  }
  
  .reply-time {
    font-size: 24rpx;
    color: #999;
  }
  
  .reply-text {
    font-size: 28rpx;
    color: #333;
    line-height: 1.6;
    margin-bottom: 16rpx;
    word-break: break-all; /* 确保长文本正确换行 */
  }
  
  .reply-actions {
    display: flex;
    
    .reply-like, .reply-comment {
      display: flex;
      align-items: center;
      margin-right: 30rpx;
      
      text {
        font-size: 24rpx;
        color: #999;
        margin-left: 6rpx;
        
        &.liked-text {
          color: #ff5656;
        }
      }
    }
  }
  
  .empty-replies {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 120rpx 0;
    
    .empty-text {
      font-size: 28rpx;
      color: #999;
      margin-top: 20rpx;
    }
  }
  
  .loading-more {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30rpx 0;
    
    text {
      font-size: 26rpx;
      color: #999;
      margin-left: 10rpx;
    }
  }
  
  .no-more {
    text-align: center;
    padding: 30rpx 0;
    
    text {
      font-size: 26rpx;
      color: #999;
    }
  }
  
  .comment-input-area {
    display: flex;
    padding: 20rpx 30rpx;
    background: #fff;
    border-top: 1px solid rgba(0,0,0,0.05);
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 100;
    box-shadow: 0 -2rpx 10rpx rgba(0,0,0,0.05);
  }
  
  .input-wrapper {
    flex: 1;
    position: relative;
    margin-right: 20rpx;
  }
  
  .comment-input {
    width: 100%;
    height: 80rpx;
    padding: 0 100rpx 0 30rpx;
    background: #f5f5f5;
    border-radius: 40rpx;
    font-size: 28rpx;
    color: #333;
  }
  
  .word-count {
    position: absolute;
    right: 20rpx;
    top: 50%;
    transform: translateY(-50%);
    font-size: 24rpx;
    color: #999;
  }
  
  .send-btn {
    width: 120rpx;
    height: 80rpx;
    line-height: 80rpx;
    text-align: center;
    background: #f0f0f0;
    border-radius: 40rpx;
    color: #999;
    font-size: 28rpx;
    padding: 0;
    border: none;
    transition: all 0.3s;
  }
  
  .send-btn-active {
    background: #3182ce;
    color: #fff;
  }
  
  .bottom-comment-btn {
    position: fixed;
    bottom: 30rpx;
    left: 50%;
    transform: translateX(-50%);
    width: 60%;
    height: 80rpx;
    line-height: 80rpx;
    background: rgba(49, 130, 206, 0.9); /* 更美观的蓝色背景 */
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    border-radius: 40rpx;
    font-size: 28rpx;
    z-index: 99;
    box-shadow: 0 4rpx 16rpx rgba(49, 130, 206, 0.3);
    transition: all 0.3s ease;
    
    &:active {
      transform: translateX(-50%) scale(0.95);
      box-shadow: 0 2rpx 8rpx rgba(49, 130, 206, 0.2);
    }
    
    text {
      margin-left: 10rpx;
    }
  }
  
  /* 登录弹窗样式 */
  .login-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: flex-end;
  }
  
  .login-container {
    width: 100%;
    background-color: #fff;
    border-radius: 24rpx 24rpx 0 0;
    padding: 40rpx;
    transform: translateY(100%);
    transition: transform 0.3s ease;
    
    &.show {
      transform: translateY(0);
    }
  }
  
  .login-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 40rpx;
  }
  
  .login-title {
    font-size: 36rpx;
    font-weight: 600;
    color: #333;
  }
  
  .close-btn {
    padding: 10rpx;
  }
  
  .login-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20rpx 0 40rpx;
  }
  
  .login-avatar {
    width: 160rpx;
    height: 160rpx;
    border-radius: 50%;
    margin-bottom: 30rpx;
    border: 4rpx solid #f1f1f1;
    box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.1);
  }
  
  .login-desc {
    font-size: 30rpx;
    color: #666;
    margin-bottom: 50rpx;
    text-align: center;
  }
  
  .login-btn {
    width: 80%;
    height: 90rpx;
    line-height: 90rpx;
    text-align: center;
    background: linear-gradient(45deg, #3182ce, #38a169);
    color: #fff;
    font-size: 32rpx;
    font-weight: 500;
    border-radius: 45rpx;
    box-shadow: 0 6rpx 16rpx rgba(56, 161, 105, 0.3);
    transition: all 0.3s ease;
    margin-bottom: 20rpx;
    
    &:active {
      transform: scale(0.98);
      box-shadow: 0 4rpx 8rpx rgba(56, 161, 105, 0.2);
    }
  }
  
  /* 新增表单样式 */
  .form-title {
    font-size: 32rpx;
    color: #333;
    font-weight: 600;
    margin-bottom: 30rpx;
    text-align: center;
  }
  
  .avatar-wrapper {
    width: 200rpx;
    height: 200rpx;
    margin: 0 auto 30rpx;
    border-radius: 50%;
    background: #f5f7fa;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 0;
    border: none;
    overflow: hidden;
  }
  
  .avatar-wrapper::after {
    border: none;
  }
  
  .avatar-preview {
    width: 180rpx;
    height: 180rpx;
    border-radius: 50%;
  }
  
  .avatar-tip {
    font-size: 24rpx;
    color: #666;
    position: absolute;
    bottom: 20rpx;
    left: 0;
    right: 0;
    text-align: center;
    background: rgba(0,0,0,0.5);
    color: #fff;
    padding: 6rpx 0;
  }
  
  .nickname-wrapper {
    width: 100%;
    margin-bottom: 40rpx;
  }
  
  .label {
    font-size: 28rpx;
    color: #666;
    margin-bottom: 10rpx;
    display: block;
  }
  
  .nickname-input {
    width: 100%;
    height: 90rpx;
    background: #f5f7fa;
    border-radius: 8rpx;
    padding: 0 30rpx;
    font-size: 28rpx;
    color: #333;
    box-sizing: border-box;
    border: 1px solid #eee;
  }
  
  .save-button {
    width: 100%;
    height: 90rpx;
    line-height: 90rpx;
    text-align: center;
    background: linear-gradient(45deg, #3182ce, #38a169);
    color: #fff;
    font-size: 32rpx;
    font-weight: 500;
    border-radius: 45rpx;
    box-shadow: 0 6rpx 16rpx rgba(56, 161, 105, 0.3);
    transition: all 0.3s ease;
    
    &:active {
      transform: scale(0.98);
      box-shadow: 0 4rpx 8rpx rgba(56, 161, 105, 0.2);
    }
  }
  </style>