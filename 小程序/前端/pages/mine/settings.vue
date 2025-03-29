<template>
  <view class="settings-container">
    <!-- 页面头部 -->
    <view class="header">
      <text class="page-title">设置</text>
    </view>
    
    <!-- 账号安全 -->
    <view class="settings-section">
      <text class="section-title">账号</text>
      <view class="setting-group">
        <view class="setting-item" hover-class="item-hover" @click="navigateTo('account')">
          <view class="item-left">
            <view class="icon-box security-icon">
              <uni-icons type="locked" size="20" color="#ffffff" />
            </view>
            <text class="item-title">账号与安全</text>
          </view>
          <uni-icons type="right" size="16" color="#c0c4cc" />
        </view>
      </view>
    </view>

    <!-- 通知设置 -->
    <view class="settings-section">
      <text class="section-title">通知</text>
      <view class="setting-group">
        <view class="setting-item">
          <view class="item-left">
            <view class="icon-box notification-icon">
              <uni-icons type="bell" size="20" color="#ffffff" />
            </view>
            <text class="item-title">消息通知</text>
          </view>
          <switch 
            :checked="notifyEnabled" 
            @change="toggleNotify" 
            color="#3182ce"
            class="custom-switch"
          />
        </view>
      </view>
    </view>

    <!-- 通用设置 -->
    <view class="settings-section">
      <text class="section-title">通用</text>
      <view class="setting-group">
        <view class="setting-item" hover-class="item-hover" @click="navigateTo('general')">
          <view class="item-left">
            <view class="icon-box general-icon">
              <uni-icons type="gear" size="20" color="#ffffff" />
            </view>
            <text class="item-title">通用设置</text>
          </view>
          <uni-icons type="right" size="16" color="#c0c4cc" />
        </view>
        
        <view class="setting-item" hover-class="item-hover" @click="navigateTo('privacy')">
          <view class="item-left">
            <view class="icon-box privacy-icon">
              <uni-icons type="eye" size="20" color="#ffffff" />
            </view>
            <text class="item-title">隐私设置</text>
          </view>
          <uni-icons type="right" size="16" color="#c0c4cc" />
        </view>
        
        <view class="setting-item" hover-class="item-hover" @click="navigateTo('language')">
          <view class="item-left">
            <view class="icon-box language-icon">
              <uni-icons type="paperplane" size="20" color="#ffffff" />
            </view>
            <text class="item-title">语言</text>
          </view>
          <view class="item-extra">
            <text class="extra-text">简体中文</text>
            <uni-icons type="right" size="16" color="#c0c4cc" />
          </view>
        </view>
      </view>
    </view>

    <!-- 关于我们 -->
    <view class="settings-section">
      <text class="section-title">关于</text>
      <view class="setting-group">
        <view class="setting-item" hover-class="item-hover" @click="navigateTo('about')">
          <view class="item-left">
            <view class="icon-box about-icon">
              <uni-icons type="info" size="20" color="#ffffff" />
            </view>
            <text class="item-title">关于我们</text>
          </view>
          <uni-icons type="right" size="16" color="#c0c4cc" />
        </view>
        
        <view class="setting-item" hover-class="item-hover" @click="checkUpdate">
          <view class="item-left">
            <view class="icon-box update-icon">
              <uni-icons type="reload" size="20" color="#ffffff" />
            </view>
            <text class="item-title">检查更新</text>
          </view>
          <view class="item-extra">
            <text class="version-text">v1.0.0</text>
            <uni-icons type="right" size="16" color="#c0c4cc" />
          </view>
        </view>
      </view>
    </view>

    <!-- 清除缓存 -->
    <view class="settings-section">
      <view class="setting-group">
        <view class="setting-item" hover-class="item-hover" @click="clearCache">
          <view class="item-left">
            <view class="icon-box cache-icon">
              <uni-icons type="trash" size="20" color="#ffffff" />
            </view>
            <text class="item-title">清除缓存</text>
          </view>
          <view class="item-extra">
            <text class="cache-size">23.5MB</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 退出登录 -->
    <view class="logout-section">
      <button class="logout-btn" hover-class="logout-hover" @click="handleLogout">
        退出登录
      </button>
    </view>
    
    <!-- 版本信息 -->
    <view class="footer">
      <image src="/static/logo.png" mode="aspectFit" class="logo-small"></image>
      <text class="copyright">© 2023-2024 旅游推荐 版权所有</text>
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
      this.notifyEnabled = e.detail.value
    },
    handleLogout() {
      uni.showModal({
        title: '提示',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            // 执行退出登录逻辑
            uni.showToast({
              title: '已退出登录',
              icon: 'success'
            })
            
            // 清除登录信息并返回
            uni.removeStorageSync('token')
            uni.removeStorageSync('userInfo')
            setTimeout(() => {
              uni.switchTab({
                url: '/pages/index/index'
              })
            }, 1500)
          }
        }
      })
    },
    navigateTo(type) {
      const routes = {
        'account': '/pages/mine/account',
        'privacy': '/pages/mine/privacy',
        'general': '/pages/mine/general',
        'about': '/pages/mine/about',
        'language': '/pages/mine/language'
      }
      
      if (routes[type]) {
        uni.navigateTo({
          url: routes[type]
        })
      } else {
        uni.showToast({
          title: '功能开发中',
          icon: 'none'
        })
      }
    },
    checkUpdate() {
      uni.showLoading({
        title: '检查更新中...'
      })
      
      setTimeout(() => {
        uni.hideLoading()
        uni.showToast({
          title: '已是最新版本',
          icon: 'success'
        })
      }, 1500)
    },
    clearCache() {
      uni.showModal({
        title: '提示',
        content: '确定要清除缓存吗？',
        success: (res) => {
          if (res.confirm) {
            uni.showLoading({
              title: '清除中...'
            })
            
            setTimeout(() => {
              uni.hideLoading()
              uni.showToast({
                title: '缓存已清除',
                icon: 'success'
              })
            }, 1500)
          }
        }
      })
    }
  }
}
</script>

<style lang="scss">
.settings-container {
  background: #f8f9fa;
  min-height: 100vh;
  padding-bottom: 40rpx;
}

.header {
  padding: 60rpx 40rpx 40rpx;
  
  .page-title {
    font-size: 48rpx;
    font-weight: 700;
    color: #222;
  }
}

.settings-section {
  margin-bottom: 40rpx;
  padding: 0 30rpx;
  
  .section-title {
    font-size: 24rpx;
    font-weight: 600;
    color: #718096;
    margin-bottom: 16rpx;
    padding-left: 20rpx;
    display: block;
  }
}

.setting-group {
  background: #ffffff;
  border-radius: 20rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04);
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 30rpx 20rpx;
  border-bottom: 1px solid rgba(0,0,0,0.03);
  transition: background-color 0.3s;
  
  &:last-child {
    border-bottom: none;
  }
}

.item-hover {
  background-color: rgba(0,0,0,0.02);
}

.item-left {
  display: flex;
  align-items: center;
}

.icon-box {
  width: 70rpx;
  height: 70rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
}

.security-icon {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.notification-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.general-icon {
  background: linear-gradient(135deg, #10b981, #059669);
}

.privacy-icon {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
}

.language-icon {
  background: linear-gradient(135deg, #ec4899, #db2777);
}

.about-icon {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.update-icon {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.cache-icon {
  background: linear-gradient(135deg, #9ca3af, #6b7280);
}

.item-title {
  font-size: 30rpx;
  color: #333;
  font-weight: 500;
}

.item-extra {
  display: flex;
  align-items: center;
}

.extra-text, .version-text, .cache-size {
  font-size: 26rpx;
  color: #999;
  margin-right: 10rpx;
}

.custom-switch {
  transform: scale(0.8);
  position: relative;
  right: -8rpx;
}

.logout-section {
  padding: 0 30rpx;
  margin: 60rpx 0;
}

.logout-btn {
  width: 100%;
  height: 90rpx;
  line-height: 90rpx;
  background: #fff;
  color: #f43f5e;
  font-size: 32rpx;
  font-weight: 500;
  border-radius: 20rpx;
  text-align: center;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.04);
  transition: all 0.3s;
  border: none;
}

.logout-hover {
  background: rgba(244, 63, 94, 0.05);
  transform: scale(0.98);
}

.footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40rpx 0;
  
  .logo-small {
    width: 80rpx;
    height: 80rpx;
    margin-bottom: 20rpx;
  }
  
  .copyright {
    font-size: 24rpx;
    color: #999;
  }
}
</style>