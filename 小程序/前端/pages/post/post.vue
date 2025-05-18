<template>
  <view class="post-page">
    <!-- 顶部标题区 -->
    <view class="header-section">
      <text class="page-title">发布评论</text>
      <text class="subtitle">分享你的旅行体验</text>
    </view>
    
    <!-- 标题输入区 -->
    <view class="content-card">
      <input 
        v-model="title"
        class="title-input"
        placeholder="请输入标题（可选）"
        maxlength="50"
      />
      <view class="separator"></view>
      <textarea 
        v-model="content"
        class="content-input"
        placeholder="写下你的旅行体验，分享精彩瞬间..."
        maxlength="500"
        auto-height
      ></textarea>
      
      <!-- 图片上传区域 -->
      <view class="image-upload-area" v-if="images.length > 0">
        <scroll-view scroll-x class="image-scroll">
          <view class="image-list">
            <view 
              v-for="(image, index) in images" 
              :key="index"
              class="image-item"
            >
              <image class="preview-image" :src="image" mode="aspectFill" @click="previewImage(index)"></image>
              <view class="delete-image" @click.stop="deleteImage(index)">
                <text class="delete-icon">×</text>
              </view>
            </view>
          </view>
        </scroll-view>
      </view>
      
      <view class="content-footer">
        <text class="word-count">{{ content.length }}/500</text>
      </view>
    </view>

    <!-- 封面图预览区域 -->
    <view class="cover-preview" v-if="coverImage">
      <view class="preview-header">
        <text class="preview-title">封面图</text>
        <view class="preview-action" @click="deleteCoverImage">
          <uni-icons type="trash" size="18" color="#718096"></uni-icons>
          <text class="action-text">删除</text>
        </view>
      </view>
      <view class="cover-container">
        <image class="cover-image" :src="coverImage" mode="aspectFill" @click="previewCoverImage"></image>
      </view>
    </view>

    <!-- 话题和定位区域 -->
    <view class="tools-section">
      <text class="section-title">添加更多信息</text>
      <view class="tools-bar">
        <view class="tool-item" hover-class="tool-item-hover" @click="showTopicInput">
          <view class="tool-icon">
            <uni-icons type="paperplane" size="20" color="#3182ce"></uni-icons>
          </view>
          <text class="tool-text"># {{ topics.length > 0 ? `已添加${topics.length}个话题` : '添加话题' }}</text>
        </view>
        <view class="tool-item" hover-class="tool-item-hover" @click="getLocation">
          <view class="tool-icon">
            <uni-icons type="location" size="20" color="#3182ce"></uni-icons>
          </view>
          <text class="tool-text">{{ location || '添加位置' }}</text>
        </view>
        <view class="tool-item" hover-class="tool-item-hover" @click="chooseImage">
          <view class="tool-icon">
            <uni-icons type="image" size="20" color="#3182ce"></uni-icons>
          </view>
          <text class="tool-text">{{ images.length > 0 ? `已上传${images.length}张图片` : '上传图片' }}</text>
        </view>
        <view class="tool-item" hover-class="tool-item-hover" @click="chooseCoverImage">
          <view class="tool-icon">
            <uni-icons type="camera" size="20" color="#3182ce"></uni-icons>
          </view>
          <text class="tool-text">{{ coverImage ? '更换封面' : '选择封面' }}</text>
        </view>
      </view>
    </view>
    
    <!-- 已添加话题区域 -->
    <view class="topics-preview" v-if="topics.length > 0">
      <scroll-view scroll-x class="topics-scroll">
        <view class="topics-list">
          <view 
            v-for="(topic, index) in topics" 
            :key="index"
            class="topic-tag"
            hover-class="topic-tag-hover"
          >
            #{{ topic }}
            <text class="delete-topic" @click.stop="removeTopic(index)">×</text>
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 话题输入弹窗 -->
    <uni-popup ref="topicPopup" type="bottom">
      <view class="topic-popup">
        <view class="popup-header">
          <text class="popup-title">添加话题</text>
          <view class="close-btn" hover-class="close-btn-hover" @click="closeTopicPopup">关闭</view>
        </view>
        <view class="search-box">
          <uni-icons type="search" size="20" color="#a0aec0"></uni-icons>
          <input 
            v-model="topicInput"
            class="topic-input"
            placeholder="搜索或创建新话题"
            confirm-type="done"
            @confirm="addTopic"
          />
        </view>
        
        <!-- 热门话题推荐 -->
        <view class="trending-topics" v-if="!topicInput">
          <text class="trending-title">热门话题</text>
          <view class="trending-list">
            <view 
              class="trending-tag" 
              hover-class="trending-tag-hover"
              v-for="(item, index) in ['旅行', '美食', '风景', '城市', '历史', '文化']" 
              :key="index"
              @click="quickAddTopic(item)"
            >
              #{{ item }}
            </view>
          </view>
        </view>
        
        <!-- 已添加的话题展示 -->
        <view class="added-topics" v-if="topics.length > 0">
          <text class="added-title">已添加话题</text>
          <view class="topics-list popup-topics">
            <view 
              v-for="(topic, index) in topics" 
              :key="index"
              class="topic-tag popup-tag"
              hover-class="topic-tag-hover"
            >
              #{{ topic }}
              <text class="delete-topic" @click.stop="removeTopic(index)">×</text>
            </view>
          </view>
        </view>
      </view>
    </uni-popup>

    <view class="submit-wrapper">
      <button class="submit-btn" hover-class="submit-btn-hover" @click="submitComment">
        <text class="btn-text">发布评论</text>
        <uni-icons type="arrowright" size="18" color="#fff"></uni-icons>
      </button>
    </view>
  </view>
</template>

<script>
import { publishComment } from '../../request/api.js';

export default {
  data() {
    return {
      content: '',
      location: '',
      topics: [],
      topicInput: '',
      images: [], // 存储上传的图片临时路径
      coverImage: '', // 存储封面图片路径
      isSubmitting: false, // 是否正在提交
      title: '' // 博文标题
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
          uni.showToast({
            title: '话题添加成功',
            icon: 'none'
          })
        } else {
          uni.showToast({
            title: '该话题已添加',
            icon: 'none'
          })
        }
        this.topicInput = ''
      }
    },
    
    // 快速添加推荐话题
    quickAddTopic(topic) {
      if (!this.topics.includes(topic)) {
        this.topics.push(topic)
        uni.showToast({
          title: '话题添加成功',
          icon: 'none'
        })
      } else {
        uni.showToast({
          title: '该话题已添加',
          icon: 'none'
        })
      }
    },

    // 删除话题
    removeTopic(index) {
      this.topics.splice(index, 1)
      uni.showToast({
        title: '已删除',
        icon: 'none'
      })
    },

    // 选择图片
    chooseImage() {
      uni.chooseImage({
        count: 9 - this.images.length, // 最多选择9张图片
        sizeType: ['compressed'], // 只使用压缩图片
        sourceType: ['album', 'camera'], // 从相册或相机选择
        success: (res) => {
          // 将选择的图片添加到图片数组
          const tempFiles = res.tempFilePaths;
          if (this.images.length + tempFiles.length > 9) {
            uni.showToast({
              title: '最多上传9张图片',
              icon: 'none'
            });
            // 只添加能添加的部分
            const remainCount = 9 - this.images.length;
            this.images = [...this.images, ...tempFiles.slice(0, remainCount)];
          } else {
            this.images = [...this.images, ...tempFiles];
          }
        },
        fail: (err) => {
          console.error('选择图片失败', err);
          uni.showToast({
            title: '选择图片失败',
            icon: 'none'
          });
        }
      });
    },
    
    // 选择封面图片
    chooseCoverImage() {
      uni.chooseImage({
        count: 1, // 只选择1张图片作为封面
        sizeType: ['compressed'], // 只使用压缩图片
        sourceType: ['album', 'camera'], // 从相册或相机选择
        success: (res) => {
          this.coverImage = res.tempFilePaths[0];
          uni.showToast({
            title: '封面设置成功',
            icon: 'success'
          });
        },
        fail: (err) => {
          console.error('选择封面失败', err);
          uni.showToast({
            title: '选择封面失败',
            icon: 'none'
          });
        }
      });
    },
    
    // 预览封面图片
    previewCoverImage() {
      if (this.coverImage) {
        uni.previewImage({
          urls: [this.coverImage],
          current: 0
        });
      }
    },
    
    // 删除封面图片
    deleteCoverImage() {
      uni.showModal({
        title: '提示',
        content: '确定要删除封面图吗？',
        success: (res) => {
          if (res.confirm) {
            this.coverImage = '';
            uni.showToast({
              title: '已删除封面图',
              icon: 'none'
            });
          }
        }
      });
    },
    
    // 预览图片
    previewImage(index) {
      uni.previewImage({
        urls: this.images,
        current: index
      });
    },
    
    // 删除图片
    deleteImage(index) {
      uni.showModal({
        title: '提示',
        content: '确定要删除这张图片吗？',
        success: (res) => {
          if (res.confirm) {
            this.images.splice(index, 1);
          }
        }
      });
    },
    
    // 自动生成标题
    generateTitle() {
      if (this.content) {
        // 从内容中提取前几个字作为标题
        const maxTitleLength = 20;
        this.title = this.content.split('\n')[0].trim().slice(0, maxTitleLength);
        
        // 如果截取的内容太短，则加上"旅行分享"
        if (this.title.length < 5) {
          this.title = '旅行分享：' + this.title;
        }
        
        // 如果标题末尾是标点符号，则去掉
        const punctuation = [',', '，', '.', '。', '!', '！', '?', '？', ';', '；', ':', '：'];
        if (punctuation.includes(this.title[this.title.length - 1])) {
          this.title = this.title.slice(0, -1);
        }
      }
    },

    // 提交评论
    async submitComment() {
      if (!this.content.trim()) {
        uni.showToast({
          title: '请输入评论内容',
          icon: 'none'
        })
        return
      }
      
      // 防止重复提交
      if (this.isSubmitting) {
        return;
      }
      
      this.isSubmitting = true;
      
      // 生成标题（如果没有手动设置）
      if (!this.title) {
        this.generateTitle();
      }
      
      try {
        uni.showLoading({ 
          title: '准备发布...',
          mask: true
        });
        
        // 构建评论数据
        const commentData = {
          content: this.content,
          title: this.title || this.content.substring(0, 20) + '...',
          location: this.location,
          topics: this.topics
        }
        
        console.log('评论数据准备就绪，开始上传图片');
        
        if (this.images.length > 0) {
          uni.showLoading({ 
            title: '上传图片中...',
            mask: true
          });
        }
        
        // 使用API发布评论，并上传图片
        const result = await publishComment(commentData, this.images, this.coverImage);
        
        console.log('发布成功，返回结果:', result);
        
        uni.hideLoading();
        uni.showToast({
          title: '发布成功',
          icon: 'success',
          duration: 2000
        });
        
        // 发布成功后跳转到首页或笔记页
        setTimeout(() => {
          // 使用switchTab代替navigateBack，避免在第一页时的错误
          uni.switchTab({
            url: '/pages/mine/mine'
          });
        }, 2000);
      } catch (error) {
        console.error('发布失败', error);
        uni.hideLoading();
        
        let errorMsg = '发布失败，请重试';
        
        // 检查错误对象结构，提取详细错误信息
        if (error && error.detail) {
          if (Array.isArray(error.detail)) {
            // 处理422验证错误
            errorMsg = error.detail[0]?.msg || '数据验证失败，请检查内容';
          } else if (typeof error.detail === 'string') {
            // 直接显示错误信息
            errorMsg = error.detail;
          }
        } else if (error && error.errMsg) {
          if (error.errMsg.includes('request:fail')) {
            errorMsg = '网络连接失败，请检查网络设置';
          } else if (error.errMsg.includes('uploadFile:fail')) {
            errorMsg = '图片上传失败，请重试';
          }
        }
        
        uni.showToast({
          title: errorMsg,
          icon: 'none',
          duration: 3000
        });
      } finally {
        this.isSubmitting = false;
      }
    }
  }
}
</script>

<style lang="scss">
.post-page {
  padding: 30rpx 30rpx 120rpx;
  background-color: #f8fafc;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header-section {
  margin-bottom: 30rpx;
  
  .page-title {
    font-size: 42rpx;
    font-weight: 700;
    color: #1a202c;
    margin-bottom: 8rpx;
    display: block;
  }
  
  .subtitle {
    font-size: 28rpx;
    color: #718096;
    display: block;
  }
}

.content-card {
  background: #ffffff;
  border-radius: 24rpx;
  padding: 24rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.06);
  position: relative;
}

.title-input {
  width: 100%;
  padding: 16rpx;
  border: none;
  margin-bottom: 20rpx;
  font-size: 32rpx;
  color: #2d3748;
  line-height: 1.6;
}

.separator {
  height: 1rpx;
  background-color: #f0f4f8;
  margin-bottom: 20rpx;
}

.content-input {
  width: 100%;
  min-height: 240rpx;
  padding: 16rpx;
  border: none;
  margin-bottom: 20rpx;
  font-size: 32rpx;
  color: #2d3748;
  line-height: 1.6;
}

.content-footer {
  display: flex;
  justify-content: flex-end;
  padding: 16rpx;
  border-top: 1rpx solid #f0f4f8;
  
  .word-count {
    font-size: 24rpx;
    color: #a0aec0;
  }
}

.cover-preview {
  background: #ffffff;
  border-radius: 24rpx;
  padding: 24rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.06);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.preview-title {
  font-size: 30rpx;
  font-weight: 600;
  color: #4a5568;
}

.preview-action {
  display: flex;
  align-items: center;
  padding: 8rpx 16rpx;
  background: #f7fafc;
  border-radius: 30rpx;
  
  .action-text {
    font-size: 24rpx;
    color: #718096;
    margin-left: 6rpx;
  }
}

.cover-container {
  width: 100%;
  height: 300rpx;
  border-radius: 16rpx;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tools-section {
  margin-bottom: 30rpx;
  
  .section-title {
    font-size: 30rpx;
    font-weight: 600;
    color: #4a5568;
    margin-bottom: 20rpx;
    display: block;
  }
}

.tools-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.tool-item {
  display: flex;
  align-items: center;
  padding: 20rpx 24rpx;
  background: #ffffff;
  border-radius: 16rpx;
  box-shadow: 0 8rpx 30rpx rgba(0, 0, 0, 0.06);
  transition: all 0.25s ease;
  flex: 1;
  min-width: 45%;
  
  .tool-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60rpx;
    height: 60rpx;
    background: rgba(49, 130, 206, 0.1);
    border-radius: 50%;
    margin-right: 16rpx;
  }
}

.tool-item-hover {
  transform: translateY(-4rpx);
  box-shadow: 0 12rpx 36rpx rgba(0, 0, 0, 0.08);
  background: #f9fafc;
}

.tool-text {
  font-size: 28rpx;
  color: #4a5568;
  font-weight: 500;
}

.topics-preview {
  margin-bottom: 30rpx;
}

.topics-scroll {
  width: 100%;
  white-space: nowrap;
}

.topics-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
  padding: 10rpx 0;
}

.topic-tag {
  display: inline-flex;
  align-items: center;
  padding: 12rpx 24rpx;
  background: rgba(49, 130, 206, 0.1);
  color: #3182ce;
  border-radius: 40rpx;
  font-size: 26rpx;
  font-weight: 500;
  transition: all 0.2s ease;
}

.topic-tag-hover {
  background: rgba(49, 130, 206, 0.2);
}

.delete-topic {
  margin-left: 12rpx;
  width: 36rpx;
  height: 36rpx;
  line-height: 34rpx;
  text-align: center;
  font-size: 30rpx;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.1);
  color: #fff;
}

.submit-wrapper {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 30rpx;
  background: rgba(248, 250, 252, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 -4rpx 20rpx rgba(0, 0, 0, 0.05);
  z-index: 100;
}

.submit-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2196f3, #2979ff);
  color: white;
  border-radius: 50rpx;
  padding: 30rpx 0;
  font-size: 32rpx;
  font-weight: 600;
  box-shadow: 0 12rpx 36rpx rgba(41, 121, 255, 0.3);
  transition: all 0.3s ease;
  width: 100%;
  
  .btn-text {
    margin-right: 10rpx;
  }
}

.submit-btn-hover {
  transform: translateY(-4rpx);
  box-shadow: 0 16rpx 48rpx rgba(41, 121, 255, 0.4);
  background: linear-gradient(135deg, #1e88e5, #2962ff);
}

.topic-popup {
  background: #fff;
  padding: 40rpx 30rpx;
  border-radius: 32rpx 32rpx 0 0;
  box-shadow: 0 -4rpx 30rpx rgba(0, 0, 0, 0.1);
  min-height: 60vh;
}

.popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 36rpx;
  
  .popup-title {
    font-size: 36rpx;
    font-weight: 700;
    color: #1a202c;
  }
}

.close-btn {
  color: #718096;
  font-size: 28rpx;
  padding: 10rpx 24rpx;
  border-radius: 30rpx;
  background: #f1f5f9;
  transition: all 0.25s ease;
}

.close-btn-hover {
  background: #e2e8f0;
}

.search-box {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  padding: 12rpx 24rpx;
  border-radius: 40rpx;
  margin-bottom: 40rpx;
}

.topic-input {
  flex: 1;
  height: 70rpx;
  font-size: 28rpx;
  color: #4a5568;
  margin-left: 16rpx;
}

.trending-topics {
  margin-bottom: 40rpx;
  
  .trending-title {
    font-size: 28rpx;
    font-weight: 600;
    color: #718096;
    margin-bottom: 20rpx;
    display: block;
  }
}

.trending-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.trending-tag {
  padding: 12rpx 24rpx;
  background: #f7fafc;
  border-radius: 40rpx;
  font-size: 26rpx;
  color: #4a5568;
  transition: all 0.2s ease;
}

.trending-tag-hover {
  background: #edf2f7;
  color: #3182ce;
}

.added-topics {
  margin-top: 40rpx;
  
  .added-title {
    font-size: 28rpx;
    font-weight: 600;
    color: #718096;
    margin-bottom: 20rpx;
    display: block;
  }
}

.popup-topics {
  margin-bottom: 30rpx;
}

.popup-tag {
  margin-bottom: 16rpx;
}

.image-upload-area {
  margin: 20rpx 0;
}

.image-scroll {
  width: 100%;
  white-space: nowrap;
}

.image-list {
  display: flex;
  padding: 10rpx 0;
}

.image-item {
  position: relative;
  width: 160rpx;
  height: 160rpx;
  margin-right: 20rpx;
  border-radius: 16rpx;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.delete-image {
  position: absolute;
  top: 6rpx;
  right: 6rpx;
  width: 40rpx;
  height: 40rpx;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-icon {
  color: #fff;
  font-size: 28rpx;
  line-height: 1;
}
</style>