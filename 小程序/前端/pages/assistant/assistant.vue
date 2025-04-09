<template>
	<view class="chat-container">
		<!-- 顶部导航栏 -->
		<view class="chat-header">
			<view class="avatar-container">
				<image class="assistant-avatar" src="/static/tabs/assistant.png" mode="aspectFill"></image>
				<view class="status-indicator"></view>
			</view>
			<view class="header-info">
				<text class="assistant-name">智能旅行助手</text>
				<text class="assistant-status">在线 · AI 驱动</text>
			</view>
		</view>
		
		<!-- 消息列表 -->
		<scroll-view 
			class="message-list" 
			scroll-y="true" 
			:scroll-top="scrollTop"
			:scroll-with-animation="true"
			:show-scrollbar="false"
			@scrolltoupper="loadMoreMessages"
			refresher-enabled
			:refresher-triggered="isRefreshing"
			@refresherrefresh="onRefresh"
		>
			<view class="chat-date">
				<text>{{ currentDate }}</text>
			</view>
			
			<view 
				v-for="(message, index) in messages" 
				:key="index" 
				:class="['message-item', `message-${message.type}`]"
				:animation="messageAnimation"
			>
				<view class="avatar">
					<image 
						:src="message.type === 'user' ? '/static/default-avatar.png' : '/static/tabs/assistant.png'" 
						mode="aspectFill"
					></image>
				</view>
				<view class="message-container">
					<view class="message-bubble">
						<rich-text v-if="message.type === 'bot' && message.content.includes('```')" 
							:nodes="formatMarkdown(message.content)" 
							class="code-message"
						></rich-text>
						<text v-else selectable class="message-text">{{ message.content }}</text>
					</view>
					<text class="message-time">{{ message.time || '刚刚' }}</text>
				</view>
			</view>
			
			<!-- 正在输入提示 -->
			<view class="typing-indicator" v-if="isTyping">
				<view class="avatar">
					<image src="/static/tabs/assistant.png" mode="aspectFill"></image>
				</view>
				<view class="message-container">
					<view class="message-bubble typing-bubble">
						<view class="typing-dots">
							<view class="typing-dot"></view>
							<view class="typing-dot"></view>
							<view class="typing-dot"></view>
						</view>
					</view>
				</view>
			</view>
		</scroll-view>
		
		<!-- 输入区域 -->
		<view class="input-area">
			<!-- 快捷问题 -->
			<scroll-view scroll-x class="quick-questions" v-if="showQuickQuestions">
				<view 
					v-for="(question, index) in quickQuestions" 
					:key="index"
					class="question-tag"
					hover-class="question-tag-hover"
					@click="quickSend(question)"
				>
					{{ question }}
				</view>
			</scroll-view>
			
			<view class="input-container">
				<view class="input-wrapper">
					<uni-icons type="sound-filled" size="24" color="#666" class="input-icon"></uni-icons>
					<input 
						type="text" 
						v-model="inputMessage" 
						class="message-input" 
						placeholder="输入您的问题..." 
						cursor-spacing="20"
						confirm-type="send"
						@confirm="sendMessage" 
					/>
					<uni-icons 
						:type="inputMessage.trim() ? 'paperplane-filled' : 'image-filled'" 
						size="24" 
						:color="inputMessage.trim() ? '#3182ce' : '#666'" 
						class="input-icon send-icon"
						@click="inputMessage.trim() ? sendMessage() : uploadImage()"
					></uni-icons>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
import { updateUserInterests } from '@/request/api.js';
import request from '@/request/request.js';

// 修改请求配置
request.defaults.baseURL = 'http://192.168.1.10:8001';

export default {
	data() {
		return {
			messages: [
				{
					type: 'bot',
					content: '👋 你好！我是你的智能旅行助手，可以为你提供旅游景点推荐、路线规划、旅行攻略等服务。有什么可以帮你的吗？',
					time: this.formatTime(new Date())
				}
			],
			inputMessage: '',
			scrollTop: 0,
			isTyping: false,
			messageAnimation: {},
			isRefreshing: false,
			showQuickQuestions: true,
			quickQuestions: [
				'推荐热门景点',
				'附近有什么好玩的地方',
				'预算3000元三日游攻略',
				'适合拍照的景点'
			],
			currentDate: this.formatDate(new Date()),
			chatHistory: [] // 添加对话历史记录
		}
	},
	mounted() {
		this.scrollToBottom();
	},
	methods: {
		async sendMessage() {
			if (!this.inputMessage.trim()) return;
			
			// 添加用户消息
			const userMessage = {
				type: 'user',
				content: this.inputMessage,
				time: this.formatTime(new Date())
			};
			this.messages.push(userMessage);
			
			// 保存用户问题
			const userQuestion = this.inputMessage;
			this.inputMessage = '';
			this.scrollToBottom();
			
			// 显示输入动画
			this.isTyping = true;
			
			try {
				// 调用Qwen API
				const response = await request({
					url: 'http://192.168.1.10:8001/api/qwen-chat',
					method: 'POST',
					data: {
						question: userQuestion,
						history: this.chatHistory
					},
					timeout: 60000, // 增加超时时间为60秒
					hideLoading: false // 显示加载中提示
				});
				
				// 更新对话历史
				this.chatHistory = response.history;
				
				// 添加机器人回复
				this.messages.push({
					type: 'bot',
					content: response.response,
					time: this.formatTime(new Date())
				});
				
				this.scrollToBottom();
			} catch (error) {
				console.error('与AI助手交互时出错:', error);
				// 添加错误提示消息
				this.messages.push({
					type: 'bot',
					content: '抱歉，我暂时无法回答您的问题。' + (error.message ? `\n错误信息：${error.message}` : '请稍后再试。'),
					time: this.formatTime(new Date())
				});
				
				// 显示错误提示
				uni.showToast({
					title: '请求失败，请检查网络连接',
					icon: 'none',
					duration: 2000
				});
			} finally {
				this.isTyping = false;
			}
		},
		
		quickSend(question) {
			this.inputMessage = question;
			this.sendMessage();
		},
		
		scrollToBottom() {
			setTimeout(() => {
				this.scrollTop = 999999;
			}, 100);
		},
		
		formatTime(date) {
			const hours = date.getHours().toString().padStart(2, '0');
			const minutes = date.getMinutes().toString().padStart(2, '0');
			return `${hours}:${minutes}`;
		},
		
		formatDate(date) {
			const year = date.getFullYear();
			const month = (date.getMonth() + 1).toString().padStart(2, '0');
			const day = date.getDate().toString().padStart(2, '0');
			return `${year}年${month}月${day}日`;
		},
		
		loadMoreMessages() {
			// 加载更多历史消息的功能
			console.log('加载更多历史消息');
		},
		
		onRefresh(e) {
			this.isRefreshing = true;
			
			// 模拟加载过程
			setTimeout(() => {
				this.isRefreshing = false;
				uni.showToast({
					title: '已刷新',
					icon: 'none'
				});
			}, 1000);
		},
		
		uploadImage() {
			uni.chooseImage({
				count: 1,
				success: (res) => {
					uni.showToast({
						title: '图片功能开发中',
						icon: 'none'
					});
				}
			});
		},
		
		formatMarkdown(content) {
			// 简单处理代码块
			let html = content;
			
			// 处理代码块
			html = html.replace(/```([^`]+)```/g, '<div class="code-block">$1</div>');
			
			// 处理粗体
			html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
			
			// 处理斜体
			html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
			
			return html;
		},
		
		generateResponse(question) {
			// 模拟智能回复
			const responses = {
				'推荐热门景点': '根据最近数据，以下景点最受欢迎：\n\n1. **西湖** - 杭州标志性景点，周边有雷峰塔、三潭印月等著名景点\n2. **故宫** - 中国明清两代的皇家宫殿，世界上现存规模最大的古代宫殿建筑群\n3. **黄山** - 以奇松、怪石、云海、温泉"四绝"闻名于世\n4. **张家界** - 独特的砂岩峰林地貌，《阿凡达》电影取景地\n5. **鼓浪屿** - 厦门著名景点，有"钢琴之岛"、"万国建筑博览"之称\n\n需要了解更多关于某个景点的详细信息吗？',
				'附近有什么好玩的地方': '要推荐附近的景点，我需要知道您当前的位置。您可以：\n\n1. 点击下方"分享位置"按钮\n2. 或直接告诉我您所在的城市/地区\n\n这样我才能为您提供更准确的周边景点推荐。',
				'预算3000元三日游攻略': '使用3000元预算的三日游，以下是我的建议：\n\n**Day 1:**\n- 上午：参观市区主要景点（门票约100元）\n- 中午：当地特色午餐（约50元）\n- 下午：市区次要景点（门票约80元）\n- 晚上：夜景游览（免费）\n\n**Day 2:**\n- 全天：周边自然风景区一日游（280元含交通）\n\n**Day 3:**\n- 上午：特色文化体验（约150元）\n- 下午：购物/自由活动\n\n**住宿**：经济型酒店双床房（约250元/晚 × 3晚 = 750元）\n**餐饮**：人均80元/天 × 3天 = 720元\n**交通**：市内交通约100元/天 × 3天 = 300元\n**其他**：约200元\n\n**总计**：约2630元，预留370元应急资金\n\n如需特定城市的具体攻略，请告诉我您计划去哪里旅游。',
				'适合拍照的景点': '以下是几个特别适合拍照的景点推荐：\n\n1. **乌镇/周庄** - 水乡古镇，小桥流水人家的风景非常上镜\n2. **鹤龙湖** - 落日余晖下的湖景非常适合拍摄剪影\n3. **莫干山** - 山间民宿和竹林景观是拍照的绝佳背景\n4. **东极岛** - 海岛日出和星空摄影胜地\n5. **茶卡盐湖** - 被称为"天空之镜"，拍照效果震撼\n\n拍摄建议时间：清晨或傍晚的黄金光线时段。您有偏好的拍摄风格吗？'
			};
			
			// 检查是否有预设回答
			for (const key in responses) {
				if (question.includes(key)) {
					return responses[key];
				}
			}
			
			// 默认回复
			return '感谢您的提问！这是一个模拟回复，目前我正在学习中。您可以尝试点击下方的快捷问题，或者询问关于旅游景点、路线规划、旅行攻略等问题，我会尽力为您提供帮助。';
		}
	}
}
</script>

<style lang="scss">
	.chat-container {
		display: flex;
		flex-direction: column;
		height: 100vh;
		background-color: #f8f9fa;
		position: relative;
	}
	
	.chat-header {
		display: flex;
		align-items: center;
		padding: 30rpx;
		background: linear-gradient(135deg, #3182ce, #005bb5);
		box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
		border-bottom-left-radius: 20rpx;
		border-bottom-right-radius: 20rpx;
		
		.avatar-container {
			position: relative;
			margin-right: 24rpx;
			
			.assistant-avatar {
				width: 90rpx;
				height: 90rpx;
				border-radius: 50%;
				border: 3rpx solid rgba(255,255,255,0.7);
			}
			
			.status-indicator {
				position: absolute;
				bottom: 2rpx;
				right: 2rpx;
				width: 18rpx;
				height: 18rpx;
				border-radius: 50%;
				background-color: #10b981;
				border: 3rpx solid #ffffff;
			}
		}
		
		.header-info {
			display: flex;
			flex-direction: column;
			
			.assistant-name {
				font-size: 36rpx;
				font-weight: 600;
				color: #ffffff;
				margin-bottom: 4rpx;
			}
			
			.assistant-status {
				font-size: 24rpx;
				color: rgba(255,255,255,0.8);
			}
		}
	}
	
	.chat-date {
		text-align: center;
		margin: 20rpx 0;
		
		text {
			display: inline-block;
			padding: 8rpx 20rpx;
			background-color: rgba(0,0,0,0.06);
			color: #666;
			font-size: 24rpx;
			border-radius: 30rpx;
		}
	}
	
	.message-list {
		flex: 1;
		padding: 20rpx 30rpx;
	}
	
	.message-item {
		display: flex;
		margin-bottom: 40rpx;
		animation: fadeIn 0.3s ease;
	}
	
	.message-item.message-user {
		flex-direction: row-reverse;
		
		.message-container {
			align-items: flex-end;
		}
		
		.message-bubble {
			background: linear-gradient(135deg, #3182ce, #0056b3);
			color: #ffffff;
			border-radius: 20rpx 4rpx 20rpx 20rpx;
		}
		
		.message-time {
			margin-right: 24rpx;
		}
	}
	
	.message-item.message-bot {
		.message-bubble {
			background-color: #ffffff;
			color: #333;
			border-radius: 4rpx 20rpx 20rpx 20rpx;
			box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.06);
		}
		
		.message-time {
			margin-left: 24rpx;
		}
	}
	
	@keyframes fadeIn {
		from { opacity: 0; transform: translateY(10rpx); }
		to { opacity: 1; transform: translateY(0); }
	}
	
	.avatar {
		width: 84rpx;
		height: 84rpx;
		flex-shrink: 0;
		
		image {
			width: 100%;
			height: 100%;
			border-radius: 50%;
			box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.1);
		}
	}
	
	.message-container {
		display: flex;
		flex-direction: column;
		max-width: calc(100% - 200rpx);
		margin: 0 20rpx;
	}
	
	.message-bubble {
		padding: 20rpx 24rpx;
		border-radius: 20rpx;
		word-break: break-word;
		position: relative;
		line-height: 1.6;
	}
	
	.message-text {
		font-size: 32rpx;
		line-height: 1.5;
	}
	
	.code-message {
		font-size: 30rpx;
		line-height: 1.5;
		
		.code-block {
			background-color: #f1f1f1;
			padding: 16rpx;
			border-radius: 8rpx;
			font-family: monospace;
			margin: 10rpx 0;
			white-space: pre-wrap;
			overflow-x: auto;
		}
	}
	
	.message-time {
		font-size: 22rpx;
		color: #999;
		margin-top: 10rpx;
	}
	
	.typing-indicator {
		display: flex;
		margin-bottom: 40rpx;
	}
	
	.typing-bubble {
		min-width: 70rpx;
		min-height: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	
	.typing-dots {
		display: flex;
		align-items: center;
	}
	
	.typing-dot {
		width: 12rpx;
		height: 12rpx;
		border-radius: 50%;
		background-color: #aaa;
		margin: 0 6rpx;
		animation: typingBounce 1.4s infinite ease-in-out;
		
		&:nth-child(1) {
			animation-delay: 0s;
		}
		
		&:nth-child(2) {
			animation-delay: 0.2s;
		}
		
		&:nth-child(3) {
			animation-delay: 0.4s;
		}
	}
	
	@keyframes typingBounce {
		0%, 60%, 100% {
			transform: translateY(0);
		}
		30% {
			transform: translateY(-6rpx);
		}
	}
	
	.input-area {
		padding: 20rpx;
		background-color: #ffffff;
		border-top: 1rpx solid rgba(0,0,0,0.05);
		display: flex;
		flex-direction: column;
	}
	
	.quick-questions {
		width: 100%;
		white-space: nowrap;
		margin-bottom: 20rpx;
		
		.question-tag {
			display: inline-block;
			padding: 12rpx 24rpx;
			margin-right: 20rpx;
			background-color: #f0f4f8;
			color: #3182ce;
			border-radius: 40rpx;
			font-size: 28rpx;
			transition: all 0.3s;
		}
		
		.question-tag-hover {
			background-color: #e1e8f0;
			transform: scale(0.98);
		}
	}
	
	.input-container {
		display: flex;
		align-items: center;
	}
	
	.input-wrapper {
		display: flex;
		align-items: center;
		background-color: #f0f4f8;
		border-radius: 40rpx;
		flex: 1;
		padding: 0 20rpx;
	}
	
	.input-icon {
		padding: 0 15rpx;
	}
	
	.message-input {
		flex: 1;
		height: 80rpx;
		font-size: 30rpx;
		padding: 0 10rpx;
	}
	
	.send-icon {
		transition: all 0.3s;
		
		&:active {
			transform: scale(0.9);
		}
	}
</style>