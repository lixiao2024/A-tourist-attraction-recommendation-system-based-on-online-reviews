<template>
  <view class="card-item" @click="onCardClick">
    <!-- 图片区域 -->
    <view class="image-container">
      <image 
        v-if="getCoverImage"
        class="card-image" 
        :src="getCoverImage" 
        mode="aspectFill"
        @error="handleImageError"
      ></image>
      <!-- 评价标识 -->
      <view 
        v-if="note.sentimentType" 
        :class="['sentiment-badge', note.sentimentType === 'positive' ? 'positive' : 'negative']"
      >
        {{ note.sentimentType === 'positive' ? '种草' : '避雷' }}
      </view>
    </view>
    
    <!-- 内容区域 -->
    <view class="card-content">
      <text class="card-title" :class="{expanded: note.expanded}">{{ note.title || note.content }}</text>
      
      <!-- 展开/收起控制 -->
      <view 
        v-if="showExpandControl"
        class="expand-control"
      >
        <text 
          v-if="!note.expanded"
          class="expand-btn"
          @click.stop="toggleExpand"
        >展开</text>
      </view>
      
      <!-- 用户信息 -->
      <view class="user-info">
        <image class="user-avatar" :src="note.avatar" mode="aspectFill"></image>
        <text class="user-name">{{ note.nickname }}</text>
      </view>
      
      <!-- 互动栏 -->
      <view class="interaction-bar">
        <view 
          class="action-btn like-btn" 
          :class="{active: note.isLiked}" 
          @click.stop="onLike"
        >
          <uni-icons 
            :type="note.isLiked ? 'heart-filled' : 'heart'" 
            size="20" 
            :color="note.isLiked ? '#ff5656' : '#666'"
          ></uni-icons>
          <text class="count">{{ note.likeCount || '' }}</text>
        </view>
        <view class="action-btn comment-btn" @click.stop="onComment">
          <uni-icons type="chat" size="20" color="#666"></uni-icons>
          <text class="count">{{ note.commentCount || '' }}</text>
        </view>
        <view class="action-btn share-btn" @click.stop="onShare">
          <uni-icons type="paperplane" size="20" color="#666"></uni-icons>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  name: 'TravelNoteCard',
  props: {
    note: {
      type: Object,
      required: true
    }
  },
  computed: {
    // 获取封面图
    getCoverImage() {
      // 优先使用images数组的第一张图片
      if (this.note.images && this.note.images.length > 0) {
        return this.note.images[0];
      }
      // 其次使用cover_image字段
      else if (this.note.cover_image) {
        return this.note.cover_image;
      }
      // 如果没有任何图片，返回默认图片
      return '/static/default-image.png';
    },
    // 判断是否显示展开控制按钮
    showExpandControl() {
      // 判断文本长度，如果是title，则超过40字符显示展开按钮
      // 如果是content，则超过50字符显示展开按钮
      if (this.note.title && this.note.title.length > 40) {
        return true;
      }
      return this.note.content && this.note.content.length > 50;
    }
  },
  methods: {
    // 处理图片加载错误
    handleImageError() {
      // 使用默认图片
      let updatedNote = { ...this.note };
      
      // 根据情况更新不同的图片字段
      if (this.note.images && this.note.images.length > 0) {
        updatedNote.images = ['/static/default-image.png'];
      } 
      if (this.note.cover_image) {
        updatedNote.cover_image = '/static/default-image.png';
      }
      
      this.$emit('update:note', updatedNote);
    },
    
    // 点击卡片
    onCardClick() {
      this.$emit('card-click', this.note.id);
    },
    
    // 展开/收起控制
    toggleExpand() {
      this.$emit('update:note', {
        ...this.note,
        expanded: !this.note.expanded
      });
    },
    
    // 点赞功能
    onLike() {
      this.$emit('like', this.note.id);
    },
    
    // 评论功能
    onComment() {
      this.$emit('comment', this.note.id);
    },
    
    // 分享功能
    onShare() {
      this.$emit('share', this.note);
    }
  }
}
</script>

<style lang="scss">
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

.image-container {
  position: relative;
  width: 100%;
}

.card-image {
  width: 100%;
  height: 320rpx; /* 固定高度 */
  border-radius: 16rpx 16rpx 0 0;
  object-fit: cover; /* 确保图片完全填充容器并保持比例 */
}

.sentiment-badge {
  position: absolute;
  top: 16rpx;
  right: 16rpx;
  padding: 6rpx 16rpx;
  border-radius: 30rpx;
  font-size: 24rpx;
  font-weight: bold;
  z-index: 2;
  box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.2);
  
  &.positive {
    background-color: #44b549;
    color: #fff;
  }
  
  &.negative {
    background-color: #ff5656;
    color: #fff;
  }
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
</style> 