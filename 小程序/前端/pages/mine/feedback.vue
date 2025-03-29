<template>
  <view class="feedback-container">
    <!-- 反馈类型选择 -->
    <view class="section">
      <text class="section-title">反馈类型</text>
      <uni-segmented-control 
        :current="currentType" 
        :values="types" 
        @clickItem="onTypeChange"
        style-type="button"
      />
    </view>

    <!-- 反馈内容输入 -->
    <view class="section">
      <text class="section-title">问题描述</text>
      <uni-easyinput 
        type="textarea" 
        v-model="content" 
        placeholder="请详细描述您遇到的问题或建议"
        :inputBorder="false"
        autoHeight
        maxlength="500"
      />
    </view>

    <!-- 联系方式 -->
    <view class="section">
      <text class="section-title">联系方式（选填）</text>
      <uni-easyinput 
        v-model="contact" 
        placeholder="请输入手机/邮箱"
        :inputBorder="false"
      />
    </view>

    <!-- 提交按钮 -->
    <button 
      class="submit-btn" 
      type="primary"
      @click="submitFeedback"
    >提交反馈</button>
  </view>
</template>

<script>
export default {
  data() {
    return {
      currentType: 0,
      types: ['功能建议', '问题反馈', '其他'],
      content: '',
      contact: ''
    }
  },
  methods: {
    onTypeChange(e) {
      this.currentType = e.currentIndex
    },
    submitFeedback() {
      // 提交逻辑
    }
  }
}
</script>

<style>
.feedback-container {
  padding: 30rpx;
}

.section {
  margin-bottom: 40rpx;
  background: #fff;
  border-radius: 12rpx;
  padding: 24rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
}

.section-title {
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
  display: block;
}

.submit-btn {
  margin-top: 60rpx;
  width: 90%;
  border-radius: 50rpx;
}
</style>