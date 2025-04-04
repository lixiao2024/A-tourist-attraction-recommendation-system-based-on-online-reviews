<template>
  <view class="footprint-container">
    <!-- 统计信息面板 -->
    <view class="stats-panel">
      <view class="stats-item">
        <text class="stats-label">已探索城市</text>
        <text class="stats-value">{{stats.visitedCount}}</text>
      </view>
      <view class="stats-item">
        <text class="stats-label">覆盖率</text>
        <text class="stats-value">{{stats.chinaRate}}</text>
      </view>
    </view>

    <!-- 地图容器 -->
    <view class="map-container">
      <!-- 使用image组件显示SVG -->
      <image 
        src="./china.svg" 
        class="china-map-svg"
        :style="{ width: '100%', height: '100%' }"
        mode="aspectFit"
      ></image>
      
      <!-- 地图标记点 -->
      <view 
        v-for="(city, index) in cityMarkers" 
        :key="index" 
        class="city-marker"
        :class="{ 'visited': city.visited }"
        :style="{ left: city.x + '%', top: city.y + '%' }"
        @tap="handleMarkerTap(city)"
      >
        <view class="marker-point"></view>
        <text class="marker-label">{{ city.name }}</text>
      </view>
    </view>
    
    <!-- 添加当前位置按钮 -->
    <view class="add-location-btn" @click="getUserLocation">
      <uni-icons type="location" size="20" color="#fff"></uni-icons>
      <text>添加当前位置</text>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 城市标记点位置数据
      cityMarkers: [
        { name: '北京', x: 65, y: 25, visited: false },
        { name: '上海', x: 78, y: 40, visited: false },
        { name: '广州', x: 65, y: 70, visited: false },
        { name: '深圳', x: 67, y: 73, visited: false },
        { name: '杭州', x: 75, y: 43, visited: false },
        { name: '南京', x: 72, y: 40, visited: false },
        { name: '成都', x: 45, y: 55, visited: false },
        { name: '重庆', x: 50, y: 58, visited: false },
        { name: '西安', x: 55, y: 42, visited: false },
        { name: '武汉', x: 63, y: 50, visited: false },
        { name: '长沙', x: 60, y: 58, visited: false },
        { name: '郑州', x: 62, y: 40, visited: false },
        { name: '哈尔滨', x: 75, y: 12, visited: false },
        { name: '沈阳', x: 73, y: 20, visited: false },
        { name: '天津', x: 67, y: 27, visited: false },
        { name: '青岛', x: 73, y: 35, visited: false },
        { name: '大连', x: 72, y: 25, visited: false },
        { name: '厦门', x: 70, y: 65, visited: false },
        { name: '昆明', x: 45, y: 70, visited: false },
        { name: '拉萨', x: 30, y: 60, visited: false },
        { name: '乌鲁木齐', x: 20, y: 26, visited: false },
        { name: '兰州', x: 45, y: 38, visited: false }
      ],
      visitedCities: [],
      footprintData: {
        cities: {}
      },
      stats: {
        visitedCount: 0,
        chinaRate: '0%'
      },
      isLoading: false
    }
  },
  
  onLoad() {
    // 从本地存储加载足迹数据
    const savedData = uni.getStorageSync('footprint_data');
    if (savedData) {
      try {
        this.footprintData = JSON.parse(savedData);
        this.updateVisitedCities();
      } catch (e) {
        console.error('解析足迹数据失败:', e);
      }
    }
  },
  
  onReady() {
    // 更新地图标记点状态
    this.updateMapMarkers();
  },
  
  methods: {
    // 更新地图标记状态
    updateMapMarkers() {
      // 遍历城市标记点，更新已访问状态
      this.cityMarkers.forEach(marker => {
        marker.visited = !!this.footprintData.cities[marker.name];
      });
    },

    // 处理标记点点击
    handleMarkerTap(city) {
      // 显示城市信息
      if (city.visited) {
        const visitData = this.footprintData.cities[city.name];
        uni.showModal({
          title: `${city.name}足迹`,
          content: `您已到访${city.name}${visitData.visitCount}次\n首次到访: ${visitData.firstVisit}`,
          showCancel: false
        });
      } else {
        // 询问是否添加足迹
        uni.showModal({
          title: '添加足迹',
          content: `是否将${city.name}添加到您的足迹中？`,
          success: (res) => {
            if (res.confirm) {
              this.addVisitedCity(city.name);
            }
          }
        });
      }
    },
    
    // 更新访问城市列表
    updateVisitedCities() {
      this.visitedCities = [];
      
      // 从足迹数据中更新访问城市列表
      for (const cityName in this.footprintData.cities) {
        const cityData = this.footprintData.cities[cityName];
        this.visitedCities.push({
          name: cityName,
          value: cityData.visitCount
        });
      }
      
      // 更新地图标记点状态
      this.updateMapMarkers();
      
      // 更新统计信息
      this.updateStats();
    },
    
    // 更新统计信息
    updateStats() {
      // 计算已访问城市数量
      const visitedCount = Object.keys(this.footprintData.cities).length;
      
      // 中国大陆城市数量(简化计算)
      const totalChinaRegions = this.cityMarkers.length;
      
      // 计算覆盖率
      const chinaRate = ((visitedCount / totalChinaRegions) * 100).toFixed(1);
      
      // 更新统计信息
      this.stats = {
        visitedCount: visitedCount,
        chinaRate: chinaRate + '%'
      };
    },
    
    // 获取用户当前位置
    getUserLocation() {
      if (this.isLoading) return;
      
      this.isLoading = true;
      uni.showLoading({
        title: '获取位置信息...'
      });
      
      uni.getFuzzyLocation({
        type: 'wgs84',
        success: (res) => {
          uni.hideLoading();
          console.log('获取模糊位置成功:', res);
          
          // 经纬度反向解析为地址
          this.getAddressFromLocation(res.latitude, res.longitude);
        },
        fail: (err) => {
          this.isLoading = false;
          uni.hideLoading();
          console.error('获取位置失败:', err);
          this.showManualInputDialog();
        }
      });
    },
    
    // 使用经纬度反向解析地址
    getAddressFromLocation(latitude, longitude) {
      uni.showLoading({
        title: '解析位置信息...'
      });
      
      uni.request({
        url: `https://apis.map.qq.com/ws/geocoder/v1/?key=KNLBZ-GNUKT-L6DXC-VRGBS-5G3IF-TVBN7&location=${latitude},${longitude}`,
        success: (res) => {
          this.isLoading = false;
          uni.hideLoading();
          if (res.statusCode === 200 && res.data && res.data.result) {
            const cityName = res.data.result.address_component.city;
            if (cityName) {
              uni.showModal({
                title: '添加足迹',
                content: `检测到您当前位于 ${cityName}，是否添加到足迹？`,
                success: (modalRes) => {
                  if (modalRes.confirm) {
                    this.addVisitedCity(cityName);
                    uni.showToast({
                      title: `已添加${cityName}到足迹`,
                      icon: 'success'
                    });
                  }
                }
              });
            } else {
              this.showManualInputDialog();
            }
          } else {
            console.error('地址解析失败:', res);
            this.showManualInputDialog();
          }
        },
        fail: (err) => {
          this.isLoading = false;
          uni.hideLoading();
          console.error('地址解析请求失败:', err);
          this.showManualInputDialog();
        }
      });
    },
    
    // 显示手动输入对话框
    showManualInputDialog() {
      uni.showModal({
        title: '添加足迹',
        content: '无法自动获取位置，请手动输入您想要添加的城市名称',
        editable: true,
        placeholderText: '例如：北京',
        success: (modalRes) => {
          if (modalRes.confirm && modalRes.content) {
            const cityName = modalRes.content;
            this.addVisitedCity(cityName);
            uni.showToast({
              title: `已添加${cityName}到足迹`,
              icon: 'success'
            });
          }
        }
      });
    },
    
    // 添加已访问城市
    addVisitedCity(cityName) {
      if (!cityName) return;
      
      // 去掉可能存在的"市"字
      const cleanCityName = cityName.replace('市', '');
      
      // 检查是否已经存在该城市
      if (this.footprintData.cities[cleanCityName]) {
        // 已存在，增加访问次数
        this.footprintData.cities[cleanCityName].visitCount++;
      } else {
        // 新城市，添加记录
        this.footprintData.cities[cleanCityName] = {
          visitCount: 1,
          firstVisit: new Date().toISOString().split('T')[0]
        };
      }
      
      // 保存数据并刷新地图
      this.saveFootprintData();
      this.updateVisitedCities();
    },
    
    // 保存足迹数据
    saveFootprintData() {
      try {
        uni.setStorageSync('footprint_data', JSON.stringify(this.footprintData));
      } catch (e) {
        console.error('保存足迹数据失败:', e);
      }
    }
  }
}
</script>

<style lang="scss">
.footprint-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
}

.stats-panel {
  display: flex;
  justify-content: space-around;
  padding: 15px;
  background: #fff;
  border-bottom: 1px solid #eee;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  
  .stats-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    
    .stats-label {
      font-size: 12px;
      color: #666;
      margin-bottom: 5px;
    }
    
    .stats-value {
      font-size: 18px;
      font-weight: bold;
      color: #333;
    }
  }
}

.map-container {
  flex: 1;
  width: 100%;
  position: relative;
  background: #fff;
  overflow: hidden;
  
  .china-map-svg {
    display: block;
  }
  
  .city-marker {
    position: absolute;
    transform: translate(-50%, -50%);
    
    .marker-point {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: #ccc;
      border: 1px solid #fff;
      box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
      margin: 0 auto;
      transition: all 0.3s;
    }
    
    .marker-label {
      font-size: 10px;
      color: #666;
      white-space: nowrap;
      text-align: center;
      display: block;
      margin-top: 2px;
      opacity: 0.8;
    }
    
    &.visited {
      .marker-point {
        width: 12px;
        height: 12px;
        background-color: #2C85BE;
      }
      
      .marker-label {
        color: #2C85BE;
        font-weight: bold;
        opacity: 1;
      }
    }
    
    &:active {
      .marker-point {
        transform: scale(1.2);
      }
    }
  }
}

.add-location-btn {
  position: fixed;
  right: 20px;
  bottom: 30px;
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background: #2C85BE;
  color: #fff;
  border-radius: 30px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  z-index: 100;
  
  text {
    margin-left: 5px;
    font-size: 14px;
  }
}
</style>
