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
					image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', 
					value: '北京',
					attractions: [
						{ name: '故宫博物院', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '故宫博物院' },
						{ name: '天安门广场', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '天安门广场' },
						{ name: '长城', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '长城' },
						{ name: '颐和园', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '颐和园' },
						{ name: '天坛公园', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '天坛公园' },
						{ name: '圆明园遗址公园', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '圆明园遗址公园' },
						{ name: '北海公园', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '北海公园' },
						{ name: '什刹海', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '什刹海' }
					]
				},
				{ 
					name: '上海', 
					image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', 
					value: '上海',
					attractions: [
						{ name: '外滩', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '外滩' },
						{ name: '东方明珠', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '东方明珠' },
						{ name: '豫园', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '豫园' },
						{ name: '南京路步行街', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '南京路步行街' },
						{ name: '上海博物馆', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '上海博物馆' },
						{ name: '田子坊', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '田子坊' },
						{ name: '上海环球金融中心', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '上海环球金融中心' },
						{ name: '上海迪士尼乐园', image: 'https://dimg04.c-ctrip.com/images/0101h120008a6c29o86BC5_C_378_245.jpg', selected: false, value: '上海迪士尼乐园' }
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
				
				// 返回上一页
				setTimeout(() => {
					uni.navigateBack();
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
		padding: 30rpx;
		background-color: #f8f9fa;
		min-height: 100vh;
	}
	
	.header {
		margin-bottom: 40rpx;
		
		.title {
			font-size: 36rpx;
			font-weight: 600;
			color: #333;
			display: block;
			margin-bottom: 10rpx;
		}
		
		.subtitle {
			font-size: 28rpx;
			color: #666;
		}
	}
	
	.section {
		margin-bottom: 40rpx;
		
		.section-title {
			font-size: 32rpx;
			font-weight: 500;
			color: #333;
			margin-bottom: 20rpx;
			display: block;
		}
	}
	
	.city-list {
		display: flex;
		flex-direction: column;
		gap: 20rpx;
	}
	
	.city-item {
		display: flex;
		align-items: center;
		background-color: #fff;
		border-radius: 12rpx;
		overflow: hidden;
		position: relative;
		box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
		
		&.selected {
			border: 2rpx solid #3182ce;
			
			.check-icon {
				display: flex;
			}
		}
		
		.city-image {
			width: 120rpx;
			height: 120rpx;
			flex-shrink: 0;
		}
		
		.city-info {
			flex: 1;
			padding: 20rpx;
		}
		
		.city-name {
			font-size: 32rpx;
			font-weight: 500;
			color: #333;
		}
		
		.check-icon {
			position: absolute;
			top: 10rpx;
			right: 10rpx;
			width: 40rpx;
			height: 40rpx;
			background-color: #3182ce;
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			display: none;
		}
	}
	
	.tags-list {
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: 20rpx;
	}
	
	.tag-item {
		background-color: #fff;
		border-radius: 12rpx;
		overflow: hidden;
		position: relative;
		box-shadow: 0 2rpx 10rpx rgba(0,0,0,0.05);
		
		&.selected {
			border: 2rpx solid #3182ce;
			
			.check-icon {
				display: flex;
			}
		}
		
		.tag-image {
			width: 100%;
			height: 180rpx;
		}
		
		.tag-info {
			padding: 16rpx;
		}
		
		.tag-name {
			font-size: 28rpx;
			color: #333;
			display: block;
			white-space: nowrap;
			overflow: hidden;
			text-overflow: ellipsis;
		}
		
		.check-icon {
			position: absolute;
			top: 10rpx;
			right: 10rpx;
			width: 40rpx;
			height: 40rpx;
			background-color: #3182ce;
			border-radius: 50%;
			display: flex;
			align-items: center;
			justify-content: center;
			display: none;
		}
	}
	
	.button-container {
		margin-top: 60rpx;
		padding: 0 30rpx;
	}
	
	.save-button {
		background: linear-gradient(135deg, #3182ce, #005bb5);
		color: #fff;
		border-radius: 40rpx;
		font-size: 32rpx;
		font-weight: 500;
		padding: 20rpx 0;
		text-align: center;
		box-shadow: 0 4rpx 12rpx rgba(49,130,206,0.3);
		
		&:active {
			transform: scale(0.98);
		}
		
		&[disabled] {
			background: #ccc;
			box-shadow: none;
		}
	}
</style> 