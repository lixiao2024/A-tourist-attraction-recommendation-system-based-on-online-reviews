<template>
  <view class="notes-container">
    <!-- 空状态 -->
    <view class="empty-state" v-if="notes.length === 0">
      <view class="empty-icon">
        <uni-icons type="paperplane" size="60" color="#cccccc"></uni-icons>
      </view>
      <text class="empty-text">暂无笔记</text>
      <text class="empty-tips">在景点详情页点击下方按钮发布您的旅行笔记</text>
      <button class="create-btn" @click="navigateToExplore">去浏览景点</button>
    </view>
    
    <!-- 笔记列表 - 使用与首页相同的瀑布流布局 -->
    <scroll-view 
      v-else
      scroll-y 
      class="waterfall-scroll"
      @scrolltolower="loadMoreNotes"
      refresher-enabled
      :refresher-triggered="isRefreshing"
      @refresherrefresh="refreshNotes"
    >
      <view class="waterfall-container">
        <!-- 左侧瀑布流列 -->
        <view class="waterfall-column">
          <view 
            v-for="note in leftColumn" 
            :key="note.id"
            class="card-item"
            @click="viewNoteDetail(note.id)"
          >
            <!-- 图片区域 -->
            <view class="card-image-container">
              <image 
                v-if="note.cover_image"
                class="card-image" 
                :src="note.cover_image" 
                mode="aspectFill"
                @error="handleImageError(note)"
              >
              </image>
              <image 
                v-else-if="note.images && note.images.length > 0"
                class="card-image" 
                :src="note.images[0]" 
                mode="aspectFill"
                @error="handleImageError(note)"
              >
              </image>
              <view v-else class="no-image-placeholder">
                <text class="empty-image-icon">📝</text>
              </view>
            </view>
            
            <!-- 内容区域 -->
            <view class="card-content">
              <text class="card-title" :class="{expanded: note.expanded}">{{ note.title || note.content }}</text>
              
              <!-- 展开/收起控制 -->
              <view 
                v-if="showExpandControl(note)"
                class="expand-control"
              >
                <text 
                  v-if="!note.expanded"
                  class="expand-btn"
                  @click.stop="toggleExpand(note)"
                >展开</text>
              </view>
              
              <!-- 时间和位置信息 -->
              <view class="note-meta">
                <text class="note-time">{{ note.createTime }}</text>
                <text class="note-location" v-if="note.location">{{ note.location }}</text>
              </view>
              
              <!-- 互动栏 -->
              <view class="interaction-bar">
                <view class="action-btn like-btn" :class="{active: note.isLiked}" @click.stop="toggleLike(note)">
                  <uni-icons :type="note.isLiked ? 'heart-filled' : 'heart'" size="20" :color="note.isLiked ? '#ff5656' : '#666'"></uni-icons>
                  <text class="count">{{ note.likeCount || '' }}</text>
                </view>
                <view class="action-btn comment-btn">
                  <uni-icons type="chat" size="20" color="#666"></uni-icons>
                  <text class="count">{{ note.commentCount || '' }}</text>
                </view>
                <view class="action-btn more-btn" @click.stop="showOptions(leftColumn.indexOf(note))">
                  <uni-icons type="more-filled" size="20" color="#666"></uni-icons>
                </view>
              </view>
            </view>
          </view>
        </view>
        
        <!-- 右侧瀑布流列 -->
        <view class="waterfall-column">
          <view 
            v-for="note in rightColumn" 
            :key="note.id"
            class="card-item"
            @click="viewNoteDetail(note.id)"
          >
            <!-- 图片区域 -->
            <view class="card-image-container">
              <image 
                v-if="note.cover_image"
                class="card-image" 
                :src="note.cover_image" 
                mode="aspectFill"
                @error="handleImageError(note)"
              >
              </image>
              <image 
                v-else-if="note.images && note.images.length > 0"
                class="card-image" 
                :src="note.images[0]" 
                mode="aspectFill"
                @error="handleImageError(note)"
              >
              </image>
              <view v-else class="no-image-placeholder">
                <text class="empty-image-icon">📝</text>
              </view>
            </view>
            
            <!-- 内容区域 -->
            <view class="card-content">
              <text class="card-title" :class="{expanded: note.expanded}">{{ note.title || note.content }}</text>
              
              <!-- 展开/收起控制 -->
              <view 
                v-if="showExpandControl(note)"
                class="expand-control"
              >
                <text 
                  v-if="!note.expanded"
                  class="expand-btn"
                  @click.stop="toggleExpand(note)"
                >展开</text>
              </view>
              
              <!-- 时间和位置信息 -->
              <view class="note-meta">
                <text class="note-time">{{ note.createTime }}</text>
                <text class="note-location" v-if="note.location">{{ note.location }}</text>
              </view>
              
              <!-- 互动栏 -->
              <view class="interaction-bar">
                <view class="action-btn like-btn" :class="{active: note.isLiked}" @click.stop="toggleLike(note)">
                  <uni-icons :type="note.isLiked ? 'heart-filled' : 'heart'" size="20" :color="note.isLiked ? '#ff5656' : '#666'"></uni-icons>
                  <text class="count">{{ note.likeCount || '' }}</text>
                </view>
                <view class="action-btn comment-btn">
                  <uni-icons type="chat" size="20" color="#666"></uni-icons>
                  <text class="count">{{ note.commentCount || '' }}</text>
                </view>
                <view class="action-btn more-btn" @click.stop="showOptions(rightColumn.indexOf(note) + leftColumn.length)">
                  <uni-icons type="more-filled" size="20" color="#666"></uni-icons>
                </view>
              </view>
            </view>
          </view>
        </view>
      </view>
      
      <!-- 加载更多提示 -->
      <view class="loading-more" v-if="loading">
        <uni-icons type="spinner-cycle" size="20" color="#999"></uni-icons>
        <text>加载中...</text>
      </view>
      
      <view class="no-more" v-if="!hasMore && notes.length > 0">
        <text>没有更多笔记了</text>
      </view>
    </scroll-view>
    
    <!-- 操作菜单 -->
    <view class="action-sheet" v-if="showActionSheet" @click="showActionSheet = false">
      <view class="action-sheet-content" @click.stop>
        <view class="action-item edit" @click="editNote(currentNoteIndex)">
          <uni-icons type="compose" size="22" color="#007AFF"></uni-icons>
          <text>编辑笔记</text>
        </view>
        <view class="action-item delete" @click="deleteNote(currentNoteIndex)">
          <uni-icons type="trash" size="22" color="#FF3B30"></uni-icons>
          <text>删除笔记</text>
        </view>
        <view class="action-item cancel" @click="showActionSheet = false">
          <text>取消</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { deletePost, getPosts } from '../../request/api.js';

export default {
  data() {
    return {
      notes: [],
      page: 1,
      pageSize: 10,
      hasMore: true,
      loading: false,
      isRefreshing: false,
      showActionSheet: false,
      currentNoteIndex: -1,
      syncedWithServer: false,  // 标记是否已经与服务器同步过
      lastSyncTime: 0,          // 记录上次同步时间
      isSyncing: false          // 同步锁，防止重复同步
    }
  },
  computed: {
    // 左侧瀑布流列
    leftColumn() {
      return this.notes.filter((_, index) => index % 2 === 0);
    },
    // 右侧瀑布流列
    rightColumn() {
      return this.notes.filter((_, index) => index % 2 === 1);
    }
  },
  onLoad() {
    this.loadNotes();
  },
  onShow() {
    // 如果正在同步或刷新，不重复触发
    if (this.isSyncing || this.isRefreshing) {
      console.log('已有同步任务正在执行，跳过');
      return;
    }
    
    // 获取当前页面路由
    const pages = getCurrentPages();
    // 如果有前一个页面，尝试检查是否从详情页返回
    let needSync = false;
    
    // 检查距离上次同步的时间
    const now = Date.now();
    if (now - this.lastSyncTime > 5 * 60 * 1000) { // 5分钟
      needSync = true;
    }
    
    // 尝试检查上一个页面
    if (pages.length > 1) {
      const prevPage = pages[pages.length - 2];
      try {
        // 不同环境下page对象结构可能不同，用try-catch保护
        if (prevPage.route && prevPage.route.includes('detail')) {
          needSync = true;
        } else if (prevPage.$page && prevPage.$page.route && prevPage.$page.route.includes('detail')) {
          needSync = true;
        }
      } catch (e) {
        console.error('检查页面路由出错:', e);
        // 出错时默认执行同步以保证数据一致性
        needSync = true;
      }
    }
    
    if (needSync) {
      this.isSyncing = true;
      console.log('执行数据同步');
      this.syncedWithServer = false;
      // 使用静默刷新，不显示加载提示
      this.refreshNotes(false).finally(() => {
        this.isSyncing = false;
        this.lastSyncTime = Date.now();
      });
    }
  },
  methods: {
    // 加载用户笔记
    async loadNotes() {
      if (this.loading || !this.hasMore) return;
      
      this.loading = true;
      
      try {
        // 模拟API请求延迟
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // 从本地存储中获取笔记数据
        const savedNotes = uni.getStorageSync('userNotes') || [];
        
        // 只在首次加载或刷新时与服务器同步
        if (this.page === 1 && !this.syncedWithServer) {
          await this.syncWithServer(savedNotes);
          this.syncedWithServer = true;
        }
        
        // 重新获取同步后的笔记
        const updatedNotes = uni.getStorageSync('userNotes') || [];
        
        if (this.page === 1) {
          // 第一页：重置笔记列表
          if (updatedNotes && updatedNotes.length > 0) {
            // 使用真实的用户笔记数据
            this.notes = updatedNotes.map(note => ({
              ...note,
              expanded: false,
              isLiked: false
            }));
            
            // 如果笔记数量少于每页数量，设置没有更多
            if (updatedNotes.length < this.pageSize) {
              this.hasMore = false;
            }
          } else if (this.notes.length === 0) {
            // 如果没有笔记数据，保持空数组
            this.notes = [];
            this.hasMore = false;
          }
        } else {
          // 分页加载：如果有足够的笔记，加载下一页
          const startIndex = (this.page - 1) * this.pageSize;
          if (updatedNotes && startIndex < updatedNotes.length) {
            const endIndex = Math.min(startIndex + this.pageSize, updatedNotes.length);
            const nextPageNotes = updatedNotes.slice(startIndex, endIndex);
            
            if (nextPageNotes.length > 0) {
              // 添加到现有笔记列表
              this.notes = [
                ...this.notes,
                ...nextPageNotes.map(note => ({
                  ...note,
                  expanded: false,
                  isLiked: false
                }))
              ];
              
              // 如果加载的笔记数量少于每页数量，设置没有更多
              if (nextPageNotes.length < this.pageSize) {
                this.hasMore = false;
              }
            } else {
              this.hasMore = false;
            }
          } else {
            this.hasMore = false;
          }
        }
        
        // 更新页码
        if (this.hasMore) {
          this.page++;
        }
      } catch (error) {
        console.error('加载笔记失败:', error);
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        });
      } finally {
        this.loading = false;
      }
    },
    
    // 与服务器同步笔记数据
    async syncWithServer(localNotes) {
      try {
        console.log('开始与服务器同步笔记数据');
        
        // 获取用户信息
        const userInfo = uni.getStorageSync('userInfo');
        if (!userInfo || !userInfo.id) {
          console.log('未找到用户信息，跳过同步');
          return;
        }
        
        // 从服务器获取用户的博文列表
        const serverPosts = await getPosts(0, 100, null, userInfo.id).catch(err => {
          console.error('获取服务器博文列表失败:', err);
          return null;
        });
        
        if (!serverPosts || !Array.isArray(serverPosts)) {
          console.log('服务器返回的博文不是有效数组，跳过同步');
          return;
        }
        
        console.log('服务器博文数量:', serverPosts.length);
        
        // 获取服务器博文ID列表
        const serverPostIds = serverPosts.map(post => post.id);
        console.log('服务器博文ID列表:', serverPostIds);
        
        // 检查本地笔记是否为空
        if (!localNotes || !Array.isArray(localNotes) || localNotes.length === 0) {
          console.log('本地没有笔记，跳过同步');
          return;
        }
        
        // 筛选出在本地存在但在服务器上已被删除的笔记
        const updatedNotes = localNotes.filter(note => {
          // 如果笔记没有ID或ID不是数字，保留它（可能是纯本地笔记）
          if (!note || !note.id || !Number.isInteger(Number(note.id))) {
            return true;
          }
          
          // 如果笔记ID在服务器列表中存在，保留它
          const shouldKeep = serverPostIds.includes(note.id);
          if (!shouldKeep) {
            console.log(`笔记ID ${note.id} 在服务器上不存在，将从本地删除`);
          }
          return shouldKeep;
        });
        
        console.log('同步前本地笔记数量:', localNotes.length);
        console.log('同步后本地笔记数量:', updatedNotes.length);
        
        // 如果有笔记被过滤掉，更新本地存储
        if (updatedNotes.length !== localNotes.length) {
          console.log('有笔记在服务器上已被删除，更新本地存储');
          uni.setStorageSync('userNotes', updatedNotes);
          // 触发UI更新
          if (this.page === 1) {
            this.notes = updatedNotes.map(note => ({
              ...note,
              expanded: false,
              isLiked: false
            }));
          }
          // 显示提示
          uni.showToast({
            title: '笔记已同步更新',
            icon: 'success',
            duration: 1500
          });
          return true; // 返回true表示有更新
        }
        
        return false; // 返回false表示没有更新
      } catch (error) {
        console.error('与服务器同步笔记失败:', error);
        return false;
      }
    },
    
    // 处理图片加载错误
    handleImageError(note) {
      // 如果cover_image加载失败，设置默认图片
      if (note.cover_image) {
        note.cover_image = '/static/default-image.png';
      }
      // 如果首张图片加载失败，设置默认图片
      if (note.images && note.images.length > 0) {
        note.images[0] = '/static/default-image.png';
      }
    },
    
    // 显示展开控制
    showExpandControl(note) {
      // 简单判断文本长度，实际应通过计算文本高度
      return note.content && note.content.length > 50;
    },
    
    // 切换展开/收起状态
    toggleExpand(note) {
      note.expanded = !note.expanded;
    },
    
    // 点赞功能
    toggleLike(note) {
      note.isLiked = !note.isLiked;
      
      if (note.isLiked) {
        note.likeCount = (note.likeCount || 0) + 1;
      } else {
        note.likeCount = Math.max(0, (note.likeCount || 1) - 1);
      }
      
      // 可以在这里添加API调用保存点赞状态
    },
    
    // 刷新笔记
    refreshNotes(showLoading = true) {
      if (showLoading) {
        this.isRefreshing = true;
      }
      
      this.notes = [];
      this.page = 1;
      this.hasMore = true;
      this.syncedWithServer = false; // 重置同步标志，确保刷新时重新同步
      
      return this.loadNotes().then(() => {
        if (showLoading) {
          this.isRefreshing = false;
          uni.stopPullDownRefresh();
        }
      });
    },
    
    // 加载更多笔记
    loadMoreNotes() {
      this.loadNotes();
    },
    
    // 查看笔记详情
    viewNoteDetail(id) {
      // 从笔记列表中查找对应的笔记
      const note = this.notes.find(item => item.id === id);
      if (!note) return;
      
      // 将当前笔记详情保存到本地，以便详情页获取
      uni.setStorageSync('currentNote', note);
      
      // 导航到详情页
      uni.navigateTo({
        url: `/pages/detail/detail?id=${id}&type=note`
      });
    },
    
    // 显示操作菜单
    showOptions(index) {
      this.currentNoteIndex = index;
      this.showActionSheet = true;
    },
    
    // 编辑笔记
    editNote(index) {
      if (index < 0 || index >= this.notes.length) return;
      
      const note = this.notes[index];
      uni.navigateTo({
        url: `/pages/note/edit?id=${note.id}`
      });
      this.showActionSheet = false;
    },
    
    // 删除笔记
    deleteNote(index) {
      if (index < 0 || index >= this.notes.length) return;
      
      const note = this.notes[index];
      
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这条笔记吗？删除后将无法恢复',
        success: async (res) => {
          if (res.confirm) {
            try {
              uni.showLoading({ title: '删除中...' });
              
              // 如果有ID且是整数类型，则调用API删除数据库中的记录
              if (note.id && Number.isInteger(Number(note.id))) {
                try {
                  // 调用API删除后端数据库中的记录
                  await deletePost(note.id);
                  console.log('数据库中的博文已删除');
                } catch (error) {
                  console.error('删除数据库记录失败:', error);
                  // 即使后端删除失败，也继续删除本地笔记
                  uni.showToast({
                    title: '服务器同步失败，但本地笔记已删除',
                    icon: 'none',
                    duration: 2000
                  });
                }
              }
              
              // 删除本地笔记
              this.notes.splice(index, 1);
              
              // 更新本地存储
              uni.setStorageSync('userNotes', this.notes);
              
              uni.hideLoading();
              uni.showToast({
                title: '删除成功',
                icon: 'success'
              });
            } catch (error) {
              uni.hideLoading();
              uni.showToast({
                title: '删除失败，请重试',
                icon: 'none'
              });
              console.error('删除笔记失败:', error);
            }
          }
        }
      });
      this.showActionSheet = false;
    },
    
    // 导航到景点浏览页
    navigateToExplore() {
      uni.switchTab({
        url: '/pages/index/index'
      });
    }
  }
}
</script>

<style>
.notes-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
  padding-top: 20rpx;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80rpx 40rpx;
}

.empty-icon {
  width: 300rpx;
  height: 300rpx;
  margin-bottom: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0,122,255,0.05);
  border-radius: 50%;
}

.empty-text {
  font-size: 34rpx;
  color: #333;
  font-weight: 600;
  margin-bottom: 20rpx;
}

.empty-tips {
  font-size: 28rpx;
  color: #999;
  margin-bottom: 60rpx;
  text-align: center;
  line-height: 1.5;
}

.create-btn {
  width: 320rpx;
  height: 80rpx;
  line-height: 80rpx;
  background: #3182ce;
  color: #fff;
  font-size: 30rpx;
  border-radius: 40rpx;
  box-shadow: 0 4rpx 16rpx rgba(49, 130, 206, 0.3);
}

/* 瀑布流样式 - 借鉴首页样式 */
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
  display: flex;
  flex-direction: column;
}

.card-item {
  margin-bottom: 24rpx;
  background: #fff;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 2rpx 12rpx rgba(0,0,0,0.05);
  transition: all 0.3s;
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 520rpx; /* 设置固定高度 */
}

.card-item:active {
  transform: scale(0.98);
}

.card-image-container {
  width: 100%;
  height: 320rpx;
  position: relative;
  overflow: hidden;
  border-radius: 16rpx 16rpx 0 0;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 20rpx;
  flex: 1;
  display: flex;
  flex-direction: column;
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
  height: 2.8em;
}

.card-title:not(.expanded) {
  -webkit-line-clamp: 2;
  line-clamp: 2;
}

.expand-control {
  margin-top: 10rpx;
  text-align: right;
}

.expand-btn {
  font-size: 24rpx;
  color: #ff2442;
  position: relative;
  padding-right: 16rpx;
}

.expand-btn::after {
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

.note-meta {
  display: flex;
  align-items: center;
  font-size: 24rpx;
  color: #999;
  margin-bottom: 16rpx;
  height: 40rpx;
}

.note-time {
  margin-right: 20rpx;
  white-space: nowrap;
}

.note-location {
  display: flex;
  align-items: center;
  max-width: 60%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.note-location:before {
  content: '';
  display: inline-block;
  width: 24rpx;
  height: 24rpx;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="%23999"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>') no-repeat center;
  background-size: contain;
  margin-right: 6rpx;
}

.interaction-bar {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 24rpx;
  height: 60rpx;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 6rpx;
  height: 100%;
}

.count {
  font-size: 24rpx;
  color: #666;
}

.like-btn.active .count {
  color: #ff5656;
}

.loading-more, .no-more {
  text-align: center;
  padding: 30rpx 0;
  color: #999;
  font-size: 26rpx;
}

.loading-more {
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading-more text {
  margin-left: 10rpx;
}

.action-sheet {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0,0,0,0.5);
  z-index: 999;
  display: flex;
  align-items: flex-end;
}

.action-sheet-content {
  width: 100%;
  background-color: #fff;
  border-radius: 24rpx 24rpx 0 0;
  overflow: hidden;
}

.action-item {
  height: 110rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.action-item uni-icons {
  margin-right: 10rpx;
}

.action-item.edit {
  color: #007AFF;
}

.action-item.delete {
  color: #FF3B30;
}

.action-item.cancel {
  color: #666;
  margin: 10rpx 0;
  border-bottom: none;
}

/* 创建一个无图片时的占位区域 */
.no-image-placeholder {
  width: 100%;
  height: 320rpx;
  background: #f0f2f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #bbb;
  font-size: 28rpx;
}

.empty-image-icon {
  font-size: 80rpx;
  margin-bottom: 10rpx;
}
</style> 