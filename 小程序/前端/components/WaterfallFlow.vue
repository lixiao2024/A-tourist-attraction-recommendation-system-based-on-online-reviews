<template>
  <scroll-view 
    class="waterfall-scroll"
    scroll-y
    :show-scrollbar="false"
    @scrolltolower="onLoadMore"
    refresher-enabled
    @refresherrefresh="onRefresh"
    :refresher-triggered="isRefreshing"
    :lower-threshold="lowerThreshold"
  >
    <view class="waterfall-container">
      <view class="waterfall-column">
        <slot name="left-column"></slot>
      </view>
      
      <view class="waterfall-column">
        <slot name="right-column"></slot>
      </view>
    </view>
    
    <!-- 加载更多提示 -->
    <view class="loading-more" v-if="isLoading">
      <uni-icons type="spinner-cycle" size="20" color="#999"></uni-icons>
      <text>{{ loadingText }}</text>
    </view>
    
    <!-- 没有更多数据提示 -->
    <view class="no-more" v-if="!hasMore && !isEmpty">
      <text>{{ noMoreText }}</text>
    </view>
    

  </scroll-view>
</template>

<script>
export default {
  name: 'WaterfallFlow',
  props: {
    // 是否正在加载数据
    isLoading: {
      type: Boolean,
      default: false
    },
    // 是否正在刷新
    isRefreshing: {
      type: Boolean,
      default: false
    },
    // 是否还有更多数据
    hasMore: {
      type: Boolean,
      default: true
    },
    // 是否为空列表
    isEmpty: {
      type: Boolean,
      default: false
    },
    // 加载更多触发的阈值
    lowerThreshold: {
      type: [Number, String],
      default: 100
    },
    // 加载中的文本
    loadingText: {
      type: String,
      default: '加载更多中...'
    },
    // 没有更多数据的文本
    noMoreText: {
      type: String,
      default: '-- 已经到底啦 --'
    },
    // 空数据提示文本
    emptyText: {
      type: String,
      default: '暂无数据'
    }
  },
  methods: {
    // 触发加载更多
    onLoadMore() {
      // 如果正在加载或没有更多数据，不触发加载更多
      if (this.isLoading || !this.hasMore) return;
      
      // 向父组件发出加载更多的事件
      this.$emit('load-more');
    },
    
    // 触发刷新
    onRefresh() {
      // 如果正在刷新，不重复触发
      if (this.isRefreshing) return;
      
      // 向父组件发出刷新的事件
      this.$emit('refresh');
    }
  }
}
</script>

<style lang="scss">
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

.no-more {
  text-align: center;
  padding: 30rpx 0;
  color: #999;
  font-size: 24rpx;
}

.empty-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100rpx 0;
  
  .empty-image {
    width: 200rpx;
    height: 200rpx;
    margin-bottom: 20rpx;
  }
  
  .empty-text {
    color: #999;
    font-size: 28rpx;
  }
}
</style> 