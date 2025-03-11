<template>
  <view class="settings-container">
    <!-- 账号安全 -->
    <uni-list class="setting-group">
      <uni-list-item title="账号与安全" showArrow>
        <uni-icons type="locked" size="20" color="#666" slot="left"/>
      </uni-list-item>
    </uni-list>

    <!-- 通知设置 -->
    <uni-list class="setting-group">
      <uni-list-item 
        title="消息通知"
        showSwitch
        :switchChecked="notifyEnabled"
        @switchChange="toggleNotify"
      >
        <uni-icons type="bell" size="20" color="#666" slot="left"/>
      </uni-list-item>
    </uni-list>

    <!-- 通用设置 -->
    <uni-list class="setting-group">
      <uni-list-item title="通用设置" showArrow>
        <uni-icons type="gear" size="20" color="#666" slot="left"/>
      </uni-list-item>
      <uni-list-item title="隐私设置" showArrow>
        <uni-icons type="eye" size="20" color="#666" slot="left"/>
      </uni-list-item>
    </uni-list>

    <!-- 关于我们 -->
    <uni-list class="setting-group">
      <uni-list-item title="关于我们" showArrow>
        <uni-icons type="info" size="20" color="#666" slot="left"/>
      </uni-list-item>
      <uni-list-item title="检查更新" showArrow>
        <uni-icons type="reload" size="20" color="#666" slot="left"/>
      </uni-list-item>
    </uni-list>

    <!-- 退出登录 -->
    <view class="logout-btn" @click="handleLogout">
      <text class="logout-text">退出登录</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      notifyEnabled: true
    }
  },
  methods: {
    toggleNotify(e) {
      this.notifyEnabled = e.value
    },
    handleLogout() {
      uni.showModal({
        title: '提示',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            // 执行退出登录逻辑
          }
        }
      })
    }
  }
}
</script>

<style>
.settings-container {
  padding: 30rpx;
}


  .setting-group {
    margin-bottom: 30rpx;
    border-radius: 12rpx;
    overflow: hidden;
    box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
  }

  .logout-btn {
    margin-top: 60rpx;
    background: #fff;
    padding: 24rpx;
    text-align: center;
    border-radius: 12rpx;
    box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
}
    .logout-text {
      color: #FF4444;
      font-size: 32rpx;
      font-weight: 500;
    }
  

</style>