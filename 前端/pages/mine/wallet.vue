<template>
  <view class="content">
    <view class="wallet-container">
  <!-- 余额卡片 -->
  <view class="balance-card">
    <text class="balance-label">当前余额</text>
    <text class="balance-amount">¥ 0.00</text>
    <button class="recharge-btn" type="primary" size="mini">立即充值</button>
  </view>

  <!-- 交易记录 -->
  <view class="section-title">交易记录</view>
  <uni-list>
    <uni-list-item title="充值 +100.00" note="2023-07-20 14:30" showArrow></uni-list-item>
    <uni-list-item title="消费 -20.00" note="2023-07-19 09:15" showArrow></uni-list-item>
    <uni-list-item title="暂无更多记录" :showArrow="false"></uni-list-item>
  </uni-list>

  <!-- 安全提示 -->
  <view class="safety-tips">
    <uni-icons type="info" size="16" color="#999"></uni-icons>
    <text class="tip-text">资金由XX银行存管，保障安全</text>
  </view>
</view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
  }
}
</script>

<style>
.wallet-container {
  padding: 20rpx;
}

.balance-card {
  background: #fff;
  border-radius: 12rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
  text-align: center;
}

.balance-label {
  font-size: 28rpx;
  color: #666;
  display: block;
  margin-bottom: 10rpx;
}

.balance-amount {
  font-size: 48rpx;
  color: #007AFF;
  font-weight: bold;
  margin-bottom: 30rpx;
  display: block;
}

.recharge-btn {
  width: 200rpx;
  margin: 0 auto;
}

.section-title {
  font-size: 32rpx;
  color: #333;
  font-weight: 500;
  margin: 30rpx 0 20rpx 20rpx;
}

.safety-tips {
  margin-top: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20rpx;
  background: #f5f5f5;
  border-radius: 8rpx;
}

.tip-text {
  font-size: 24rpx;
  color: #999;
  margin-left: 10rpx;
}
</style>