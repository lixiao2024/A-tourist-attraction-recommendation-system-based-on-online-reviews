<template>
	<view class="chat-container">
		<scroll-view class="message-list" scroll-y="true" :scroll-top="scrollTop">
			<view v-for="(message, index) in messages" :key="index" :class="['message-item', message.type]">
				<view class="avatar">
					<image :src="message.type === 'user' ? '/static/default-avatar.png' : '/static/tabs/assistant.png'" mode="aspectFill"></image>
				</view>
				<view class="message-content">
					<text>{{ message.content }}</text>
				</view>
			</view>
		</scroll-view>
		
		<view class="input-area">
			<input type="text" v-model="inputMessage" class="message-input" placeholder="请输入您的问题..." @confirm="sendMessage" />
			<button class="send-btn" @click="sendMessage">发送</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				messages: [
					{
						type: 'bot',
						content: '你好！我是你的智能助手，有什么可以帮你的吗？'
					}
				],
				inputMessage: '',
				scrollTop: 0
			}
		},
		methods: {
			sendMessage() {
				if (!this.inputMessage.trim()) return
				
				// 添加用户消息
				this.messages.push({
					type: 'user',
					content: this.inputMessage
				})
				
				// 模拟机器人回复
				setTimeout(() => {
					this.messages.push({
						type: 'bot',
						content: '这是一个模拟回复，后续将接入真实的AI模型。'
					})
					this.scrollToBottom()
				}, 500)
				
				this.inputMessage = ''
				this.scrollToBottom()
			},
			scrollToBottom() {
				setTimeout(() => {
					this.scrollTop = 9999999
				}, 100)
			}
		}
	}
</script>

<style>
	.chat-container {
		display: flex;
		flex-direction: column;
		height: 100vh;
		background-color: #f5f5f5;
	}
	
	.message-list {
		flex: 1;
		padding: 20rpx;
	}
	
	.message-item {
		display: flex;
		margin-bottom: 30rpx;
	}
	
	.message-item.user {
		flex-direction: row-reverse;
	}
	
	.avatar {
		width: 80rpx;
		height: 80rpx;
		margin: 0 20rpx;
	}
	
	.avatar image {
		width: 100%;
		height: 100%;
		border-radius: 50%;
	}
	
	.message-content {
		max-width: 60%;
		padding: 20rpx;
		border-radius: 10rpx;
		word-break: break-all;
	}
	
	.bot .message-content {
		background-color: #ffffff;
	}
	
	.user .message-content {
		background-color: #007AFF;
		color: #ffffff;
	}
	
	.input-area {
		display: flex;
		padding: 20rpx;
		background-color: #ffffff;
		border-top: 1rpx solid #e5e5e5;
	}
	
	.message-input {
		flex: 1;
		height: 80rpx;
		padding: 0 20rpx;
		border-radius: 40rpx;
		background-color: #f5f5f5;
		margin-right: 20rpx;
	}
	
	.send-btn {
		width: 120rpx;
		height: 80rpx;
		line-height: 80rpx;
		text-align: center;
		background-color: #007AFF;
		color: #ffffff;
		border-radius: 40rpx;
		font-size: 28rpx;
	}
</style>