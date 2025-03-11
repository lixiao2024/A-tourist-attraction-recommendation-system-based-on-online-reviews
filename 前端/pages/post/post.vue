<template>
  <view class="post-page">
    <!-- 评论输入区 -->
    <textarea 
      v-model="content"
      class="content-input"
      placeholder="写下你的旅行体验..."
      maxlength="500"
      auto-height
    ></textarea>

    <!-- 话题和定位区域 -->
    <view class="tools-bar">
      <view class="tool-item" @click="showTopicInput">
        <uni-icons type="paperplane" size="20" color="#666"></uni-icons>
        <text class="tool-text"># 添加话题</text>
      </view>
      <view class="tool-item" @click="getLocation">
        <uni-icons type="location" size="20" color="#666"></uni-icons>
        <text class="tool-text">{{ location || '添加位置' }}</text>
      </view>
    </view>

    <!-- 话题输入弹窗 -->
    <uni-popup ref="topicPopup" type="bottom">
      <view class="topic-popup">
        <view class="popup-header">
          <text>添加话题</text>
          <text class="close-btn" @click="closeTopicPopup">关闭</text>
        </view>
        <input 
          v-model="topicInput"
          class="topic-input"
          placeholder="输入话题，回车添加"
          @confirm="addTopic"
        />
        <!-- 已添加的话题展示 -->
        <view class="topics-list" v-if="topics.length > 0">
          <view 
            v-for="(topic, index) in topics" 
            :key="index"
            class="topic-tag"
          >
            #{{ topic }}
            <text class="delete-topic" @click="removeTopic(index)">×</text>
          </view>
        </view>
      </view>
    </uni-popup>

    <button class="submit-btn" @click="submitComment">发布评论</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      content: '',
      location: '',
      topics: [],
      topicInput: ''
    }
  },
  methods: {
    // 获取位置信息
    getLocation() {
      uni.showLoading({ title: '获取位置中...' })
      uni.getLocation({
        type: 'gcj02',
        success: (res) => {
          this.reverseGeocode(res.longitude, res.latitude)
        },
        fail: () => {
          uni.showToast({
            title: '获取位置失败',
            icon: 'none'
          })
        },
        complete: () => {
          uni.hideLoading()
        }
      })
    },

    // 反向地理编码
    reverseGeocode(longitude, latitude) {
      // 这里应该调用地图API进行反向地理编码
      // 示例中使用模拟数据
      this.location = '北京市朝阳区'
    },

    // 显示话题输入弹窗
    showTopicInput() {
      this.$refs.topicPopup.open()
    },

    // 关闭话题输入弹窗
    closeTopicPopup() {
      this.$refs.topicPopup.close()
      this.topicInput = ''
    },

    // 添加话题
    addTopic() {
      if (this.topicInput.trim()) {
        if (!this.topics.includes(this.topicInput.trim())) {
          this.topics.push(this.topicInput.trim())
        }
        this.topicInput = ''
      }
    },

    // 删除话题
    removeTopic(index) {
      this.topics.splice(index, 1)
    },

    // 提交评论
    submitComment() {
      if (!this.content.trim()) {
        uni.showToast({
          title: '请输入评论内容',
          icon: 'none'
        })
        return
      }

      // 构建评论数据
      const commentData = {
        content: this.content,
        location: this.location,
        topics: this.topics,
        timestamp: new Date().getTime()
      }

      console.log('评论数据：', commentData)
      
      // 这里应该调用API提交评论
      uni.showToast({
        title: '评论发布成功',
        icon: 'success'
      })
      
      setTimeout(() => {
        uni.navigateBack()
      }, 1500)
    }
  }
}
</script>

<style lang="scss">
.post-page {
  padding: 36rpx;
  background-color: #f8fafc;
}

.content-input {
  width: 100%;
  min-height: 320rpx;
  padding: 28rpx;
  border: 2rpx solid #e2e8f0;
  border-radius: 24rpx;
  margin-bottom: 30rpx;
  font-size: 32rpx;
  color: #2d3748;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.02);
  transition: all 0.3s ease;
  
  &:focus {
    border-color: #3182ce;
    box-shadow: 0 4rpx 16rpx rgba(49, 130, 206, 0.1);
  }
}

.tools-bar {
  display: flex;
  padding: 24rpx 0;
  border-bottom: 2rpx solid #e2e8f0;
  margin-bottom: 48rpx;
}

.tool-item {
  display: flex;
  align-items: center;
  margin-right: 40rpx;
  padding: 14rpx 24rpx;
  background: #f1f5f9;
  border-radius: 36rpx;
  transition: all 0.25s ease;
  
  &:active {
    transform: scale(0.98);
    background: #e2e8f0;
  }
}

.tool-text {
  font-size: 26rpx;
  color: #4a5568;
  margin-left: 12rpx;
  font-weight: 500;
}

.submit-btn {
  background: linear-gradient(135deg, #3182ce, #0056b3);
  color: white;
  border-radius: 50rpx;
  padding: 24rpx 0;
  font-size: 32rpx;
  font-weight: 500;
  letter-spacing: 2rpx;
  box-shadow: 0 6rpx 16rpx rgba(0, 86, 179, 0.2);
  transition: all 0.3s ease;
  
  &:active {
    transform: translateY(2rpx);
    box-shadow: 0 2rpx 8rpx rgba(0, 86, 179, 0.2);
  }
}

.topic-popup {
  background: #fff;
  padding: 36rpx;
  border-radius: 24rpx 24rpx 0 0;
  box-shadow: 0 -4rpx 24rpx rgba(0, 0, 0, 0.06);
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 36rpx;
  
  text {
    font-size: 32rpx;
    font-weight: 600;
    color: #1a202c;
  }
}

.close-btn {
  color: #4a5568;
  font-size: 28rpx;
  padding: 10rpx 20rpx;
  border-radius: 30rpx;
  background: #f1f5f9;
  transition: all 0.25s ease;
  
  &:active {
    background: #e2e8f0;
  }
}

.topic-input {
  width: 100%;
  height: 88rpx;
  border: 2rpx solid #e2e8f0;
  border-radius: 44rpx;
  padding: 0 32rpx;
  margin-bottom: 24rpx;
  font-size: 30rpx;
  color: #2d3748;
  transition: all 0.3s ease;
  
  &:focus {
    border-color: #3182ce;
    box-shadow: 0 2rpx 12rpx rgba(49, 130, 206, 0.1);
  }
}

.topics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 24rpx;
  padding: 24rpx 0;
}

.topic-tag {
  background: #edf2f7;
  padding: 12rpx 24rpx;
  border-radius: 36rpx;
  font-size: 26rpx;
  color: #4a5568;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.03);
  transition: all 0.25s ease;
  
  &:active {
    transform: scale(0.98);
  }
}

.delete-topic {
  margin-left: 12rpx;
  color: #718096;
  font-size: 30rpx;
  height: 36rpx;
  width: 36rpx;
  line-height: 32rpx;
  text-align: center;
  border-radius: 50%;
  transition: all 0.25s ease;
  
  &:active {
    background: rgba(0, 0, 0, 0.1);
  }
}
</style>