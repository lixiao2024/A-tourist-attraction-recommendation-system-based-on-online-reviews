<template>
	<view class="my-page">
		<!-- 顶部背景区域 -->
		<view class="tops">
			<view class="bg-pattern"></view>
			<view class="auth-section" @click="handleAuth">
				<view class="avatar-container">
					<image 
						:src="avatarUrl || '/static/default-avatar.png'"
						class="auth-avatar"
						mode="aspectFill"
					></image>
					<view class="avatar-status" v-if="isLogged"></view>
				</view>
				<view class="user-info">
					<text class="auth-title">{{ isLogged ? nickName : '登录/注册' }}</text>
					<text class="auth-subtitle" v-if="isLogged">普通用户</text>
					<text class="auth-subtitle" v-else>登录后体验更多功能</text>
				</view>
				<view class="auth-arrow" v-if="isLogged">
					<uni-icons type="right" size="16" color="#666"></uni-icons>
				</view>
			</view>
		</view>

		<!-- 数据统计面板 -->
		<view class="dashboard">
			<view v-for="(item,index) in statsData" :key="index" class="stat-item" hover-class="stat-item-hover">
				<view class="stat-icon">
					<uni-icons :type="getStatIcon(item.label)" size="22" color="#007AFF"/>
				</view>
				<text class="stat-value">{{ item.value }}</text>
				<text class="stat-label">{{ item.label }}</text>
			</view>
		</view>

		<!-- 功能区域 -->
		<view class="function-grid">
			<view v-for="(group,gIndex) in functionGroups" :key="gIndex" class="grid-group">
				<view 
					v-for="(item,index) in group" 
					:key="index"
					class="grid-item"
					hover-class="grid-item-hover"
					@click="handleFunction(item)"
				>
					<view class="item-icon-container">
						<uni-icons :type="item.icon" size="24" color="#007AFF"/>
					</view>
					<text class="item-label">{{ item.label }}</text>
				</view>
			</view>
		</view>
		
		<!-- 版本信息 -->
		<view class="app-version">
			<text class="version-text">版本 1.0.0</text>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				isLogged: false,
				nickName: '',
				avatarUrl: '',
				statsData: [
					{ label: '粉丝', value: 0, icon: 'person' },
					{ label: '获赞', value: 0, icon: 'heart' },
					{ label: '关注', value: 0, icon: 'eye' },
					{ label: '收藏', value: 45, icon: 'star' }
				],
				functionGroups: [
					[
						{ label: '个人信息', type: 'info', icon: 'info' },
						{ label: '我的笔记', type: 'notes', icon: 'bars' },
						{ label: '用户反馈', type: 'feedback', icon: 'chat' }
					]
				]
			}
		},
		onLoad() {
			console.log('页面加载，开始初始化...');
			// 检查登录状态并加载用户信息
			this.checkLoginStatus();
			
			// 加载用户统计数据
			this.loadUserStatsData();
			console.log('页面初始化完成');
		},
		// 添加onShow生命周期，确保每次进入页面都检查登录状态
		onShow() {
			console.log('页面显示，检查登录状态...');
			// 检查登录状态并加载用户信息
			this.checkLoginStatus();
			
			// 加载用户统计数据
			this.loadUserStatsData();
		},
		methods: {
			// 加载用户统计数据
			loadUserStatsData() {
				// 从本地存储获取用户统计数据
				const statsData = uni.getStorageSync('userStatsData');
				if (statsData && Array.isArray(statsData)) {
					// 更新页面上的统计数据
					statsData.forEach(item => {
						const index = this.statsData.findIndex(stat => stat.label === item.label);
						if (index !== -1) {
							this.statsData[index].value = item.value;
						}
					});
				}
			},
			
			async checkLoginStatus() {
				try {
					console.log('开始检查登录状态...');
					// 检查是否有token，判断用户是否已登录
					const token = uni.getStorageSync('token');
					console.log('从存储中读取token:', token ? '已获取' : '未获取');
					
					if (token) {
						const userInfo = uni.getStorageSync('userInfo');
						console.log('从存储中读取用户信息:', userInfo);
						
						if (userInfo) {
							// 确保使用正确的属性名
							this.avatarUrl = userInfo.avatar || userInfo.avatarUrl;
							this.nickName = userInfo.nickname || userInfo.nickName;
							this.isLogged = true;
							console.log('用户已登录，信息加载完成', this.nickName, this.avatarUrl);
							
							// 如果有token但无用户信息，可以调用后端获取用户信息
							// 这里暂时不实现该逻辑
						} else {
							// 有token但无用户信息时，尝试从后端获取用户信息
							console.log('有token但无用户信息，尝试获取用户数据');
							await this.fetchUserInfo(token);
						}
					} else {
						this.isLogged = false;
						this.avatarUrl = '';
						this.nickName = '';
						console.log('用户未登录');
					}
				} catch (error) {
					console.error('获取登录状态失败:', error);
					this.isLogged = false;
				}
			},
			
			// 从后端获取用户信息
			async fetchUserInfo(token) {
				try {
					// 模拟API请求获取用户信息
					// 实际项目中应替换为真实接口调用
					console.log('向后端发送获取用户信息请求...');
					// 由于是示例，这里我们直接从本地存储获取用户基本信息
					// 实际项目中应该使用以下代码发送请求
					/*
					const result = await uni.request({
						url: 'http://localhost:8000/api/user/info',
						method: 'GET',
						header: {
							'Authorization': `Bearer ${token}`,
							'content-type': 'application/json'
						}
					});
					
					if (result.statusCode === 200) {
						const userInfo = result.data;
						// 保存用户信息
						uni.setStorageSync('userInfo', userInfo);
						
						// 更新页面数据
						this.avatarUrl = userInfo.avatar;
						this.nickName = userInfo.nickname;
						this.isLogged = true;
					}
					*/
					
					// 模拟获取，检查openid是否存在
					const openid = uni.getStorageSync('openid');
					const userId = uni.getStorageSync('user_id');
					
					if (openid || userId) {
						console.log('找到用户ID，尝试从其他信息重建用户数据');
						// 创建基本用户信息
						const userInfo = {
							nickname: '微信用户',
							avatar: '/static/default-avatar.png'
						};
						
						// 保存到本地
						uni.setStorageSync('userInfo', userInfo);
						
						// 更新页面数据
						this.avatarUrl = userInfo.avatar;
						this.nickName = userInfo.nickname;
						this.isLogged = true;
					}
				} catch (error) {
					console.error('获取用户信息失败:', error);
				}
			},
			
			async getUserInfo(e) {
				// 添加参数检查
				if (!e || !e.detail) return;
				
				if (e.detail.errMsg === 'getUserInfo:ok') {
					const userInfo = e.detail.userInfo;
					this.avatarUrl = userInfo.avatarUrl;
					this.nickName = userInfo.nickName;
					this.isLogged = true;
				}
			},

			handleAuth() {
				if(!this.isLogged) {
					console.log('用户点击登录按钮');
					uni.showLoading({ title: '登录中...' })
					
					// 1. 获取用户信息
					uni.getUserProfile({
						desc: '用于完善会员信息',
						lang: 'zh_CN',
						success: async (res) => {
							console.log('获取到用户个人信息:', {
								nickName: res.userInfo.nickName,
								avatarUrl: res.userInfo.avatarUrl
							});
							
							// 2. 获取微信code
							uni.login({
								provider: 'weixin',
								success: async (loginRes) => {
									try {
										console.log('获取到微信登录code:', loginRes.code);
										
										// 3. 调用后端API进行登录验证
										console.log('准备向后端发送登录请求...');
										const result = await uni.request({
											url: 'http://localhost:8000/api/wechat-login', // 修改为simple_app.py中的路由路径
											method: 'POST',
											data: {
												code: loginRes.code,
												user_info: {
													nickname: res.userInfo.nickName,
													avatar_url: res.userInfo.avatarUrl,
													gender: res.userInfo.gender,
													country: res.userInfo.country,
													province: res.userInfo.province,
													city: res.userInfo.city,
													language: res.userInfo.language
												}
											},
											header: {
												'content-type': 'application/json'
											}
										});
										
										console.log('收到后端响应:', result);
										
										// 检查请求是否成功
										if (result.statusCode === 200) {
											const data = result.data;
											console.log('登录成功, 获取到token和openid:', {
												token: data.access_token,
												openid: data.openid,
												user_id: data.user_id
											});
											
											// 4. 保存登录状态
											uni.setStorageSync('token', data.access_token);
											uni.setStorageSync('openid', data.openid);
											uni.setStorageSync('user_id', data.user_id);
											
											// 获取用户信息 - 从微信获取而非后端
											const userInfo = {
												nickname: res.userInfo.nickName,
												avatar: res.userInfo.avatarUrl,
												gender: res.userInfo.gender,
												country: res.userInfo.country,
												province: res.userInfo.province,
												city: res.userInfo.city,
												language: res.userInfo.language
											};
											console.log('保存用户信息:', userInfo);
											uni.setStorageSync('userInfo', userInfo);
											
											// 5. 更新页面数据
											this.isLogged = true;
											this.nickName = res.userInfo.nickName;
											this.avatarUrl = res.userInfo.avatarUrl;
											
											uni.showToast({ title: '登录成功' });
										} else {
											console.error('登录失败:', result.data);
											uni.showToast({ 
												title: result.data?.detail || '登录失败',
												icon: 'none'
											});
										}
									} catch (e) {
										console.error('登录请求异常:', e);
										uni.showToast({ 
											title: '登录请求失败',
											icon: 'none'
										});
									}
									uni.hideLoading();
								},
								fail: (err) => {
									console.error('获取微信code失败:', err);
									uni.hideLoading();
									uni.showToast({ 
										title: '微信登录失败',
										icon: 'none'
									});
								}
							});
						},
						fail: (err) => {
							console.error('用户拒绝授权:', err);
							uni.hideLoading();
							uni.showToast({ 
								title: '需要授权才能登录',
								icon: 'none'
							});
						}
					});
				} else {
					console.log('用户已登录，点击查看个人信息');
					// 可以跳转到个人信息页面
				}
			},

			handleFunction(item) {
				const routeMap = {
					'info': '/pages/mine/profile',
					'notes': '/pages/mine/notes',
					'feedback': '/pages/mine/feedback'
				}
				if(routeMap[item.type]) {
					uni.navigateTo({ url: routeMap[item.type] });
				} else {
					uni.showToast({
						title: `${item.label}功能开发中`,
						icon: 'none'
					});
				}
			},

			getStatIcon(label) {
				const iconMap = {
					'粉丝': 'person',
					'获赞': 'heart',
					'关注': 'eye',
					'收藏': 'star'
				};
				return iconMap[label] || 'help';
			}
		}
	}
</script>

<style>
	.my-page {
		background: #f8f9fa;
		min-height: 100vh;
		padding-bottom: 40rpx;
	}

	.tops {
		position: relative;
		height: 360rpx;
		background: linear-gradient(120deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
		box-shadow: 0 4rpx 20rpx rgba(0,0,0,0.15);
		overflow: hidden;
		border-bottom-left-radius: 40rpx;
		border-bottom-right-radius: 40rpx;
	}
	
	.bg-pattern {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		opacity: 0.1;
		background-image: radial-gradient(circle at 20% 80%, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 20%),
						  radial-gradient(circle at 80% 20%, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0) 20%);
	}

	.auth-section {
		position: absolute;
		bottom: 40rpx;
		left: 40rpx;
		right: 40rpx;
		background: rgba(255,255,255,0.95);
		border-radius: 24rpx;
		padding: 30rpx;
		display: flex;
		align-items: center;
		box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.08);
		backdrop-filter: blur(10px);
		transition: all 0.3s ease;
	}
	
	.auth-section:active {
		transform: scale(0.98);
		box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.06);
	}

	.avatar-container {
		position: relative;
	}
	
	.avatar-status {
		position: absolute;
		bottom: 4rpx;
		right: 4rpx;
		width: 20rpx;
		height: 20rpx;
		border-radius: 50%;
		background: #4CAF50;
		border: 3rpx solid #fff;
		box-shadow: 0 2rpx 4rpx rgba(0,0,0,0.1);
	}

	.auth-avatar {
		width: 120rpx;
		height: 120rpx;
		border-radius: 50%;
		margin-right: 30rpx;
		border: 4rpx solid rgba(255,255,255,0.9);
		box-shadow: 0 4rpx 16rpx rgba(0,0,0,0.15);
		transition: all 0.3s ease;
	}
	
	.user-info {
		flex: 1;
		display: flex;
		flex-direction: column;
	}

	.auth-title {
		font-size: 36rpx;
		color: #333;
		font-weight: 600;
		margin-bottom: 8rpx;
	}
	
	.auth-subtitle {
		font-size: 24rpx;
		color: #888;
	}
	
	.auth-arrow {
		width: 40rpx;
		height: 40rpx;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.dashboard {
		display: flex;
		justify-content: space-around;
		background: #fff;
		border-radius: 24rpx;
		padding: 40rpx 20rpx;
		margin: 30rpx 20rpx;
		box-shadow: 0 8rpx 24rpx rgba(0,0,0,0.06);
	}
	
	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		position: relative;
		padding: 10rpx 30rpx;
		border-radius: 16rpx;
		transition: all 0.2s ease;
	}
	
	.stat-item-hover {
		background-color: rgba(0,122,255,0.05);
	}

	.stat-item:not(:last-child):after {
		content: '';
		position: absolute;
		right: -20rpx;
		top: 50%;
		transform: translateY(-50%);
		width: 1px;
		height: 60%;
		background: rgba(0,0,0,0.06);
	}

	.stat-icon {
		width: 80rpx;
		height: 80rpx;
		background: rgba(0,122,255,0.1);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 16rpx;
	}

	.stat-value {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		margin: 6rpx 0;
	}

	.stat-label {
		font-size: 24rpx;
		color: #666;
	}

	.function-grid {
		background: #fff;
		border-radius: 24rpx;
		margin: 20rpx;
		box-shadow: 0 8rpx 24rpx rgba(0,0,0,0.06);
		overflow: hidden;
	}

	.grid-group {
		display: flex;
		flex-wrap: wrap;
	}
	
	.grid-group:not(:last-child) {
		border-bottom: 1px solid rgba(0,0,0,0.04);
	}

	.grid-item {
		width: 33.33%;
		padding: 40rpx 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		transition: all 0.2s ease;
	}
	
	.grid-item-hover {
		background-color: rgba(0,0,0,0.02);
	}
	
	.item-icon-container {
		width: 100rpx;
		height: 100rpx;
		background: rgba(0,122,255,0.08);
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin-bottom: 16rpx;
		transition: all 0.3s ease;
	}
	
	.grid-item-hover .item-icon-container {
		transform: scale(1.1);
		background: rgba(0,122,255,0.12);
	}

	.item-label {
		font-size: 28rpx;
		color: #333;
		margin-top: 15rpx;
	}
	
	.app-version {
		text-align: center;
		padding: 40rpx 0 20rpx;
	}
	
	.version-text {
		font-size: 24rpx;
		color: #999;
	}
</style>