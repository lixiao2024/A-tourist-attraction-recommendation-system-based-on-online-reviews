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
			<!-- 添加清空记录按钮 -->
			<view class="header-actions">
				<view class="clear-btn" @click="clearChatHistory">
					<uni-icons type="trash" size="20" color="#ffffff"></uni-icons>
				</view>
			</view>
		</view>
		
		<!-- 消息列表区域(固定高度，可滚动) -->
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
						<rich-text v-if="message.type === 'bot'" 
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
			
			<!-- 底部留白区域，避免消息被输入框遮挡 -->
			<view class="bottom-space"></view>
		</scroll-view>
		
		<!-- 输入区域(固定在底部) -->
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

// 简单的缓存机制，保存常见问题的回答
const RESPONSE_CACHE = {
	'推荐热门景点': '根据最近数据，以下景点最受欢迎：\n\n1. **西湖** - 杭州标志性景点，周边有雷峰塔、三潭印月等著名景点\n2. **故宫** - 中国明清两代的皇家宫殿，世界上现存规模最大的古代宫殿建筑群\n3. **黄山** - 以奇松、怪石、云海、温泉"四绝"闻名于世\n4. **张家界** - 独特的砂岩峰林地貌，《阿凡达》电影取景地\n5. **鼓浪屿** - 厦门著名景点，有"钢琴之岛"、"万国建筑博览"之称\n\n需要了解更多关于某个景点的详细信息吗？',
	'附近有什么好玩的地方': '要推荐附近的景点，我需要知道您当前的位置。您可以：\n\n1. 直接告诉我您所在的城市/地区\n2. 或分享您感兴趣的目的地\n\n这样我才能为您提供更准确的周边景点推荐。',
	'预算3000元三日游攻略': '使用3000元预算的三日游，以下是我的建议：\n\n**Day 1:**\n- 上午：参观市区主要景点（门票约100元）\n- 中午：当地特色午餐（约50元）\n- 下午：市区次要景点（门票约80元）\n- 晚上：夜景游览（免费）\n\n**Day 2:**\n- 全天：周边自然风景区一日游（280元含交通）\n\n**Day 3:**\n- 上午：特色文化体验（约150元）\n- 下午：购物/自由活动\n\n**住宿**：经济型酒店双床房（约250元/晚 × 3晚 = 750元）\n**餐饮**：人均80元/天 × 3天 = 720元\n**交通**：市内交通约100元/天 × 3天 = 300元\n**其他**：约200元\n\n**总计**：约2630元，预留370元应急资金\n\n如需特定城市的具体攻略，请告诉我您计划去哪里旅游。',
	'适合拍照的景点': '以下是几个特别适合拍照的景点推荐：\n\n1. **乌镇/周庄** - 水乡古镇，小桥流水人家的风景非常上镜\n2. **鹤龙湖** - 落日余晖下的湖景非常适合拍摄剪影\n3. **莫干山** - 山间民宿和竹林景观是拍照的绝佳背景\n4. **东极岛** - 海岛日出和星空摄影胜地\n5. **茶卡盐湖** - 被称为"天空之镜"，拍照效果震撼\n\n拍摄建议时间：清晨或傍晚的黄金光线时段。您有偏好的拍摄风格吗？'
};

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
			chatHistory: [], // 添加对话历史记录
			sessionId: null, // 添加会话ID
			isRetrying: false, // 添加重试标志
			maxRetries: 2, // 最大重试次数
			retryCount: 0 // 当前重试次数
		}
	},
	mounted() {
		this.loadChatHistory();
		this.scrollToBottom();
	},
	methods: {
		// 加载本地缓存的聊天记录
		loadChatHistory() {
			try {
				const savedMessages = uni.getStorageSync('assistant_messages');
				const savedSessionId = uni.getStorageSync('assistant_session_id');
				
				if (savedMessages) {
					this.messages = JSON.parse(savedMessages);
				}
				
				if (savedSessionId) {
					this.sessionId = savedSessionId;
				}
				
				console.log('从缓存加载聊天记录:', this.messages.length, '条消息');
			} catch (e) {
				console.error('加载聊天记录失败:', e);
			}
		},
		
		// 保存聊天记录到本地
		saveChatHistory() {
			try {
				uni.setStorageSync('assistant_messages', JSON.stringify(this.messages));
				if (this.sessionId) {
					uni.setStorageSync('assistant_session_id', this.sessionId);
				}
				console.log('聊天记录已保存至本地缓存');
			} catch (e) {
				console.error('保存聊天记录失败:', e);
			}
		},
		
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
			
			// 保存聊天记录到本地
			this.saveChatHistory();
			
			// 显示输入动画
			this.isTyping = true;
			
			// 重置重试计数
			this.retryCount = 0;
			
			// 检查常见问题缓存
			const cachedResponse = this.checkResponseCache(userQuestion);
			if (cachedResponse) {
				// 使用缓存的回答快速响应
				setTimeout(() => {
					this.messages.push({
						type: 'bot',
						content: cachedResponse,
						time: this.formatTime(new Date()),
						isFromCache: true // 标记为缓存回答
					});
					
					this.saveChatHistory();
					this.scrollToBottom();
					this.isTyping = false;
				}, 500); // 添加短暂延迟让体验更自然
				
				return;
			}
			
			// 如果不是缓存的问题，则调用后端API
			await this.callAssistantAPI(userQuestion);
		},
		
		// 从缓存中检查常见问题的回答
		checkResponseCache(question) {
			// 检查是否匹配常见问题
			for (const key in RESPONSE_CACHE) {
				if (question.includes(key)) {
					console.log('从缓存获取回答:', key);
					return RESPONSE_CACHE[key];
				}
			}
			
			// 如果是简单的问候语，也可以快速响应
			if (this.isGreeting(question)) {
				return '你好！很高兴为你服务。请问有什么我可以帮助你的吗？';
			}
			
			return null;
		},
		
		// 判断是否是简单问候语
		isGreeting(text) {
			const greetings = ['你好', '您好', 'hello', 'hi', '嗨', '哈喽', '早上好', '中午好', '晚上好', '晚安'];
			const lowerText = text.toLowerCase();
			
			return greetings.some(greeting => lowerText.includes(greeting));
		},
		
		// 调用助手API的方法，包含重试逻辑
		async callAssistantAPI(userQuestion) {
			try {
				// 调用后端API
				const response = await request({
					url: '/api/assistant/chat',
					method: 'POST',
					data: {
						message: userQuestion,
						session_id: this.sessionId || ''
					},
					timeout: 15000 // 设置较短的超时时间
				});
				
				// 处理响应
				if (response.session_id) {
					this.sessionId = response.session_id;
				}
				
				// 添加机器人回复
				this.messages.push({
					type: 'bot',
					content: response.text,
					time: this.formatTime(new Date())
				});
				
				// 保存更新后的聊天记录到本地
				this.saveChatHistory();
				
				this.scrollToBottom();
				this.isTyping = false;
			} catch (error) {
				console.error('与AI助手交互时出错:', error);
				
				// 判断是否需要重试
				if (this.retryCount < this.maxRetries) {
					this.retryCount++;
					console.log(`请求失败，第${this.retryCount}次重试...`);
					
					// 提示用户正在重试
					if (this.retryCount === 1) {
						uni.showToast({
							title: '网络不稳定，正在重试...',
							icon: 'none',
							duration: 1500
						});
					}
					
					// 递增延迟重试
					setTimeout(() => {
						this.callAssistantAPI(userQuestion);
					}, 1000 * this.retryCount);
					return;
				}
				
				// 超过重试次数，使用本地生成的回复
				const fallbackResponse = this.generateFallbackResponse(userQuestion);
				
				// 添加错误提示消息
				this.messages.push({
					type: 'bot',
					content: fallbackResponse,
					time: this.formatTime(new Date()),
					isLocal: true // 标记为本地生成的回复
				});
				
				// 保存错误消息到本地
				this.saveChatHistory();
				
				// 显示错误提示
				uni.showToast({
					title: '网络请求失败，已使用离线回复',
					icon: 'none',
					duration: 2000
				});
				
				this.isTyping = false;
				this.scrollToBottom();
			}
		},
		
		// 生成本地回复
		generateFallbackResponse(question) {
			// 预设的通用回复
			const fallbackResponses = [
				'很抱歉，我暂时无法连接到服务器。您可以尝试询问一些关于旅游景点、路线规划或旅行攻略的常见问题，我会尽力在本地为您提供帮助。',
				'网络连接不稳定，我无法获取最新信息。不过我能回答一些常见的旅游问题，您可以尝试问问关于热门景点、旅行预算或拍照地点的问题。',
				'抱歉，连接服务器时出现错误。您可以尝试稍后再试，或者提问一些基础的旅游咨询问题。'
			];
			
			// 尝试匹配关键词生成更相关的回复
			if (question.includes('景点') || question.includes('旅游') || question.includes('地方')) {
				return '抱歉，我无法获取最新的景点信息。一般来说，选择旅游景点可以考虑以下因素：知名度、季节适宜性、交通便利性、性价比和个人兴趣。您有特别感兴趣的地区或类型的景点吗？';
			} else if (question.includes('预算') || question.includes('花费') || question.includes('价格')) {
				return '很抱歉，我现在无法为您提供详细的预算建议。旅行预算通常需要考虑交通、住宿、餐饮、景点门票和购物等因素。一般来说，国内城市旅行每人每天预算大约在300-1000元之间，具体取决于目的地和您的消费习惯。';
			} else if (question.includes('攻略') || question.includes('行程') || question.includes('计划')) {
				return '抱歉，我无法获取最新的旅行攻略。制定旅行计划时，建议您考虑旅行天数、目的地距离、景点分布和开放时间，以及您的兴趣和体力。通常3-4天的行程适合游览一个中型城市及其周边景点。';
			}
			
			// 随机返回一个通用回复
			return fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
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
		
		// 添加清空聊天记录功能
		clearChatHistory() {
			// 显示确认弹窗
			uni.showModal({
				title: '确认清空',
				content: '确定要清空所有聊天记录吗？',
				success: (res) => {
					if (res.confirm) {
						// 保留初始欢迎消息
						this.messages = [
							{
								type: 'bot',
								content: '👋 你好！我是你的智能旅行助手，可以为你提供旅游景点推荐、路线规划、旅行攻略等服务。有什么可以帮你的吗？',
								time: this.formatTime(new Date())
							}
						];
						this.sessionId = null;
						
						// 清除本地存储
						uni.removeStorageSync('assistant_messages');
						uni.removeStorageSync('assistant_session_id');
						
						// 提示用户
						uni.showToast({
							title: '聊天记录已清空',
							icon: 'success'
						});
					}
				}
			});
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
			// 完整处理Markdown格式
			let html = content;
			
			// 处理标题 (h1-h6)
			html = html.replace(/#{1,6}\s+([^\n]+)/g, (match, text) => {
				const level = match.trim().indexOf(' ');
				return `<h${level} style="font-size: ${28 - (level-1)*2}px; margin-top: 16rpx; margin-bottom: 16rpx; font-weight: bold;">${text}</h${level}>`;
			});
			
			// 处理代码块
			html = html.replace(/```([^`]+)```/g, '<div class="code-block">$1</div>');
			
			// 处理行内代码
			html = html.replace(/`([^`]+)`/g, '<code style="background-color: #f1f1f1; padding: 4rpx 8rpx; border-radius: 4rpx; font-family: monospace;">$1</code>');
			
			// 处理粗体
			html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
			
			// 处理斜体
			html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
			
			// 处理有序列表
			html = html.replace(/^\d+\.\s+([^\n]+)/gm, '<li style="margin-left: 20rpx; list-style-type: decimal;">$1</li>');
			
			// 处理无序列表
			html = html.replace(/^[\-\*]\s+([^\n]+)/gm, '<li style="margin-left: 20rpx; list-style-type: disc;">$1</li>');
			
			// 处理链接
			html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" style="color: #3182ce; text-decoration: underline;">$1</a>');
			
			// 处理图片
			html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" style="max-width: 100%; border-radius: 8rpx;" />');
			
			// 处理水平线
			html = html.replace(/^---+$/gm, '<hr style="border: 0; height: 1px; background: #eee; margin: 16rpx 0;" />');
			
			// 处理引用块
			html = html.replace(/^>\s+([^\n]+)/gm, '<blockquote style="border-left: 4px solid #eee; padding-left: 16rpx; color: #666; margin: 16rpx 0;">$1</blockquote>');
			
			// 处理段落
			html = html.replace(/(?<!\n)\n(?!\n)/g, '<br>');
			
			// 包装有序列表和无序列表项到列表容器中
			if (html.includes('<li')) {
				// 找到所有列表项并包装
				let tempHtml = html;
				html = tempHtml.replace(/(<li[^>]*>.*?<\/li>)+/gs, function(match) {
					// 检查第一个列表项的类型
					if (match.includes('list-style-type: decimal')) {
						return `<ol style="padding-left: 20rpx; margin: 16rpx 0;">${match}</ol>`;
					} else {
						return `<ul style="padding-left: 20rpx; margin: 16rpx 0;">${match}</ul>`;
					}
				});
			}
			
			return html;
		},
		
		generateResponse(question) {
			// 优先使用预设的缓存回复
			for (const key in RESPONSE_CACHE) {
				if (question.includes(key)) {
					return RESPONSE_CACHE[key];
				}
			}
			
			// 否则使用默认回复
			return '感谢您的提问！这是一个本地生成的回复。您可以尝试点击下方的快捷问题，或者询问关于旅游景点、路线规划、旅行攻略等问题，我会尽力为您提供帮助。';
		}
	}
}
</script>

<style lang="scss">
	page {
		background-color: #f8f9fa;
	}
	
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
		position: relative;
		z-index: 2;
		
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
			flex: 1;
			
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
		
		.header-actions {
			display: flex;
			align-items: center;
			
			.clear-btn {
				width: 60rpx;
				height: 60rpx;
				display: flex;
				align-items: center;
				justify-content: center;
				border-radius: 50%;
				background-color: rgba(255, 255, 255, 0.2);
				transition: all 0.3s;
				
				&:active {
					transform: scale(0.9);
					background-color: rgba(255, 255, 255, 0.3);
				}
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
		background-color: #f8f9fa;
		position: relative;
		z-index: 1;
	}
	
	.bottom-space {
		height: 40rpx; /* 底部额外留白，避免最后一条消息被输入框遮挡 */
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
		
		code {
			font-family: monospace;
			background-color: #f1f1f1;
			padding: 4rpx 8rpx;
			border-radius: 4rpx;
			font-size: 28rpx;
		}
		
		a {
			color: #3182ce;
			text-decoration: underline;
		}
		
		img {
			max-width: 100%;
			border-radius: 8rpx;
			margin: 10rpx 0;
		}
		
		blockquote {
			border-left: 4px solid #eee;
			padding-left: 16rpx;
			color: #666;
			margin: 16rpx 0;
		}
		
		ul, ol {
			padding-left: 20rpx;
			margin: 16rpx 0;
		}
		
		li {
			margin-left: 20rpx;
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
		position: sticky;
		bottom: 0;
		left: 0;
		right: 0;
		z-index: 10;
		box-shadow: 0 -2rpx 10rpx rgba(0,0,0,0.05);
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