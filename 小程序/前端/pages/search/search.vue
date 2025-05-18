<template>
  <view class="search-page">
    <!-- 搜索栏 -->
    <view class="search-header" :style="{ paddingTop: safeAreaInsetTop + 'px' }">
      <view class="search-bar">
        <uni-icons type="search" size="18" color="#666"></uni-icons>
        <input 
          type="text" 
          class="search-input" 
          placeholder="搜索目的地、景点、攻略" 
          v-model="keyword"
          confirm-type="search"
          @confirm="handleSearch"
          @input="onSearchInput"
          focus
        />
        <view v-if="keyword" class="clear-icon" @click="clearSearch">
          <uni-icons type="clear" size="18" color="#999"></uni-icons>
        </view>
      </view>
      <view class="cancel-btn" @click="navigateBack">取消</view>
    </view>
    
    <!-- 搜索结果 -->
    <view class="search-result" v-if="keyword">
      <!-- 使用瀑布流组件 -->
      <waterfall-flow
        :is-loading="isLoading"
        :is-refreshing="isRefreshing"
        :has-more="hasMore"
        :isEmpty="searchResults.length === 0"
        emptyText="没有找到相关内容"
        @load-more="loadMore"
        @refresh="refreshSearch"
      >
        <!-- 左侧列 -->
        <template #left-column>
          <travel-note-card
            v-for="note in leftColumn" 
            :key="note.id"
            :note="note"
            @card-click="navigateToDetail"
            @like="toggleLike"
            @comment="showCommentInput"
            @share="shareNote"
          />
        </template>
        
        <!-- 右侧列 -->
        <template #right-column>
          <travel-note-card
            v-for="note in rightColumn" 
            :key="note.id"
            :note="note"
            @card-click="navigateToDetail"
            @like="toggleLike"
            @comment="showCommentInput"
            @share="shareNote"
          />
        </template>
      </waterfall-flow>
    </view>
    
    <!-- 未搜索时或无搜索关键词时的建议 -->
    <view class="search-tips" v-else>
      <view class="hot-search">
        <view class="section-title">热门搜索</view>
        <view class="tag-list">
          <view class="tag-item" v-for="(tag, index) in hotTags" :key="index" @click="searchTag(tag)">
            {{ tag }}
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { searchPosts } from '@/request/api.js'
import TravelNoteCard from '@/components/TravelNoteCard.vue'
import WaterfallFlow from '@/components/WaterfallFlow.vue'

export default {
  components: {
    TravelNoteCard,
    WaterfallFlow
  },
  data() {
    return {
      keyword: '',            // 搜索关键词
      searchResults: [],      // 搜索结果
      isLoading: false,       // 是否正在加载
      isRefreshing: false,    // 是否正在刷新
      hasMore: true,          // 是否有更多数据
      page: 1,                // 当前页码
      pageSize: 15,           // 每页数量
      lastClickTime: 0,       // 上次点击时间（用于防抖）
      searchTimer: null,      // 搜索延时器（用于防抖）
      isLoggedIn: false,      // 是否已登录
      hotTags: ['西湖', '故宫', '长城', '黄山', '三亚', '成都', '美食', '民宿'], // 热门搜索标签
      statusBarHeight: 0,     // 状态栏高度
      safeAreaInsetTop: 0     // 安全区域顶部距离
    }
  },
  
  computed: {
    // 左侧瀑布流列
    leftColumn() {
      return this.searchResults.filter((_, index) => index % 2 === 0);
    },
    // 右侧瀑布流列
    rightColumn() {
      return this.searchResults.filter((_, index) => index % 2 === 1);
    }
  },
  
  onLoad(options) {
    // 如果从其他页面传入了搜索关键词，则立即搜索
    if (options.keyword) {
      this.keyword = decodeURIComponent(options.keyword);
      this.handleSearch();
    }
    
    // 检查用户登录状态
    this.checkLoginStatus();
  },
  
  onReady() {
    // 获取系统信息，用于适配不同设备的状态栏高度
    this.getSystemInfo();
  },
  
  methods: {
    // 搜索
    handleSearch() {
      if (!this.keyword.trim()) {
        return;
      }
      
      // 重置页码和状态
      this.page = 1;
      this.hasMore = true;
      this.searchResults = [];
      
      // 执行搜索
      this.fetchSearchResults();
    },
    
    // 搜索输入防抖
    onSearchInput() {
      // 清除之前的定时器
      if (this.searchTimer) {
        clearTimeout(this.searchTimer);
      }
      
      // 设置防抖延时500ms
      this.searchTimer = setTimeout(() => {
        this.handleSearch();
      }, 500);
    },
    
    // 清空搜索
    clearSearch() {
      this.keyword = '';
      this.searchResults = [];
    },
    
    // 搜索标签
    searchTag(tag) {
      this.keyword = tag;
      this.handleSearch();
    },
    
    // 获取搜索结果
    async fetchSearchResults() {
      if (this.isLoading || !this.keyword.trim()) return;
      
      this.isLoading = true;
      
      try {
        const skip = (this.page - 1) * this.pageSize;
        
        // 调用搜索API
        const results = await searchPosts(this.keyword, skip, this.pageSize);
        
        // 处理API返回的数据，确保格式与卡片组件需要的格式一致
        const processedResults = results.map(item => {
          // 确保用户字段存在
          const user = item.user || {};
          
          return {
            id: item.id,
            title: item.title,
            content: item.content,
            // 处理图片，优先使用images数组，其次使用cover_image
            images: Array.isArray(item.images) && item.images.length > 0 
                   ? item.images 
                   : (item.cover_image ? [item.cover_image] : []),
            // 直接设置封面图，以防TravelNoteCard组件使用
            cover_image: item.cover_image || (Array.isArray(item.images) && item.images.length > 0 ? item.images[0] : null),
            // 设置用户信息
            nickname: user.nickname || user.username || '未知用户',
            avatar: user.avatar || '/static/default-avatar.png',
            // 点赞和评论数据
            likeCount: item.likes_count || 0,
            isLiked: false,
            commentCount: item.comments_count || 0,
            // 情感分析类型
            sentimentType: item.sentiment_type,
            // 展开状态
            expanded: false,
            // 其他元数据
            publishTime: item.created_at ? this.formatDate(item.created_at) : '未知时间'
          };
        });
        
        // 如果是第一页，替换结果；否则追加结果
        if (this.page === 1) {
          this.searchResults = processedResults;
        } else {
          this.searchResults = [...this.searchResults, ...processedResults];
        }
        
        // 判断是否还有更多数据
        this.hasMore = results.length >= this.pageSize;
        
        // 如果是第一页且没有结果，显示提示
        if (this.page === 1 && results.length === 0) {
          uni.showToast({
            title: '未找到相关内容',
            icon: 'none'
          });
        }
      } catch (error) {
        console.error('搜索失败:', error);
        uni.showToast({
          title: '搜索失败，请重试',
          icon: 'none'
        });
      } finally {
        this.isLoading = false;
        this.isRefreshing = false;
      }
    },
    
    // 加载更多
    loadMore() {
      if (this.isLoading || !this.hasMore) return;
      
      console.log('加载更多搜索结果，当前页码:', this.page);
      this.page++;
      this.fetchSearchResults();
    },
    
    // 刷新搜索
    refreshSearch() {
      if (this.isRefreshing) return;
      
      console.log('刷新搜索结果');
      this.isRefreshing = true;
      this.page = 1;
      this.hasMore = true;
      this.fetchSearchResults();
    },
    
    // 导航到详情页
    navigateToDetail(postId) {
      uni.navigateTo({
        url: `/pages/detail/detail?id=${postId}`
      });
    },
    
    // 点赞
    toggleLike(postId) {
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
      
      // 防抖处理
      const now = Date.now()
      if (now - this.lastClickTime < 300) return
      this.lastClickTime = now
      
      // 找到对应笔记
      const note = this.searchResults.find(item => item.id === postId)
      if (!note) return
      
      // 切换点赞状态
      if (!note.isLiked) {
        note.likeCount++
        note.isLiked = true
      } else {
        note.likeCount--
        note.isLiked = false
      }
    },
    
    // 显示评论输入框
    showCommentInput(postId) {
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
      
      uni.showToast({
        title: '评论功能开发中',
        icon: 'none'
      });
    },
    
    // 分享笔记
    shareNote(note) {
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
    
    // 返回上一页
    navigateBack() {
      // 使用switchTab跳转到首页，而不是navigateBack
      // 这样可以确保在任何情况下都能返回首页，避免导航栈为空的报错
      uni.switchTab({
        url: '/pages/index/index'
      });
    },
    
    // 检查用户登录状态
    checkLoginStatus() {
      const token = uni.getStorageSync('token');
      this.isLoggedIn = !!token;
    },
    
    // 前往登录页
    goToLogin() {
      uni.navigateTo({
        url: '/pages/login/login'
      });
    },
    
    // 获取系统信息，用于适配不同设备的状态栏高度
    getSystemInfo() {
      uni.getSystemInfo({
        success: (info) => {
          this.statusBarHeight = info.statusBarHeight;
          console.log('状态栏高度:', this.statusBarHeight);
          
          // 兼容不同环境的CSS变量设置
          // #ifdef H5
          document.documentElement.style.setProperty('--status-bar-height', `${this.statusBarHeight}px`);
          // #endif
          
          // 小程序环境直接在style中动态绑定
          this.safeAreaInsetTop = this.statusBarHeight + 20; // 状态栏高度 + 额外安全距离
        }
      });
    },
    
    // 格式化日期
    formatDate(dateStr) {
      // 创建日期对象
      const date = new Date(dateStr);
      const now = new Date();
      
      // 计算时间差（毫秒）
      const diff = now - date;
      
      // 计算对应的时间单位
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);
      
      // 根据时间差显示不同格式
      if (seconds < 60) {
        return '刚刚';
      } else if (minutes < 60) {
        return `${minutes}分钟前`;
      } else if (hours < 24) {
        return `${hours}小时前`;
      } else if (days < 30) {
        return `${days}天前`;
      } else {
        // 超过一个月返回具体日期
        return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
      }
    }
  }
}
</script>

<style lang="scss">
.search-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f8f8f8;
  padding-top: 20rpx;
}

.search-header {
  display: flex;
  align-items: center;
  padding: 20rpx 30rpx;
  background-color: #fff;
  border-bottom: 1rpx solid #eee;
  margin-top: 40rpx;
  margin-bottom: 20rpx;
  border-radius: 20rpx;
  margin-left: 20rpx;
  margin-right: 20rpx;
  box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
  
  .search-bar {
    flex: 1;
    display: flex;
    align-items: center;
    height: 72rpx;
    background-color: #f5f5f5;
    border-radius: 36rpx;
    padding: 0 24rpx;
    position: relative;
    
    .uni-icons {
      margin-right: 12rpx;
    }
    
    .search-input {
      flex: 1;
      height: 100%;
      font-size: 28rpx;
    }
    
    .clear-icon {
      padding: 10rpx;
    }
  }
  
  .cancel-btn {
    font-size: 28rpx;
    color: #333;
    margin-left: 20rpx;
    padding: 0 10rpx;
  }
}

.search-result {
  flex: 1;
  background-color: #f8f8f8;
}

.search-tips {
  flex: 1;
  padding: 30rpx;
  
  .section-title {
    font-size: 30rpx;
    font-weight: bold;
    color: #333;
    margin-bottom: 20rpx;
  }
  
  .tag-list {
    display: flex;
    flex-wrap: wrap;
    
    .tag-item {
      background-color: #f5f5f5;
      padding: 12rpx 24rpx;
      border-radius: 28rpx;
      margin: 0 20rpx 20rpx 0;
      font-size: 26rpx;
      color: #666;
      
      &:active {
        background-color: #eee;
      }
    }
  }
}
</style> 