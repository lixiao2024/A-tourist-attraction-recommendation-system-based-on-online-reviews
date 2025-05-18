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
    <view 
      class="map-container" 
      @touchstart="touchStart"
      @touchmove="touchMove"
      @touchend="touchEnd"
    >
      <!-- 使用image组件显示SVG -->
      <view 
        class="map-wrapper"
        :style="{
          transform: `scale(${scale}) translate(${translateX}px, ${translateY}px)`,
          transformOrigin: '50% 50%'
        }"
      >
        <image 
          src="/static/footprint/china1.svg" 
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
          :style="{ 
            left: city.x + '%', 
            top: city.y + '%',
            transform: `translate(-50%, -50%) scale(${1/scale})`
          }"
          @tap="handleMarkerTap(city)"
        >
          <view class="marker-point"></view>
          <text class="marker-label">{{ city.name }}</text>
        </view>
      </view>
    </view>
    
    <!-- 添加当前位置按钮 -->
    <view class="add-location-btn" @click="getUserLocation">
      <uni-icons type="location" size="20" color="#fff"></uni-icons>
      <text>添加当前位置</text>
    </view>
    
    <!-- 地图控制按钮 -->
    <view class="map-controls">
      <view class="control-btn" @tap="zoomIn">
        <text class="zoom-icon">+</text>
      </view>
      <view class="control-btn" @tap="zoomOut">
        <text class="zoom-icon">-</text>
      </view>
      <view class="control-btn" @tap="resetMap">
        <text class="zoom-icon">⟲</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      // 城市标记点位置数据
      cityMarkers: [
        { name: '北京', x: 64, y: 35, visited: false },
        { name: '上海', x: 70, y: 48, visited: false },
        { name: '广州', x: 60, y: 58, visited: false },
        { name: '深圳', x: 61, y: 59, visited: false },
        { name: '杭州', x: 68, y: 49, visited: false },
        { name: '南京', x: 67, y: 46, visited: false },
        { name: '成都', x: 48, y: 48, visited: false },
        { name: '重庆', x: 53, y: 49, visited: false },
        { name: '西安', x: 55, y: 44, visited: false },
        { name: '武汉', x: 61, y: 48, visited: false },
        { name: '长沙', x: 59, y: 51, visited: false },
        { name: '郑州', x: 61, y: 45, visited: false },
        { name: '哈尔滨', x: 75, y: 29, visited: false },
        { name: '沈阳', x: 72, y: 34, visited: false },
        { name: '天津', x: 65, y: 37, visited: false },
        { name: '青岛', x: 70, y: 40, visited: false },
        { name: '大连', x: 70, y: 37, visited: false },
        { name: '厦门', x: 66, y: 56, visited: false },
        { name: '昆明', x: 47, y: 55, visited: false },
        { name: '拉萨', x: 34, y: 50, visited: false },
        { name: '乌鲁木齐', x: 29, y: 32, visited: false },
        { name: '兰州', x: 50, y: 43, visited: false }
      ],
      visitedCities: [],
      footprintData: {
        cities: {}
      },
      stats: {
        visitedCount: 0,
        chinaRate: '0%'
      },
      isLoading: false,
      // 地图缩放和平移相关数据
      scale: 1,
      minScale: 0.8,
      maxScale: 3,
      translateX: 0,
      translateY: 0,
      lastDistance: 0,
      lastTouchX: 0,
      lastTouchY: 0,
      touches: [],
      isDragging: false
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
          this.isLoading = false;
          uni.hideLoading();
          console.log('获取模糊位置成功:', res);
          
          // 使用经纬度估算最近的城市
          const nearestCity = this.findNearestCity(res.latitude, res.longitude);
          if (nearestCity) {
            uni.showModal({
              title: '添加足迹',
              content: `根据您的位置信息，您可能位于${nearestCity.name}附近，是否添加到足迹？`,
              success: (modalRes) => {
                if (modalRes.confirm) {
                  this.addVisitedCity(nearestCity.name);
                  uni.showToast({
                    title: `已添加${nearestCity.name}到足迹`,
                    icon: 'success'
                  });
                }
              }
            });
          } else {
            this.showManualInputDialog();
          }
        },
        fail: (err) => {
          this.isLoading = false;
          uni.hideLoading();
          console.error('获取位置失败:', err);
          this.showManualInputDialog();
        }
      });
    },
    
    // 根据经纬度找到最近的城市
    findNearestCity(latitude, longitude) {
      // 中国主要城市的大致经纬度
      const cityCoordinates = [
        { name: '北京', lat: 39.90, lng: 116.40 },
        { name: '上海', lat: 31.23, lng: 121.47 },
        { name: '广州', lat: 23.13, lng: 113.27 },
        { name: '深圳', lat: 22.54, lng: 114.06 },
        { name: '杭州', lat: 30.26, lng: 120.19 },
        { name: '南京', lat: 32.06, lng: 118.78 },
        { name: '成都', lat: 30.67, lng: 104.06 },
        { name: '重庆', lat: 29.56, lng: 106.55 },
        { name: '西安', lat: 34.34, lng: 108.94 },
        { name: '武汉', lat: 30.59, lng: 114.31 },
        { name: '长沙', lat: 28.21, lng: 112.97 },
        { name: '郑州', lat: 34.75, lng: 113.62 },
        { name: '哈尔滨', lat: 45.80, lng: 126.53 },
        { name: '沈阳', lat: 41.80, lng: 123.43 },
        { name: '天津', lat: 39.12, lng: 117.20 },
        { name: '青岛', lat: 36.10, lng: 120.38 },
        { name: '大连', lat: 38.91, lng: 121.61 },
        { name: '厦门', lat: 24.48, lng: 118.08 },
        { name: '昆明', lat: 25.05, lng: 102.70 },
        { name: '拉萨', lat: 29.65, lng: 91.10 },
        { name: '乌鲁木齐', lat: 43.82, lng: 87.62 },
        { name: '兰州', lat: 36.06, lng: 103.83 }
      ];
      
      let nearestCity = null;
      let minDistance = Number.MAX_VALUE;
      
      // 计算和每个城市的距离
      for (const city of cityCoordinates) {
        const distance = this.calculateDistance(latitude, longitude, city.lat, city.lng);
        if (distance < minDistance) {
          minDistance = distance;
          nearestCity = city;
        }
      }
      
      // 如果距离太远(超过300公里)，可能不准确，返回null
      if (minDistance > 300) {
        return null;
      }
      
      return nearestCity;
    },
    
    // 计算两点之间的大致距离(公里)
    calculateDistance(lat1, lon1, lat2, lon2) {
      const R = 6371; // 地球半径，单位公里
      const dLat = this.deg2rad(lat2 - lat1);
      const dLon = this.deg2rad(lon2 - lon1);
      const a = 
        Math.sin(dLat/2) * Math.sin(dLat/2) +
        Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) * 
        Math.sin(dLon/2) * Math.sin(dLon/2); 
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
      const distance = R * c;
      return distance;
    },
    
    // 角度转弧度
    deg2rad(deg) {
      return deg * (Math.PI/180);
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
    },
    
    // 地图缩放和平移相关方法
    touchStart(e) {
      if (e.touches.length === 1) {
        // 单指触摸，准备拖动
        this.lastTouchX = e.touches[0].clientX;
        this.lastTouchY = e.touches[0].clientY;
        this.isDragging = true;
      } else if (e.touches.length === 2) {
        // 双指触摸，准备缩放
        this.lastDistance = this.getDistance(e.touches[0], e.touches[1]);
        this.isDragging = false;
      }
      this.touches = e.touches;
    },
    
    touchMove(e) {
      if (e.touches.length === 1 && this.isDragging) {
        // 单指拖动地图
        const deltaX = e.touches[0].clientX - this.lastTouchX;
        const deltaY = e.touches[0].clientY - this.lastTouchY;
        
        this.translateX += deltaX / this.scale;
        this.translateY += deltaY / this.scale;
        
        this.lastTouchX = e.touches[0].clientX;
        this.lastTouchY = e.touches[0].clientY;
      } else if (e.touches.length === 2) {
        // 双指缩放地图
        const currentDistance = this.getDistance(e.touches[0], e.touches[1]);
        const scaleFactor = currentDistance / this.lastDistance;
        
        if (scaleFactor !== 0) {
          let newScale = this.scale * scaleFactor;
          
          // 限制缩放范围
          newScale = Math.max(this.minScale, Math.min(this.maxScale, newScale));
          
          this.scale = newScale;
          this.lastDistance = currentDistance;
        }
      }
    },
    
    touchEnd(e) {
      this.isDragging = false;
    },
    
    // 计算两点之间的距离
    getDistance(touch1, touch2) {
      const dx = touch1.clientX - touch2.clientX;
      const dy = touch1.clientY - touch2.clientY;
      return Math.sqrt(dx * dx + dy * dy);
    },
    
    // 放大地图
    zoomIn() {
      if (this.scale < this.maxScale) {
        this.scale = Math.min(this.maxScale, this.scale + 0.2);
      }
    },
    
    // 缩小地图
    zoomOut() {
      if (this.scale > this.minScale) {
        this.scale = Math.max(this.minScale, this.scale - 0.2);
      }
    },
    
    // 重置地图
    resetMap() {
      this.scale = 1;
      this.translateX = 0;
      this.translateY = 0;
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
  touch-action: none;
  
  .map-wrapper {
    width: 100%;
    height: 100%;
    position: relative;
    transition: transform 0.05s ease-out;
  }
  
  .china-map-svg {
    display: block;
  }
  
  .city-marker {
    position: absolute;
    
    .marker-point {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background-color: #ccc;
      border: 1px solid #fff;
      box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
      margin: 0 auto;
      transition: all 0.3s;
    }
    
    .marker-label {
      font-size: 6px;
      color: #666;
      white-space: nowrap;
      text-align: center;
      display: block;
      margin-top: 1px;
      opacity: 0.8;
    }
    
    &.visited {
      .marker-point {
        width: 8px;
        height: 8px;
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

.map-controls {
  position: fixed;
  left: 20px;
  bottom: 30px;
  display: flex;
  flex-direction: column;
  z-index: 100;
  
  .control-btn {
    width: 40px;
    height: 40px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    
    .zoom-icon {
      font-size: 24px;
      font-weight: bold;
      color: #333;
    }
    
    &:active {
      background: #f0f0f0;
    }
  }
}
</style>
