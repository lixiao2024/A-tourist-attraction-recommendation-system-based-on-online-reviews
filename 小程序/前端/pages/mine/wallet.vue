<template>
  <view class="content">
    <view class="wallet-container">
      <!-- 顶部背景 -->
      <view class="header-bg">
        <view class="wallet-title">我的钱包</view>
      </view>
      
      <!-- 余额卡片 -->
      <view class="balance-card">
        <view class="card-header">
          <text class="balance-label">当前余额</text>
          <view class="wallet-icon">
            <uni-icons type="wallet" size="24" color="#fff"></uni-icons>
          </view>
        </view>
        
        <text class="balance-amount">¥ 0.00</text>
        
        <view class="card-actions">
          <button class="action-btn recharge-btn" hover-class="btn-hover">
            <uni-icons type="plus" size="16" color="#fff"></uni-icons>
            <text>充值</text>
          </button>
          <button class="action-btn withdraw-btn" hover-class="btn-hover">
            <uni-icons type="download" size="16" color="#fff"></uni-icons>
            <text>提现</text>
          </button>
        </view>
        
        <view class="card-pattern"></view>
      </view>

      <!-- 快捷功能 -->
      <view class="quick-actions">
        <view class="quick-item" hover-class="quick-item-hover">
          <view class="quick-icon transfer-icon">
            <uni-icons type="paperplane" size="20" color="#fff"></uni-icons>
          </view>
          <text class="quick-text">转账</text>
        </view>
        <view class="quick-item" hover-class="quick-item-hover">
          <view class="quick-icon bill-icon">
            <uni-icons type="calendar" size="20" color="#fff"></uni-icons>
          </view>
          <text class="quick-text">账单</text>
        </view>
        <view class="quick-item" hover-class="quick-item-hover">
          <view class="quick-icon card-icon">
            <uni-icons type="card" size="20" color="#fff"></uni-icons>
          </view>
          <text class="quick-text">卡包</text>
        </view>
        <view class="quick-item" hover-class="quick-item-hover">
          <view class="quick-icon settings-icon">
            <uni-icons type="gear" size="20" color="#fff"></uni-icons>
          </view>
          <text class="quick-text">设置</text>
        </view>
      </view>

      <!-- 交易记录 -->
      <view class="transaction-section">
        <view class="section-header">
          <text class="section-title">交易记录</text>
          <view class="view-all" hover-class="text-hover">
            <text>查看全部</text>
            <uni-icons type="right" size="14" color="#999"></uni-icons>
          </view>
        </view>
        
        <view class="transaction-list">
          <view class="transaction-item" hover-class="item-hover">
            <view class="transaction-icon income-icon">
              <uni-icons type="arrow-down" size="18" color="#fff"></uni-icons>
            </view>
            <view class="transaction-info">
              <text class="transaction-title">充值</text>
              <text class="transaction-time">2023-07-20 14:30</text>
            </view>
            <text class="transaction-amount income">+100.00</text>
          </view>
          
          <view class="transaction-item" hover-class="item-hover">
            <view class="transaction-icon expense-icon">
              <uni-icons type="arrow-up" size="18" color="#fff"></uni-icons>
            </view>
            <view class="transaction-info">
              <text class="transaction-title">消费</text>
              <text class="transaction-time">2023-07-19 09:15</text>
            </view>
            <text class="transaction-amount expense">-20.00</text>
          </view>
          
          <view class="no-more">
            <text>暂无更多记录</text>
          </view>
        </view>
      </view>

      <!-- 安全提示 -->
      <view class="safety-tips">
        <view class="tip-icon">
          <uni-icons type="info" size="16" color="#fff"></uni-icons>
        </view>
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

<style lang="scss">
.content {
  background: #f8f9fa;
  min-height: 100vh;
}

.wallet-container {
  padding-bottom: 40rpx;
  position: relative;
}

.header-bg {
  background: linear-gradient(120deg, #3949AB, #1E88E5);
  height: 200rpx;
  border-bottom-left-radius: 40rpx;
  border-bottom-right-radius: 40rpx;
  padding: 40rpx 30rpx;
  position: relative;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.1);
}

.wallet-title {
  font-size: 36rpx;
  color: #fff;
  font-weight: 600;
}

.balance-card {
  background: linear-gradient(135deg, #6200EA, #3949AB);
  margin: -80rpx 30rpx 30rpx;
  border-radius: 24rpx;
  padding: 40rpx 30rpx;
  position: relative;
  overflow: hidden;
  box-shadow: 0 8rpx 30rpx rgba(0,0,0,0.15);
  z-index: 10;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.balance-label {
  font-size: 28rpx;
  color: rgba(255,255,255,0.8);
}

.wallet-icon {
  width: 60rpx;
  height: 60rpx;
  background: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.balance-amount {
  font-size: 64rpx;
  color: #ffffff;
  font-weight: bold;
  letter-spacing: 2rpx;
  margin: 20rpx 0;
  display: block;
}

.card-actions {
  display: flex;
  gap: 20rpx;
  margin-top: 40rpx;
}

.action-btn {
  flex: 1;
  height: 70rpx;
  border-radius: 35rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28rpx;
  border: none;
  gap: 8rpx;
  transition: all 0.3s ease;
}

.recharge-btn {
  background: rgba(255,255,255,0.25);
}

.withdraw-btn {
  background: rgba(255,255,255,0.15);
}

.btn-hover {
  transform: scale(0.96);
  opacity: 0.9;
}

.card-pattern {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 200rpx;
  height: 200rpx;
  background: radial-gradient(circle at center, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%);
  border-radius: 50%;
  transform: translate(50%, 50%);
  z-index: -1;
}

.quick-actions {
  display: flex;
  justify-content: space-between;
  padding: 20rpx 30rpx;
  margin-bottom: 30rpx;
}

.quick-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.3s ease;
}

.quick-item-hover {
  transform: translateY(-4rpx);
}

.quick-icon {
  width: 80rpx;
  height: 80rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12rpx;
}

.transfer-icon {
  background: linear-gradient(135deg, #FF9800, #FF5722);
}

.bill-icon {
  background: linear-gradient(135deg, #4CAF50, #009688);
}

.card-icon {
  background: linear-gradient(135deg, #9C27B0, #673AB7);
}

.settings-icon {
  background: linear-gradient(135deg, #607D8B, #455A64);
}

.quick-text {
  font-size: 24rpx;
  color: #666;
}

.transaction-section {
  background: #fff;
  border-radius: 24rpx;
  margin: 0 30rpx 30rpx;
  padding: 30rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30rpx;
}

.section-title {
  font-size: 32rpx;
  color: #333;
  font-weight: 600;
}

.view-all {
  display: flex;
  align-items: center;
  font-size: 24rpx;
  color: #999;
  gap: 4rpx;
}

.text-hover {
  color: #3949AB;
}

.transaction-list {
  
}

.transaction-item {
  display: flex;
  align-items: center;
  padding: 20rpx 0;
  border-bottom: 1px solid rgba(0,0,0,0.05);
}

.item-hover {
  background: rgba(0,0,0,0.02);
}

.transaction-icon {
  width: 60rpx;
  height: 60rpx;
  border-radius: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20rpx;
}

.income-icon {
  background: linear-gradient(135deg, #4CAF50, #009688);
}

.expense-icon {
  background: linear-gradient(135deg, #F44336, #E91E63);
}

.transaction-info {
  flex: 1;
}

.transaction-title {
  font-size: 28rpx;
  color: #333;
  display: block;
}

.transaction-time {
  font-size: 22rpx;
  color: #999;
}

.transaction-amount {
  font-size: 32rpx;
  font-weight: 500;
}

.income {
  color: #4CAF50;
}

.expense {
  color: #F44336;
}

.no-more {
  text-align: center;
  padding: 30rpx 0 10rpx;
  font-size: 26rpx;
  color: #999;
}

.safety-tips {
  margin: 20rpx 30rpx;
  display: flex;
  align-items: center;
  padding: 24rpx;
  background: rgba(255,255,255,0.8);
  border-radius: 16rpx;
  box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.05);
}

.tip-icon {
  width: 40rpx;
  height: 40rpx;
  background: #607D8B;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16rpx;
}

.tip-text {
  font-size: 24rpx;
  color: #666;
}
</style>