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
        <view class="phone-section">
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
      </uni-forms-item>

      <uni-forms-item v-if="showVerifyCode" label="验证码" required>
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
      countdown: 60
    }
  },

  onLoad() {
    this.loadUserInfo();
  },

  methods: {
    loadUserInfo() {
      const userInfo = uni.getStorageSync('userInfo');
      if (userInfo) {
        this.avatarUrl = userInfo.avatar || this.avatarUrl;
        this.formData.nickName = userInfo.nickName || '';
        this.formData.phone = userInfo.phone || '';
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
        const result = await uniCloud.uploadFile({
          filePath: filePath,
          cloudPath: `avatars/${Date.now()}_${Math.random().toString(36).substr(2)}`
        });

        // 更新用户头像
        await this.updateUserInfo({ avatar: result.fileID });
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

    async sendSmsCode() {
      if (!/^1[3-9]\d{9}$/.test(this.formData.phone)) {
        uni.showToast({ title: '手机号格式错误', icon: 'none' });
        return;
      }

      try {
        const res = await uniCloud.callFunction({
          name: 'sendSmsCode',
          data: { phone: this.formData.phone }
        });

        if (res.result.code === 200) {
          this.startCountdown();
          this.showVerifyCode = true;
          uni.showToast({ title: '验证码已发送' });
        }
      } catch (error) {
        uni.showToast({ title: '发送失败', icon: 'error' });
      }
    },

    startCountdown() {
      this.canSendSms = false;
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
      if (!this.validateNickname()) return;

      try {
        const updateData = {
          nickName: this.formData.nickName,
          ...(this.formData.phone && { phone: this.formData.phone })
        };

        await this.updateUserInfo(updateData);
        uni.showToast({ title: '保存成功' });
        setTimeout(() => uni.navigateBack(), 1500);
      } catch (error) {
        uni.showToast({ title: '保存失败', icon: 'error' });
      }
    },

    async updateUserInfo(data) {
      const res = await uniCloud.callFunction({
        name: 'updateUserInfo',
        data: {
          userId: uni.getStorageSync('userInfo')._id,
          updateData: data
        }
      });

      if (res.result.code === 200) {
        const newUserInfo = { ...uni.getStorageSync('userInfo'), ...data };
        uni.setStorageSync('userInfo', newUserInfo);
      }
    },

    navigateToRealnameAuth() {
      uni.navigateTo({ url: '/pages/mine/realnameAuth' });
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
}
</style>