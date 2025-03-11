<template>
	<view class="my-page">
		<view class="tops">
			<uni-icons type="gear" size="32" class="setIcon" @click="setFun"></uni-icons>
			<view class="auth-section" @click="handleAuth">
				<image 
					:src="avatarUrl || '/static/default-avatar.png'"
					class="auth-avatar"
					mode="aspectFill"
				></image>
				<text class="auth-title">{{ isLogged ? nickName : '登录/注册' }}</text>
			</view>
		</view>

		<view class="dashboard">
			<view v-for="(item,index) in statsData" :key="index" class="stat-item">
				<view class="stat-icon">
					<uni-icons :type="getStatIcon(item.label)" size="30" color="#007AFF"/>
				</view>
				<text class="stat-value">{{ item.value }}</text>
				<text class="stat-label">{{ item.label }}</text>
			</view>
		</view>

		<view class="function-grid">
			<view v-for="(group,gIndex) in functionGroups" :key="gIndex" class="grid-group">
				<view 
					v-for="(item,index) in group" 
					:key="index"
					class="grid-item"
					@click="handleFunction(item)"
				>
					<view class="item-icon">
						<uni-icons :type="item.icon" size="30" color="#666"/>
					</view>
					<text class="item-label">{{ item.label }}</text>
				</view>
			</view>
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
						{ label: '我的钱包', type: 'balance', icon: 'wallet' },
						{ label: '实名认证', type: 'certification', icon: 'vip' }
					],
					[
						{ label: '联系客服', type: 'service', icon: 'headphones' },
						{ label: '用户反馈', type: 'feedback', icon: 'chat' },
						{ label: '系统设置', type: 'settings', icon: 'gear' }
					]
				]
			}
		},
		onLoad() {
			const userInfo = uni.getStorageSync('userInfo')
			if(userInfo) {
				this.isLogged = true
				this.nickName = userInfo.nickname
				this.avatarUrl = userInfo.avatar
			}
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
					const res = await new Promise((resolve, reject) => {
						uni.getSetting({
							success: (result) => resolve(result),
							fail: (error) => reject(error)
						});
					});
					
					if (res.authSetting['scope.userInfo']) {
						// 不再直接调用 getUserInfo
						// 而是检查本地存储的用户信息
						const userInfo = uni.getStorageSync('userInfo');
						if (userInfo) {
							this.avatarUrl = userInfo.avatar;
							this.nickName = userInfo.nickname;
							this.isLogged = true;
						}
					}
				} catch (error) {
					console.error('获取设置失败：', error);
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
					uni.showLoading({ title: '登录中...' })
					
					// 1. 获取用户信息
					uni.getUserProfile({
						desc: '用于完善会员信息',
						lang: 'zh_CN',
						success: async (res) => {
							// 2. 获取微信code
							uni.login({
								provider: 'weixin',
								success: async (loginRes) => {
									try {
										// 3. 调用云函数
										const result = await uniCloud.callFunction({
											name: 'login',
											data: {
												code: loginRes.code,
												userInfo: {
													nickName: res.userInfo.nickName,
													avatarUrl: res.userInfo.avatarUrl
												}
											}
										})
										
										if(result.result.code === 200) {
											// 4. 保存登录状态
											uni.setStorageSync('token', result.result.data.token)
											uni.setStorageSync('userInfo', result.result.data.userInfo)
											
											// 5. 更新页面数据
											this.isLogged = true
											this.nickName = result.result.data.userInfo.nickname
											this.avatarUrl = result.result.data.userInfo.avatar
											
											uni.showToast({ title: '登录成功' })
										} else {
											uni.showToast({ 
												title: result.result.msg || '登录失败',
												icon: 'none'
											})
										}
									} catch (e) {
										console.error(e)
										uni.showToast({ 
											title: '登录请求失败',
											icon: 'none'
										})
									}
									uni.hideLoading()
								},
								fail: () => {
									uni.hideLoading()
									uni.showToast({ 
										title: '微信登录失败',
										icon: 'none'
									})
								}
							})
						},
						fail: () => {
							uni.hideLoading()
							uni.showToast({ 
								title: '需要授权才能登录',
								icon: 'none'
							})
						}
					})
				}
			},

			handleFunction(item) {
				const routeMap = {
					'info': '/pages/mine/profile',
					'balance': '/pages/mine/wallet',
					'settings': '/pages/mine/settings'
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
			},

			setFun() {
				uni.navigateTo({ url: '/pages/mine/settings' });
			}
		}
	}
</script>

<style>
	.my-page {
		background: #f5f5f5;
		min-height: 100vh;
	}

	.tops {
		position: relative;
		height: 300rpx;
		background: linear-gradient(135deg, #1976D2 0%, #64B5F6 100%);
		box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
	}

	.auth-section {
		position: absolute;
		bottom: 40rpx;
		left: 40rpx;
		right: 40rpx;
		background: rgba(255,255,255,0.95);
		border-radius: 20rpx;
		padding: 30rpx;
		display: flex;
		align-items: center;
		box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
		backdrop-filter: blur(10px);
	}

	.auth-avatar {
		width: 100rpx;
		height: 100rpx;
		border-radius: 50%;
		margin-right: 30rpx;
		border: 4rpx solid rgba(255,255,255,0.8);
		box-shadow: 0 2rpx 8rpx rgba(0,0,0,0.1);
	}

	.auth-title {
		font-size: 36rpx;
		color: #333;
		font-weight: 500;
		flex: 1;
	}

	.dashboard {
		display: flex;
		justify-content: space-around;
		background: #fff;
		border-radius: 20rpx;
		padding: 40rpx 0;
		margin: 20rpx;
		box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
	}

	.stat-item {
		display: flex;
		flex-direction: column;
		align-items: center;
		position: relative;
	}

	.stat-item:not(:last-child):after {
		content: '';
		position: absolute;
		right: -50%;
		top: 50%;
		transform: translateY(-50%);
		width: 2rpx;
		height: 40rpx;
		background: rgba(0,0,0,0.1);
	}

	.stat-value {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		margin: 12rpx 0;
	}

	.stat-label {
		font-size: 24rpx;
		color: #666;
	}

	.function-grid {
		background: #fff;
		border-radius: 20rpx;
		margin: 20rpx;
		box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.05);
		overflow: hidden;
	}

	.grid-group {
		display: flex;
		flex-wrap: wrap;
		border-bottom: 1rpx solid #eee;
	}

	.grid-item {
		width: 33.33%;
		padding: 30rpx 0;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.item-label {
		font-size: 28rpx;
		color: #444;
		margin-top: 15rpx;
	}

	.setIcon {
		position: absolute;
		top: 50rpx;
		right: 50rpx;
		z-index: 1;
		color: #fff;
		background: rgba(255,255,255,0.2);
		border-radius: 50%;
		padding: 10rpx;
		backdrop-filter: blur(5px);
	}
</style>