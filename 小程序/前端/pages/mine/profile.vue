<template>
  <view class="profile-container">
    <!-- 头像上传区域 -->
    <view class="avatar-section">
      <uni-file-picker
        v-model="avatar"
        fileMediatype="image"
        mode="grid"
        :auto-upload="false"
        @select="onSelectAvatar"
        title="点击修改头像"
      >
        <image :src="avatarUrl" class="user-avatar" mode="aspectFill" />
      </uni-file-picker>
    </view>

    <!-- 个人信息表单 -->
    <uni-forms :modelValue="formData" labelWidth="80px">
      <uni-forms-item label="昵称" required>
        <uni-easyinput
          v-model="formData.nickName"
          placeholder="请输入昵称"
          :inputBorder="false"
          @blur="validateNickname"
        />
      </uni-forms-item>

      <uni-forms-item label="手机号">
        <view class="phone-section" v-if="!isPhoneBound">
          <uni-easyinput
            v-model="formData.phone"
            placeholder="请输入手机号"
            :inputBorder="false"
            type="number"
          />
          <button
            class="verify-btn"
            :disabled="!canSendSms"
            @click="sendSmsCode"
          >
            {{ smsBtnText }}
          </button>
        </view>
        <view class="bound-phone" v-else>
          <text class="phone-text">{{ maskedPhone }}</text>
          <button class="change-btn" @click="changePhone">更换手机号</button>
        </view>
      </uni-forms-item>

      <uni-forms-item label="验证码" required v-if="!isPhoneBound && showVerifyCode">
        <uni-easyinput
          v-model="formData.verifyCode"
          placeholder="请输入验证码"
          :inputBorder="false"
          type="number"
        />
      </uni-forms-item>

      <uni-forms-item label="实名认证">
        <button class="auth-btn" @click="navigateToRealnameAuth">
          立即认证
        </button>
      </uni-forms-item>
    </uni-forms>

    <!-- 操作按钮 -->
    <button class="save-btn" @click="submitForm">保存修改</button>
  </view>
</template>

<script>
import { sendVerificationCode, verifyAndBindPhone } from '@/request/api.js'

export default {
  data() {
    return {
      avatarUrl: '/static/default-avatar.png',
      formData: {
        nickName: '',
        phone: '',
        verifyCode: ''
      },
      smsBtnText: '获取验证码',
      canSendSms: true,
      showVerifyCode: false,
      countdown: 60,
      isPhoneBound: false,
      maskedPhone: ''
    }
  },

  onLoad() {
    this.loadUserInfo();
  },

  methods: {
    loadUserInfo() {
      const userInfo = uni.getStorageSync('userInfo');
      if (userInfo) {
        this.avatarUrl = userInfo.avatar || userInfo.avatarUrl || this.avatarUrl;
        this.formData.nickName = userInfo.nickname || userInfo.nickName || '';
        this.formData.phone = userInfo.phone || '';
        this.isPhoneBound = !!userInfo.phone;
        this.maskedPhone = this.maskPhone(userInfo.phone);
      }
    },

    onSelectAvatar(e) {
      const tempFilePaths = e.tempFilePaths;
      this.avatarUrl = tempFilePaths[0];
      this.uploadAvatar(tempFilePaths[0]);
    },

    async uploadAvatar(filePath) {
      uni.showLoading({ title: '上传中...' });
      try {
        // 调用API上传头像
        // 注意：这里需要调用实际的API来上传头像
        
        uni.hideLoading();
        uni.showToast({ title: '头像更新成功' });
      } catch (error) {
        uni.hideLoading();
        uni.showToast({ title: '上传失败', icon: 'error' });
      }
    },

    validateNickname() {
      if (!this.formData.nickName.trim()) {
        uni.showToast({ title: '昵称不能为空', icon: 'none' });
        return false;
      }
      if (this.formData.nickName.length > 12) {
        uni.showToast({ title: '昵称不能超过12个字', icon: 'none' });
        return false;
      }
      return true;
    },

    validatePhone() {
      if (!/^1[3-9]\d{9}$/.test(this.formData.phone)) {
        uni.showToast({ title: '手机号格式错误', icon: 'none' });
        return false;
      }
      return true;
    },

    async sendSmsCode() {
      // 验证手机号
      if (!this.validatePhone()) return;

      try {
        uni.showLoading({ title: '发送中...' });
        
        // 调用发送验证码API
        const res = await sendVerificationCode(this.formData.phone);
        
        uni.hideLoading();
        
        if (res.success) {
          this.startCountdown();
          this.showVerifyCode = true;
          uni.showToast({ title: res.message || '验证码已发送' });
        } else {
          uni.showToast({ 
            title: res.message || '发送验证码失败', 
            icon: 'none' 
          });
        }
      } catch (error) {
        uni.hideLoading();
        console.error('发送验证码失败:', error);
        
        // 处理超时但可能已发送的情况
        if (error.message && error.message.includes('timeout')) {
          uni.showModal({
            title: '提示',
            content: '网络请求超时，但验证码可能已发送。请查看手机短信，如收到验证码可继续操作。',
            confirmText: '我已收到',
            cancelText: '重新发送',
            success: (res) => {
              if (res.confirm) {
                // 用户确认已收到，启动倒计时并显示验证码输入框
                this.startCountdown();
                this.showVerifyCode = true;
              } else if (res.cancel) {
                // 用户选择重新发送，不做任何处理，用户可以再次点击发送按钮
                console.log('用户选择重新发送验证码');
              }
            }
          });
        } else {
          uni.showToast({ 
            title: error.message || '发送验证码失败', 
            icon: 'none' 
          });
        }
      }
    },

    startCountdown() {
      this.canSendSms = false;
      this.countdown = 60;
      
      const timer = setInterval(() => {
        if (this.countdown <= 0) {
          clearInterval(timer);
          this.smsBtnText = '重新发送';
          this.canSendSms = true;
          this.countdown = 60;
          return;
        }
        this.countdown--;
        this.smsBtnText = `${this.countdown}s后重发`;
      }, 1000);
    },

    async submitForm() {
      // 验证昵称
      if (!this.validateNickname()) return;
      
      // 如果填写了手机号和验证码，则进行验证并绑定
      if (this.formData.phone && this.formData.verifyCode && !this.isPhoneBound) {
        if (!this.validatePhone()) return;
        
        // 验证码格式验证
        if (!/^\d{6}$/.test(this.formData.verifyCode)) {
          uni.showToast({ title: '验证码必须是6位数字', icon: 'none' });
          return;
        }
        
        try {
          uni.showLoading({ title: '提交中...' });
          
          // 打印请求信息，方便调试
          console.log('准备提交验证请求：', {
            phone: this.formData.phone,
            code: this.formData.verifyCode
          });
          
          // 调用验证并绑定API
          const res = await verifyAndBindPhone(this.formData.phone, this.formData.verifyCode);
          
          uni.hideLoading();
          console.log('验证响应结果：', res);
          
          if (!res.success) {
            // 验证失败，显示更多错误信息帮助调试
            const errorMsg = res.message || '验证码错误或已过期';
            console.error('验证失败：', errorMsg);
            
            uni.showToast({ 
              title: errorMsg, 
              icon: 'none',
              duration: 3000
            });
            return;
          }
          
          // 手机绑定成功，更新本地存储和UI状态
          const userInfo = uni.getStorageSync('userInfo') || {};
          userInfo.phone = this.formData.phone;
          uni.setStorageSync('userInfo', userInfo);
          
          // 更新UI状态
          this.isPhoneBound = true;
          this.maskedPhone = this.maskPhone(this.formData.phone);
          this.showVerifyCode = false;
          
          uni.showToast({ title: '手机号绑定成功' });
        } catch (error) {
          uni.hideLoading();
          console.error('绑定手机号失败详情:', error);
          
          // 显示更详细的错误信息
          let errorMsg = '';
          if (typeof error === 'object') {
            errorMsg = error.message || (error.data ? JSON.stringify(error.data) : '未知错误');
          } else {
            errorMsg = String(error);
          }
          
          uni.showToast({ 
            title: errorMsg.substring(0, 100), // 限制长度
            icon: 'none',
            duration: 3000
          });
          return;
        }
      }
      
      // 更新其他信息
      try {
        // 更新昵称等其他信息
        const userInfo = uni.getStorageSync('userInfo') || {};
        userInfo.nickname = this.formData.nickName;
        userInfo.nickName = this.formData.nickName;
        uni.setStorageSync('userInfo', userInfo);
        
        uni.showToast({ title: '保存成功' });
        setTimeout(() => uni.navigateBack(), 1500);
      } catch (error) {
        console.error('保存失败:', error);
        uni.showToast({ title: '保存失败', icon: 'none' });
      }
    },

    navigateToRealnameAuth() {
      uni.navigateTo({ url: '/pages/mine/realnameAuth' });
    },

    maskPhone(phone) {
      if (!phone) return '';
      const masked = phone.slice(0, 3) + '****' + phone.slice(-4);
      return masked;
    },

    changePhone() {
      this.isPhoneBound = false;
      this.showVerifyCode = false;
      this.formData.phone = '';
      this.formData.verifyCode = '';
    }
  }
}
</script>

<style lang="scss">
.profile-container {
  padding: 20rpx 30rpx;

  .avatar-section {
    display: flex;
    justify-content: center;
    margin: 40rpx 0;

    .user-avatar {
      width: 160rpx;
      height: 160rpx;
      border-radius: 50%;
      border: 2rpx solid #eee;
    }
  }

  .phone-section {
    display: flex;
    align-items: center;

    .verify-btn {
      margin-left: 20rpx;
      padding: 0 30rpx;
      height: 60rpx;
      line-height: 60rpx;
      font-size: 26rpx;
      background: #007AFF;
      color: #fff;
      border-radius: 30rpx;

      &[disabled] {
        background: #ccc;
      }
    }
  }

  .auth-btn {
    width: 200rpx;
    height: 60rpx;
    line-height: 60rpx;
    font-size: 26rpx;
    background: #007AFF;
    color: #fff;
    border-radius: 30rpx;
  }

  .save-btn {
    margin-top: 60rpx;
    background: #007AFF;
    color: #fff;
    border-radius: 50rpx;
    height: 80rpx;
    line-height: 80rpx;
  }

  .bound-phone {
    display: flex;
    align-items: center;

    .phone-text {
      margin-right: 20rpx;
    }

    .change-btn {
      padding: 0 30rpx;
      height: 60rpx;
      line-height: 60rpx;
      font-size: 26rpx;
      background: #007AFF;
      color: #fff;
      border-radius: 30rpx;
    }
  }
}
</style>