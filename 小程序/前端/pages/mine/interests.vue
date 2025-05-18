<template>
	<view class="interests-container">
		<view class="header">
			<text class="title">选择您感兴趣的城市和景点</text>
			<text class="subtitle">这将帮助我们为您推荐更符合您兴趣的旅游景点</text>
		</view>
		
		<!-- 城市选择区域 -->
		<view class="section">
			<text class="section-title">选择您所在的城市</text>
			<view class="city-list">
				<view 
					v-for="(city, index) in cities" 
					:key="index"
					:class="['city-item', selectedCity === city.value ? 'selected' : '']"
					@click="selectCity(city.value)"
				>
					<image :src="city.image" mode="aspectFill" class="city-image"></image>
					<view class="city-info">
						<text class="city-name">{{ city.name }}</text>
					</view>
					<view class="check-icon" v-if="selectedCity === city.value">
						<uni-icons type="checkmarkempty" size="20" color="#ffffff"></uni-icons>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 景点选择区域 -->
		<view class="section" v-if="selectedCity">
			<text class="section-title">选择您感兴趣的景点</text>
			<view class="tags-list">
				<view 
					v-for="(tag, index) in currentCityAttractions" 
					:key="index"
					:class="['tag-item', tag.selected ? 'selected' : '']"
					@click="toggleTag(index)"
				>
					<image :src="tag.image" mode="aspectFill" class="tag-image"></image>
					<view class="tag-info">
						<text class="tag-name">{{ tag.name }}</text>
					</view>
					<view class="check-icon" v-if="tag.selected">
						<uni-icons type="checkmarkempty" size="20" color="#ffffff"></uni-icons>
					</view>
				</view>
			</view>
		</view>
		
		<!-- 保存按钮 -->
		<view class="button-container">
			<button 
				class="save-button" 
				:disabled="!selectedCity || !hasSelectedAttractions"
				@click="saveInterests"
			>
				保存
			</button>
		</view>
	</view>
</template>

<script>
import { updateUserInterests } from '@/request/api.js';

export default {
	data() {
		return {
			selectedCity: '',
			cities: [
				{ 
					name: '成都', 
					image: 'https://dimg04.c-ctrip.com/images/0105p12000f6scno87BC5_C_378_245.jpg', 
					value: '成都',
					attractions: [
						{ name: '成都大熊猫繁育研究基地', image: 'https://dimg04.c-ctrip.com/images/0105p12000f6scno87BC5_C_378_245.jpg', selected: false, value: '成都大熊猫繁育研究基地' },
						{ name: '都江堰景区', image: 'https://dimg04.c-ctrip.com/images/100g0z000000nd29yD334_C_378_245.jpg', selected: false, value: '都江堰景区' },
						{ name: '杜甫草堂', image: 'https://dimg04.c-ctrip.com/images/0104712000f6pqdbe0C80_C_378_245.jpg', selected: false, value: '杜甫草堂' },
						{ name: '武侯祠', image: 'https://dimg04.c-ctrip.com/images/0103n12000f6trha712AE_C_378_245.jpg', selected: false, value: '武侯祠' },
						{ name: '青城山', image: 'https://dimg04.c-ctrip.com/images/0103t1200087ctezh5DC1_C_378_245.jpg', selected: false, value: '青城山' },
						{ name: '金沙遗址博物馆', image: 'https://dimg04.c-ctrip.com/images/0103l12000hxop2usDC88_C_378_245.jpg', selected: false, value: '金沙遗址博物馆' },
						{ name: '成都博物馆', image: 'https://dimg04.c-ctrip.com/images/350j1c000001cpign4A54_C_220_140.jpg', selected: false, value: '成都博物馆' },
						{ name: '文殊坊', image: 'https://dimg04.c-ctrip.com/images/1lo3s12000cndjrd45EF0_C_220_140.jpg', selected: false, value: '文殊坊' }
					]
				},
				{ 
					name: '北京', 
					image: 'https://dimg04.c-ctrip.com/images/100a0g00000087qb8E7CE_C_1180_462.jpg', 
					value: '北京',
					attractions: [
						{ name: '故宫博物院', image: 'https://dimg04.c-ctrip.com/images/0100j1200046x94ebB936_C_378_245.jpg', selected: false, value: '故宫博物院' },
						{ name: '北京环球度假区', image: 'https://dimg04.c-ctrip.com/images/1lo2v12000j5bz7ao10B6_C_378_245.jpg', selected: false, value: '北京环球度假区' },
						{ name: '八达岭长城', image: 'https://dimg04.c-ctrip.com/images/1lo2v12000j5bz7ao10B6_C_378_245.jpg', selected: false, value: '八达岭长城' },
						{ name: '颐和园', image: '	https://dimg04.c-ctrip.com/images/10010p000000ftdk87BDF_C_378_245.jpg', selected: false, value: '颐和园' },
						{ name: '天坛公园', image: 'https://dimg04.c-ctrip.com/images/10040h0000008s9n50143_C_220_140.jpg', selected: false, value: '天坛公园' },
						{ name: '圆明园', image: 'https://dimg04.c-ctrip.com/images/010131200046ybzogE113_C_220_140.jpg', selected: false, value: '圆明园' },
						{ name: '中国国家博物馆', image: 'https://dimg04.c-ctrip.com/images/0102y12000hxkc5n61AF4_C_378_245.jpg', selected: false, value: '中国国家博物馆' },
						{ name: '恭王府', image: 'https://dimg04.c-ctrip.com/images/010261200087dxb2445A6_C_378_245.jpg', selected: false, value: '恭王府' },
						{ name: '北京野生动物园', image: 'https://dimg04.c-ctrip.com/images/10030c00000063u6rBDAE_C_220_140.jpg', selected: false, value: '北京野生动物园' },
						{ name: '慕田峪长城', image: 'https://dimg04.c-ctrip.com/images/1lo0m12000bjgo0zjBC35_C_220_140.jpg', selected: false, value: '慕田峪长城' }
					]
				},
				{ 
					name: '上海', 
					image: 'https://dimg04.c-ctrip.com/images/100e0h0000008rp39A12F_C_1180_462.jpg', 
					value: '上海',
					attractions: [
						{ name: '外滩', image: 'https://dimg04.c-ctrip.com/images/10040m000000dht6p0F19_C_220_140.jpg', selected: false, value: '外滩' },
						{ name: '东方明珠', image: 'https://dimg04.c-ctrip.com/images/1lo7412000isn0jrbD500_C_220_140.jpg', selected: false, value: '东方明珠' },
						{ name: '豫园', image: 'https://dimg04.c-ctrip.com/images/0103v12000f9ug057967E_C_220_140.jpg', selected: false, value: '豫园' },
						{ name: '南京路步行街', image: 'https://dimg04.c-ctrip.com/images/0106u120008c3zeiy8417_C_220_140.jpg', selected: false, value: '南京路步行街' },
						{ name: '上海博物馆', image: 'https://dimg04.c-ctrip.com/images/0103x1200042pw7745DC1_C_220_140.jpg', selected: false, value: '上海博物馆' },
						{ name: '上海野生动物园', image: 'https://dimg04.c-ctrip.com/images/1lo6912000jox1tqr381E_C_220_140.jpg', selected: false, value: '上海野生动物园' },
						{ name: '上海迪士尼度假区', image: 'https://dimg04.c-ctrip.com/images/1lo4f12000iudih1251F7_C_220_140.jpg', selected: false, value: '上海迪士尼度假区' },
						{ name: '上海海昌海洋公园', image: 'https://dimg04.c-ctrip.com/images/1lo6f12000jfw8aic86E9_C_220_140.jpg', selected: false, value: '上海海昌海洋公园' }
					]
				}
			],
			currentCityAttractions: []
		}
	},
	computed: {
		hasSelectedAttractions() {
			return this.currentCityAttractions.some(tag => tag.selected);
		}
	},
	onLoad() {
		// 尝试从本地存储加载已保存的兴趣标签
		const savedInterests = uni.getStorageSync('userInterests');
		if (savedInterests) {
			try {
				const interests = JSON.parse(savedInterests);
				if (interests.city) {
					this.selectedCity = interests.city;
					// 找到对应城市的景点
					const cityData = this.cities.find(city => city.value === interests.city);
					if (cityData) {
						this.currentCityAttractions = [...cityData.attractions];
						// 标记已选择的景点
						if (interests.attractions && interests.attractions.length > 0) {
							interests.attractions.forEach(attraction => {
								const index = this.currentCityAttractions.findIndex(tag => tag.value === attraction);
								if (index !== -1) {
									this.currentCityAttractions[index].selected = true;
								}
							});
						}
					}
				}
			} catch (e) {
				console.error('解析保存的兴趣标签失败:', e);
			}
		}
	},
	methods: {
		selectCity(cityValue) {
			this.selectedCity = cityValue;
			// 找到对应城市的景点
			const cityData = this.cities.find(city => city.value === cityValue);
			if (cityData) {
				this.currentCityAttractions = [...cityData.attractions];
			}
		},
		toggleTag(index) {
			this.currentCityAttractions[index].selected = !this.currentCityAttractions[index].selected;
		},
		async saveInterests() {
			if (!this.selectedCity) {
				uni.showToast({
					title: '请选择城市',
					icon: 'none'
				});
				return;
			}
			
			if (!this.hasSelectedAttractions) {
				uni.showToast({
					title: '请至少选择一个景点',
					icon: 'none'
				});
				return;
			}
			
			// 获取选中的景点
			const selectedAttractions = this.currentCityAttractions
				.filter(tag => tag.selected)
				.map(tag => tag.value);
			
			// 构建兴趣标签数据
			const interestsData = {
				city: this.selectedCity,
				attractions: selectedAttractions
			};
			
			// 保存到本地存储
			uni.setStorageSync('userInterests', JSON.stringify(interestsData));
			
			// 构建API请求数据
			const apiData = {
				tags: JSON.stringify(interestsData)
			};
			
			try {
				uni.showLoading({
					title: '保存中...'
				});
				
				await updateUserInterests(apiData);
				
				uni.hideLoading();
				uni.showToast({
					title: '保存成功',
					icon: 'success'
				});
				
				// 检查当前页面栈深度，决定导航方式
				setTimeout(() => {
					const pages = getCurrentPages();
					if (pages.length > 1) {
						// 如果不是第一个页面，则可以返回
						uni.navigateBack();
					} else {
						// 如果是第一个页面，则跳转到首页
						uni.switchTab({
							url: '/pages/index/index'
						});
					}
				}, 1500);
			} catch (error) {
				uni.hideLoading();
				uni.showToast({
					title: '保存失败，请重试',
					icon: 'none'
				});
				console.error('保存兴趣标签失败:', error);
			}
		}
	}
}
</script>

<style lang="scss">
	.interests-container {
		padding: 40rpx 30rpx;
		background-color: #f8f9fa;
		min-height: 100vh;
	}
	
	.header {
		margin-bottom: 50rpx;
		text-align: center;
		
		.title {
			font-size: 40rpx;
			font-weight: 600;
			color: #333;
			display: block;
			margin-bottom: 16rpx;
			letter-spacing: 2rpx;
		}
		
		.subtitle {
			font-size: 28rpx;
			color: #666;
			line-height: 1.5;
		}
	}
	
	.section {
		margin-bottom: 50rpx;
		background-color: transparent;
		border-radius: 20rpx;
		padding: 10rpx;
		
		.section-title {
			font-size: 32rpx;
			font-weight: 500;
			color: #333;
			margin-bottom: 30rpx;
			display: block;
			position: relative;
			padding-left: 20rpx;
			
			&::before {
				content: '';
				position: absolute;
				left: 0;
				top: 50%;
				transform: translateY(-50%);
				width: 8rpx;
				height: 32rpx;
				background: linear-gradient(135deg, #3182ce, #5a9de6);
				border-radius: 4rpx;
			}
		}
	}
	
	.city-list {
		display: flex;
		flex-direction: column;
		gap: 24rpx;
	}
	
	.city-item {
		display: flex;
		align-items: center;
		background-color: #fff;
		border-radius: 16rpx;
		overflow: hidden;
		position: relative;
		box-shadow: 0 8rpx 20rpx rgba(0,0,0,0.06);
		padding: 6rpx;
		transition: all 0.3s ease;
		
		&.selected {
			border: 2rpx solid #3182ce;
			transform: translateY(-4rpx);
			box-shadow: 0 12rpx 24rpx rgba(49,130,206,0.15);
			
			.check-icon {
				display: flex;
			}
			
			.city-info {
				.city-name {
					color: #3182ce;
				}
			}
		}
		
		&:active {
			transform: scale(0.98);
		}
		
		.city-image {
			width: 140rpx;
			height: 140rpx;
			flex-shrink: 0;
			border-radius: 12rpx;
			object-fit: cover;
		}
		
		.city-info {
			flex: 1;
			padding: 20rpx 30rpx;
		}
		
		.city-name {
			font-size: 34rpx;
			font-weight: 500;
			color: #333;
			transition: color 0.3s ease;
		}
		
		.check-icon {
			position: absolute;
			top: 16rpx;
			right: 16rpx;
			width: 44rpx;
			height: 44rpx;
			background-color: #3182ce;
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			display: none;
			box-shadow: 0 4rpx 8rpx rgba(49,130,206,0.3);
			animation: scaleIn 0.2s ease-out;
		}
	}
	
	.tags-list {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 24rpx;
	}
	
	.tag-item {
		background-color: #fff;
		border-radius: 16rpx;
		overflow: hidden;
		position: relative;
		box-shadow: 0 8rpx 20rpx rgba(0,0,0,0.06);
		transition: all 0.3s ease;
		
		&.selected {
			border: 2rpx solid #3182ce;
			transform: translateY(-4rpx);
			box-shadow: 0 12rpx 24rpx rgba(49,130,206,0.15);
			
			.check-icon {
				display: flex;
			}
			
			.tag-info {
				.tag-name {
					color: #3182ce;
				}
			}
		}
		
		&:active {
			transform: scale(0.98);
		}
		
		.tag-image {
			width: 100%;
			height: 200rpx;
			object-fit: cover;
		}
		
		.tag-info {
			padding: 20rpx;
		}
		
		.tag-name {
			font-size: 28rpx;
			font-weight: 500;
			color: #333;
			display: block;
			text-align: center;
			white-space: nowrap;
			overflow: hidden;
			text-overflow: ellipsis;
			transition: color 0.3s ease;
		}
		
		.check-icon {
			position: absolute;
			top: 16rpx;
			right: 16rpx;
			width: 44rpx;
			height: 44rpx;
			background-color: #3182ce;
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			display: none;
			box-shadow: 0 4rpx 8rpx rgba(49,130,206,0.3);
			animation: scaleIn 0.2s ease-out;
		}
	}
	
	.button-container {
		margin-top: 80rpx;
		padding: 0 40rpx;
	}
	
	.save-button {
		background: linear-gradient(135deg, #3182ce, #1b5ea3);
		color: #fff;
		border-radius: 50rpx;
		font-size: 34rpx;
		font-weight: 600;
		padding: 25rpx 0;
		text-align: center;
		box-shadow: 0 10rpx 20rpx rgba(49,130,206,0.3);
		letter-spacing: 4rpx;
		transition: all 0.3s ease;
		
		&:active {
			transform: scale(0.97);
			box-shadow: 0 5rpx 10rpx rgba(49,130,206,0.2);
		}
		
		&[disabled] {
			background: linear-gradient(135deg, #b8c2cc, #97a6b6);
			box-shadow: none;
			opacity: 0.8;
		}
	}
	
	@keyframes scaleIn {
		0% {
			transform: scale(0);
		}
		80% {
			transform: scale(1.2);
		}
		100% {
			transform: scale(1);
		}
	}
</style> 