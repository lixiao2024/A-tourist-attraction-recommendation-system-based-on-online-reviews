<template>
	<view class="my-page">
		<!-- 顶部背景区域 -->
		<view class="tops">
			<view class="bg-pattern"></view>
			<view class="auth-section" @click="showLoginModal">
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
		
		<!-- 登录模态框 -->
		<view class="login-modal" v-if="showModal" @click.stop="closeLoginModal">
			<view class="modal-mask"></view>
			<view class="modal-content" @click.stop>
				<view class="modal-header">
					<text class="modal-title">微信登录</text>
					<view class="close-btn" @click="closeLoginModal">
						<uni-icons type="closeempty" size="20" color="#999"></uni-icons>
					</view>
				</view>
				<view class="modal-body">
					<image src="/static/wechat-login.png" class="wechat-logo" mode="aspectFit"></image>
					<text class="modal-tips">授权后可同步您的微信昵称和头像</text>
					
					<!-- 分步骤登录 -->
					<view v-if="loginStep === 1">
						<!-- 先使用getUserProfile获取基本信息并登录 -->
						<button 
							v-if="canIUseGetUserProfile"
							class="auth-button"
							@click="getUserProfile"
						>微信一键登录</button>
						<button 
							v-else
							class="auth-button" 
							open-type="getUserInfo"
							@getuserinfo="getUserInfo"
						>微信一键登录</button>
					</view>
					
					<!-- 完善头像昵称信息 -->
					<view v-else-if="loginStep === 2" class="profile-form">
						<text class="form-title">完善头像和昵称</text>
						
						<!-- 选择头像按钮 -->
						<button class="avatar-wrapper" open-type="chooseAvatar" @chooseavatar="onChooseAvatar">
							<image class="avatar-preview" :src="tempAvatarUrl || '/static/default-avatar.png'" mode="aspectFill"></image>
							<text class="avatar-tip">点击选择头像</text>
						</button>
						
						<!-- 输入昵称 -->
						<view class="nickname-wrapper">
							<text class="label">昵称</text>
							<input 
								type="nickname" 
								class="nickname-input" 
								placeholder="请输入昵称" 
								v-model="tempNickName"
								@change="onInputNickname" 
							/>
						</view>
						
						<!-- 保存信息按钮 -->
						<button class="save-button" @click="saveUserInfo">保存</button>
					</view>
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
				showModal: false,
				canIUseGetUserProfile: false, // 是否支持getUserProfile
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
						{ label: '我的足迹', type: 'footprint', icon: 'location' },
						{ label: '用户反馈', type: 'feedback', icon: 'chat' }
					]
				],
				loginStep: 1,
				tempAvatarUrl: '',
				tempNickName: ''
			}
		},
		onLoad() {
			console.log('页面加载，开始初始化...');
			// 检查是否支持getUserProfile
			if (wx.getUserProfile) {
				this.canIUseGetUserProfile = true;
				console.log('当前环境支持getUserProfile');
			} else {
				console.log('当前环境不支持getUserProfile，将使用getUserInfo');
			}
			
			// 直接刷新登录状态
			this.refreshLoginStatus();
			
			// 尝试从App全局状态获取登录信息
			const app = getApp();
			if (app.globalData && app.globalData.isLoggedIn && app.globalData.userInfo) {
				console.log('从App全局状态获取登录信息:', app.globalData.userInfo);
				this.avatarUrl = app.globalData.userInfo.avatar || app.globalData.userInfo.avatarUrl || '';
				this.nickName = app.globalData.userInfo.nickname || app.globalData.userInfo.nickName || '';
				this.isLogged = true;
			} else {
				// 检查登录状态并加载用户信息
				this.checkLoginStatus();
			}
			
			// 加载用户统计数据
			this.loadUserStatsData();
			
			// 添加全局登录成功事件监听
			uni.$on('loginSuccess', this.handleLoginSuccess);
			// 添加全局登录状态变化事件监听
			uni.$on('loginStatusChanged', this.handleLoginStatusChanged);
			
			console.log('页面初始化完成');
		},
		// 添加onShow生命周期，确保每次进入页面都检查登录状态
		onShow() {
			console.log('页面显示，检查登录状态...');
			
			// 检查存储中的数据完整性
			this.checkStorageIntegrity();
			
			// 检查登录状态并加载用户信息
			this.checkLoginStatus();
			
			// 加载用户统计数据
			this.loadUserStatsData();
		},
		// 页面销毁时清除事件监听
		onUnload() {
			uni.$off('loginSuccess', this.handleLoginSuccess);
			uni.$off('loginStatusChanged', this.handleLoginStatusChanged);
		},
		methods: {
			// 检查存储数据的完整性，防止不一致
			checkStorageIntegrity() {
				console.log('检查存储数据完整性...');
				const token = uni.getStorageSync('token');
				const userInfo = uni.getStorageSync('userInfo');
				
				if (userInfo && !token) {
					// 有用户信息但没有token，创建临时token
					const tempToken = 'temp_' + new Date().getTime();
					uni.setStorageSync('token', tempToken);
					console.log('修复存储: 创建临时token', tempToken);
				}
				
				if (token && !userInfo) {
					// 有token但没有用户信息，尝试创建默认用户信息
					const defaultUserInfo = {
						nickname: '微信用户',
						avatar: '/static/default-avatar.png',
						nickName: '微信用户',
						avatarUrl: '/static/default-avatar.png'
					};
					uni.setStorageSync('userInfo', defaultUserInfo);
					console.log('修复存储: 创建默认用户信息');
				}
				
				// 如果有用户信息和token，检查全局状态是否同步
				if (token && userInfo) {
					const app = getApp();
					if (app && app.globalData && !app.globalData.isLoggedIn) {
						app.globalData.isLoggedIn = true;
						app.globalData.userInfo = userInfo;
						console.log('修复全局状态: 用户已登录但全局状态未同步');
					}
				}
			},
			// 显示登录模态框
			showLoginModal() {
				if (!this.isLogged) {
					this.showModal = true;
				} else {
					console.log('用户已登录，点击查看个人信息');
					// 可以跳转到个人信息页面
					uni.navigateTo({ url: '/pages/mine/profile' });
				}
			},
			
			// 关闭登录模态框
			closeLoginModal() {
				this.showModal = false;
				// 重置登录步骤
				this.loginStep = 1;
				this.tempNickName = '';
				this.tempAvatarUrl = '';
			},
			
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
					console.log('从存储中读取token:', token ? `已获取: ${token.substring(0, 10)}...` : '未获取');
					
					if (token) {
						const userInfo = uni.getStorageSync('userInfo');
						console.log('从存储中读取用户信息:', userInfo ? JSON.stringify(userInfo).substring(0, 100) + '...' : '未获取');
						
						if (userInfo) {
							// 确保使用统一的属性名
							this.avatarUrl = userInfo.avatar || userInfo.avatarUrl || '';
							this.nickName = userInfo.nickname || userInfo.nickName || '';
							
							// 输出调试信息以便排查
							console.log('设置用户信息:', {
								设置的头像: this.avatarUrl,
								原始头像: userInfo.avatar || userInfo.avatarUrl,
								设置的昵称: this.nickName,
								原始昵称: userInfo.nickname || userInfo.nickName
							});
							
							this.isLogged = true;
							console.log('用户已登录，信息加载完成', this.nickName, this.avatarUrl);
							
							// 确保App全局状态也是最新的
							const app = getApp();
							if (app && app.globalData) {
								app.globalData.isLoggedIn = true;
								app.globalData.userInfo = userInfo;
								console.log('同步更新App全局状态');
							}
						} else {
							// 有token但无用户信息时，尝试从后端获取用户信息
							console.log('有token但无用户信息，尝试获取用户数据');
							await this.fetchUserInfo(token);
						}
					} else {
						// 检查是否有其他登录依据（如userInfo）
						const userInfo = uni.getStorageSync('userInfo');
						if (userInfo) {
							console.log('虽然没有token，但找到了用户信息', userInfo);
							// 仍然使用用户信息更新界面
							this.avatarUrl = userInfo.avatar || userInfo.avatarUrl || '';
							this.nickName = userInfo.nickname || userInfo.nickName || '';
							this.isLogged = true;
							console.log('基于用户信息更新登录状态');
							
							// 创建一个临时token，确保后续逻辑正常
							const tempToken = 'temp_' + new Date().getTime();
							uni.setStorageSync('token', tempToken);
							console.log('创建临时token:', tempToken);
						} else {
							this.isLogged = false;
							this.avatarUrl = '';
							this.nickName = '';
							console.log('用户未登录');
						}
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
						// 尝试从本地存储中获取微信用户信息
						const wxUserInfo = uni.getStorageSync('wx_user_info');
						
						let userInfo;
						if (wxUserInfo) {
							// 如果存在微信用户信息，使用它
							userInfo = {
								nickname: wxUserInfo.nickName,
								avatar: wxUserInfo.avatarUrl
							};
							console.log('使用存储的微信用户信息:', userInfo);
						} else {
							// 否则使用默认值
							userInfo = {
								nickname: '微信用户',
								avatar: '/static/default-avatar.png'
							};
							console.log('使用默认用户信息，无法获取微信资料');
						}
						
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
			
			// 处理微信登录
			getUserProfile() {
				console.log('调用getUserProfile获取用户信息');
				uni.showLoading({ title: '登录中...' });
				
				// 调用wx.getUserProfile获取用户信息
				wx.getUserProfile({
					desc: '用于完善会员资料', // 声明获取用户个人信息后的用途，会展示在弹窗中
					success: (res) => {
						console.log('获取到用户个人信息:', res.userInfo);
						
						// 保存微信原始用户信息，以便后续使用
						uni.setStorageSync('wx_user_info', res.userInfo);
						
						// 预填充临时头像和昵称
						this.tempAvatarUrl = res.userInfo.avatarUrl;
						this.tempNickName = res.userInfo.nickName;
						
						// 如果获取到的是"微信用户"或默认头像，则进入完善信息步骤
						if (res.userInfo.nickName === '微信用户' || !res.userInfo.avatarUrl) {
							console.log('获取到默认昵称或头像，进入完善信息步骤');
							this.loginStep = 2;
							uni.hideLoading();
						} else {
							// 否则直接使用获取到的信息登录
							// 获取到用户信息后，继续获取微信code并调用后端API
							this.loginWithWechat(res.userInfo);
						}
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
			},
			
			// 兼容旧版微信的获取用户信息方法
			getUserInfo(e) {
				console.log('通过getUserInfo获取用户信息');
				if (e.detail.userInfo) {
					// 用户同意授权
					console.log('获取到用户个人信息:', e.detail.userInfo);
					
					// 保存微信原始用户信息，以便后续使用
					uni.setStorageSync('wx_user_info', e.detail.userInfo);
					
					// 预填充临时头像和昵称
					this.tempAvatarUrl = e.detail.userInfo.avatarUrl;
					this.tempNickName = e.detail.userInfo.nickName;
					
					// 如果获取到的是"微信用户"或默认头像，则进入完善信息步骤
					if (e.detail.userInfo.nickName === '微信用户' || !e.detail.userInfo.avatarUrl) {
						console.log('获取到默认昵称或头像，进入完善信息步骤');
						this.loginStep = 2;
						uni.hideLoading();
					} else {
						// 否则直接使用获取到的信息登录
						this.loginWithWechat(e.detail.userInfo);
					}
				} else {
					// 用户拒绝授权
					console.error('用户拒绝授权');
					uni.showToast({ 
						title: '需要授权才能登录',
						icon: 'none'
					});
				}
			},
			
			// 使用微信登录
			loginWithWechat(userInfo) {
				// 获取微信code
				uni.login({
					provider: 'weixin',
					success: async (loginRes) => {
						try {
							console.log('获取到微信登录code:', loginRes.code);
							
							// 保存微信登录信息到本地，即使后端不可用也能显示头像和昵称
							const localUserInfo = {
								nickname: userInfo.nickName,
								avatar: userInfo.avatarUrl,
								gender: userInfo.gender,
								country: userInfo.country,
								province: userInfo.province,
								city: userInfo.city,
								language: userInfo.language
							};
							uni.setStorageSync('userInfo', localUserInfo);
							
							// 更新页面显示
							this.nickName = userInfo.nickName;
							this.avatarUrl = userInfo.avatarUrl;
							
							// 调用后端API进行登录验证
							console.log('准备向后端发送登录请求...');
							
							// 使用实际IP地址替换localhost
							// const backendUrl = 'http://localhost:8000/api/wechat-login';
							const backendUrl = 'http://192.168.1.10:8000/api/wechat-login'; // 替换为您的实际IP
							
							try {
								const result = await uni.request({
									url: backendUrl,
									method: 'POST',
									data: {
										code: loginRes.code,
										user_info: {
											nickname: userInfo.nickName,
											avatar_url: userInfo.avatarUrl,
											gender: userInfo.gender,
											country: userInfo.country,
											province: userInfo.province,
											city: userInfo.city,
											language: userInfo.language
										}
									},
									header: {
										'content-type': 'application/json'
									},
									timeout: 10000 // 增加超时时间
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
									
									// 保存登录状态
									uni.setStorageSync('token', data.access_token);
									uni.setStorageSync('openid', data.openid);
									uni.setStorageSync('user_id', data.user_id);
									
									// 记录日志，确认token是否保存成功
									const savedToken = uni.getStorageSync('token');
									console.log('保存并验证token成功:', savedToken ? '√ 已保存' : '× 未保存');
									
									// 发布全局登录成功事件，通知其他页面更新状态
									uni.$emit('loginSuccess', {
										isLoggedIn: true,
										userInfo: localUserInfo,
										token: data.access_token // 显式包含token
									});
									
									// 标记为已登录
									this.isLogged = true;
									
									uni.showToast({ title: '登录成功' });
								} else {
									console.error('登录失败:', result.data);
									uni.showToast({ 
										title: result.data?.detail || '登录失败',
										icon: 'none'
									});
									
									// 如果后端返回错误但我们已经保存了用户信息，仍然允许本地登录
									this.isLogged = true;
									uni.showToast({ title: '本地登录成功' });
								}
							} catch (e) {
								console.error('登录请求异常:', e);
								
								// 即使后端请求失败，也允许用户使用本地登录
								this.isLogged = true;
								uni.showToast({ 
									title: '本地登录成功，但无法连接服务器',
									icon: 'none',
									duration: 2000
								});
							}
						} catch (e) {
							console.error('登录过程出现异常:', e);
							uni.showToast({ 
								title: '登录处理失败',
								icon: 'none'
							});
						} finally {
							// 关闭模态框
							this.closeLoginModal();
							uni.hideLoading();
						}
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

			handleFunction(item) {
				const routeMap = {
					'info': '/pages/mine/profile',
					'notes': '/pages/mine/notes',
					'footprint': '/pages/footprint/footprint',
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
			},

			onChooseAvatar(e) {
				console.log('选择头像:', e.detail);
				this.tempAvatarUrl = e.detail.avatarUrl;
			},

			onInputNickname(e) {
				console.log('输入昵称:', e.detail.value);
				this.tempNickName = e.detail.value;
			},

			saveUserInfo() {
				if (!this.tempNickName.trim()) {
					uni.showToast({
						title: '请输入昵称',
						icon: 'none'
					});
					return;
				}
				
				if (!this.tempAvatarUrl) {
					uni.showToast({
						title: '请选择头像',
						icon: 'none'
					});
					return;
				}
				
				console.log('保存用户信息:', this.tempAvatarUrl, this.tempNickName);
				
				// 创建自定义用户信息对象
				const customUserInfo = {
					nickName: this.tempNickName,
					avatarUrl: this.tempAvatarUrl,
					gender: 0,
					country: '',
					province: '',
					city: '',
					language: 'zh_CN'
				};
				
				// 保存到本地存储
				uni.setStorageSync('wx_user_info', customUserInfo);
				
				// 调用登录方法
				this.loginWithWechat(customUserInfo);
			},

			handleLoginSuccess(data) {
				console.log('收到登录成功事件', data);
				
				if (data && data.userInfo) {
					// 直接使用事件传递的用户信息更新页面状态
					this.avatarUrl = data.userInfo.avatar || data.userInfo.avatarUrl || '';
					this.nickName = data.userInfo.nickname || data.userInfo.nickName || '';
					this.isLogged = true;
					
					console.log('通过事件更新用户信息:', {
						头像: this.avatarUrl,
						昵称: this.nickName
					});
					
					// 如果事件包含token，确保也保存到本地存储
					if (data.token) {
						console.log('从事件中获取并保存token');
						uni.setStorageSync('token', data.token);
					} else {
						// 如果没有传递token但确认登录成功，创建一个临时token
						const tempToken = 'temp_' + new Date().getTime();
						uni.setStorageSync('token', tempToken);
						console.log('事件中没有token，创建临时token:', tempToken);
					}
					
					// 加载用户统计数据
					this.loadUserStatsData();
				} else {
					// 如果没有传递用户信息，则重新检查登录状态
					this.checkLoginStatus();
				}
			},

			handleLoginStatusChanged(data) {
				console.log('收到登录状态变化事件', data);
				
				if (data && data.userInfo) {
					// 直接使用事件传递的用户信息更新页面状态
					this.avatarUrl = data.userInfo.avatar || data.userInfo.avatarUrl || '';
					this.nickName = data.userInfo.nickname || data.userInfo.nickName || '';
					this.isLogged = true;
					
					console.log('通过事件更新用户信息:', {
						头像: this.avatarUrl,
						昵称: this.nickName
					});
					
					// 如果事件包含token，确保也保存到本地存储
					if (data.token) {
						console.log('从状态变化事件中获取并保存token');
						uni.setStorageSync('token', data.token);
					}
					
					// 加载用户统计数据
					this.loadUserStatsData();
				} else {
					// 如果没有传递用户信息，则重新检查登录状态
					this.checkLoginStatus();
				}
			},

			// 刷新登录状态的方法，可以在需要时调用
			refreshLoginStatus() {
				console.log("主动刷新登录状态...");
				
				// 先清除当前页面状态
				this.isLogged = false; 
				this.avatarUrl = '';
				this.nickName = '';
				
				// 获取存储中最新的数据
				const token = uni.getStorageSync('token');
				const userInfo = uni.getStorageSync('userInfo');
				
				if (token && userInfo) {
					console.log("刷新状态: 找到有效的token和用户信息");
					// 更新页面状态
					this.avatarUrl = userInfo.avatar || userInfo.avatarUrl || '';
					this.nickName = userInfo.nickname || userInfo.nickName || '';
					this.isLogged = true;
					
					// 同步更新App全局状态
					const app = getApp();
					if (app && app.globalData) {
						app.globalData.isLoggedIn = true;
						app.globalData.userInfo = userInfo;
					}
					
					return true;
				} else {
					console.log("刷新状态: 未找到有效的登录信息");
					return false;
				}
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
	
	/* 登录模态框样式 */
	.login-modal {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		z-index: 999;
	}
	
	.modal-mask {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0,0,0,0.5);
		backdrop-filter: blur(5px);
	}
	
	.modal-content {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		background-color: #fff;
		border-top-left-radius: 30rpx;
		border-top-right-radius: 30rpx;
		overflow: hidden;
		transform: translateY(0);
		animation: slideUp 0.3s ease;
	}
	
	@keyframes slideUp {
		from { transform: translateY(100%); }
		to { transform: translateY(0); }
	}
	
	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 30rpx;
		border-bottom: 1px solid rgba(0,0,0,0.05);
	}
	
	.modal-title {
		font-size: 34rpx;
		font-weight: bold;
		color: #333;
	}
	
	.close-btn {
		width: 60rpx;
		height: 60rpx;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 50%;
	}
	
	.modal-body {
		padding: 50rpx;
		display: flex;
		flex-direction: column;
		align-items: center;
	}
	
	.wechat-logo {
		width: 120rpx;
		height: 120rpx;
		margin-bottom: 30rpx;
	}
	
	.modal-tips {
		font-size: 28rpx;
		color: #666;
		margin-bottom: 50rpx;
		text-align: center;
	}
	
	.auth-button {
		width: 80%;
		height: 80rpx;
		line-height: 80rpx;
		background: #07C160;
		color: #fff;
		font-size: 30rpx;
		border-radius: 40rpx;
		margin-bottom: 30rpx;
	}

	.profile-form {
		width: 100%;
		text-align: center;
	}

	.form-title {
		font-size: 36rpx;
		font-weight: bold;
		color: #333;
		margin-bottom: 30rpx;
	}

	.avatar-wrapper {
		width: 200rpx;
		height: 200rpx;
		border-radius: 50%;
		margin: 0 auto 30rpx;
		position: relative;
		overflow: hidden;
		background-color: #f0f0f0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		border: none;
	}

	.avatar-wrapper::after {
		border: none;
	}

	.avatar-preview {
		width: 200rpx;
		height: 200rpx;
		border-radius: 50%;
	}

	.avatar-tip {
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		background: rgba(0,0,0,0.5);
		color: #fff;
		font-size: 22rpx;
		padding: 8rpx 0;
		text-align: center;
	}

	.nickname-wrapper {
		margin: 30rpx 0;
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.label {
		font-size: 28rpx;
		color: #333;
		margin-bottom: 20rpx;
		font-weight: bold;
	}

	.nickname-input {
		width: 80%;
		height: 80rpx;
		border: 1px solid #eee;
		border-radius: 40rpx;
		padding: 0 30rpx;
		font-size: 28rpx;
		background: #f8f8f8;
	}

	.save-button {
		width: 80%;
		height: 80rpx;
		line-height: 80rpx;
		background: #07C160;
		color: #fff;
		font-size: 30rpx;
		border-radius: 40rpx;
		margin-top: 20rpx;
		margin-bottom: 0;
	}
	
	.save-button:active {
		opacity: 0.8;
	}
</style>