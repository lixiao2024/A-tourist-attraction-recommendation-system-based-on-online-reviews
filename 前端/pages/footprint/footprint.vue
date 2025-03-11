<template>
  <view class="footprint-container">
    <!-- 地图切换按钮 -->
    <view class="map-switch">
      <button 
        class="switch-btn" 
        :class="{ active: mapType === 'china' }" 
        @click="switchMap('china')"
      >中国地图</button>
      <button 
        class="switch-btn" 
        :class="{ active: mapType === 'world' }" 
        @click="switchMap('world')"
      >世界地图</button>
    </view>

    <!-- 统计信息面板 -->
    <view class="stats-panel">
      <view class="stats-item">
        <text class="stats-label">已探索城市</text>
        <text class="stats-value">{{stats.visitedCount}}</text>
      </view>
      <view class="stats-item">
        <text class="stats-label">{{mapType === 'china' ? '中国' : '世界'}}覆盖率</text>
        <text class="stats-value">{{mapType === 'china' ? stats.chinaRate : stats.worldRate}}</text>
      </view>
    </view>

    <!-- 地图容器 -->
    <view class="map-container">
      <canvas 
        type="2d"
        id="chinaMap"
        class="map-canvas" 
        :style="{ display: mapType === 'china' ? 'block' : 'none' }"
      ></canvas>
      <canvas 
        type="2d"
        id="worldMap"
        class="map-canvas" 
        :style="{ display: mapType === 'world' ? 'block' : 'none' }"
      ></canvas>
    </view>
    
    <!-- 添加当前位置按钮 -->
    <view class="add-location-btn" @click="getUserLocation">
      <uni-icons type="location" size="20" color="#fff"></uni-icons>
      <text>添加当前位置</text>
    </view>
  </view>
</template>

<script>
// 修改 echarts 导入方式
import * as echarts from '@/js/echarts.js'

// 地图数据
let chinaJson = null;
let worldJson = null;

export default {
  data() {
    return {
      mapType: 'china',
      chinaMap: null,
      worldMap: null,
      visitedCities: [
        { name: '北京', value: 1 },
        { name: '上海', value: 1 },
        { name: '广州', value: 1 }
        // 这里可以根据实际访问数据动态生成
      ],
      // 添加足迹数据对象
      footprintData: {
        cities: {
          '北京': { visitCount: 1, firstVisit: '2023-01-01' },
          '上海': { visitCount: 1, firstVisit: '2023-02-15' },
          '广州': { visitCount: 1, firstVisit: '2023-03-20' }
        }
      },
      // 城市坐标数据
      cityCoordinates: {},
      // 添加统计信息
      stats: {
        totalCities: 0,
        visitedCount: 0,
        chinaRate: '0%',
        worldRate: '0%'
      }
    }
  },
  
  // 页面加载完成后初始化地图
  onLoad() {
    // 从本地存储加载足迹数据
    const savedData = uni.getStorageSync('footprint_data');
    if (savedData) {
      try {
        this.footprintData = JSON.parse(savedData);
        // 更新访问城市列表
        this.updateVisitedCities();
      } catch (e) {
        console.error('解析足迹数据失败:', e);
      }
    }
  },
  
  // 页面显示时初始化地图
  onReady() {
    this.loadMapData();
  },
  
  methods: {
    // 加载地图数据
    async loadMapData() {
      try {
        uni.showLoading({
          title: '加载地图数据...'
        });
        
        // 加载中国地图数据
        if (!chinaJson) {
          const chinaRes = await uni.request({
            url: '/static/map/china.json',
            method: 'GET'
          });
          
          if (chinaRes.statusCode === 200 && chinaRes.data) {
            chinaJson = chinaRes.data;
            // 注册地图数据
            echarts.registerMap('china', chinaJson);
            console.log('中国地图数据加载成功');
          } else {
            throw new Error('中国地图数据加载失败');
          }
        }
        
        // 加载世界地图数据
        if (!worldJson) {
          const worldRes = await uni.request({
            url: '/static/map/world.json',
            method: 'GET'
          });
          
          if (worldRes.statusCode === 200 && worldRes.data) {
            worldJson = worldRes.data;
            // 注册地图数据
            echarts.registerMap('world', worldJson);
            console.log('世界地图数据加载成功');
          } else {
            throw new Error('世界地图数据加载失败');
          }
        }
        
        uni.hideLoading();
        
        // 初始化地图
        setTimeout(() => {
          this.initChinaMap();
          this.initWorldMap();
          // 更新统计信息
          this.updateStats();
        }, 300);
      } catch (error) {
        uni.hideLoading();
        console.error('加载地图数据失败:', error);
        uni.showToast({
          title: '地图数据加载失败',
          icon: 'none'
        });
      }
    },

    initChinaMap() {
      const query = uni.createSelectorQuery().in(this)
      query.select('#chinaMap')
        .fields({ node: true, size: true })
        .exec((res) => {
          if (res[0]) {
            const canvas = res[0].node
            const ctx = canvas.getContext('2d')
            
            canvas.width = res[0].width * 2
            canvas.height = res[0].height * 2
            
            this.chinaMap = echarts.init(canvas, null, {
              width: res[0].width,
              height: res[0].height,
              devicePixelRatio: 2
            })
            
            const option = {
              title: {
                text: '我的旅行足迹',
                left: 'center',
                textStyle: {
                  color: '#333',
                  fontSize: 16
                }
              },
              tooltip: {
                trigger: 'item',
                formatter: function(params) {
                  if (params.name) {
                    return params.name + '<br/>到访次数：' + (params.value || 0);
                  }
                }
              },
              visualMap: {
                type: 'piecewise',
                pieces: [
                  { min: 1, color: '#FFD700' },  // 已访问的城市显示金色
                  { max: 0, color: '#C0C0C0' }   // 未访问的城市显示灰色
                ],
                left: 'left',
                bottom: '10%',
                show: true
              },
              series: [
                {
                  name: '足迹',
                  type: 'map',
                  map: 'china',
                  roam: true,
                  scaleLimit: {
                    min: 1,
                    max: 5
                  },
                  label: {
                    show: true,
                    fontSize: 8,
                    color: '#333'
                  },
                  itemStyle: {
                    areaColor: '#C0C0C0',
                    borderColor: '#666',
                    borderWidth: 0.5
                  },
                  emphasis: {
                    label: {
                      show: true,
                      fontSize: 12,
                      color: '#fff'
                    },
                    itemStyle: {
                      areaColor: '#FFB800'
                    }
                  },
                  data: this.visitedCities
                },
                {
                  type: 'effectScatter',
                  coordinateSystem: 'geo',
                  data: this.visitedCities,
                  symbolSize: 12,
                  symbol: 'image://static/footprint.png',
                  showEffectOn: 'render',
                  rippleEffect: {
                    brushType: 'stroke'
                  },
                  label: {
                    show: true,
                    position: 'right',
                    formatter: '{b}'
                  },
                  itemStyle: {
                    color: '#FFD700'
                  },
                  emphasis: {
                    scale: true
                  },
                  zlevel: 1
                }
              ]
            }
            
            this.chinaMap.setOption(option)
          }
        })
    },

    initWorldMap() {
      const query = uni.createSelectorQuery().in(this)
      query.select('#worldMap')
        .fields({ node: true, size: true })
        .exec((res) => {
          if (res[0]) {
            const canvas = res[0].node
            const ctx = canvas.getContext('2d')
            
            canvas.width = res[0].width * 2
            canvas.height = res[0].height * 2
            
            this.worldMap = echarts.init(canvas, null, {
              width: res[0].width,
              height: res[0].height,
              devicePixelRatio: 2
            })
            
            const option = {
              backgroundColor: '#404a59',
              tooltip: {
                trigger: 'item',
                formatter: '{b}<br/>到访次数：{c}'
              },
              geo: {
                map: 'world',
                roam: true,
                scaleLimit: {
                  min: 1,
                  max: 10
                },
                itemStyle: {
                  areaColor: '#323c48',
                  borderColor: '#404a59',
                  borderWidth: 1
                },
                emphasis: {
                  itemStyle: {
                    areaColor: '#2a333d'
                  }
                }
              },
              series: [
                {
                  type: 'effectScatter',
                  coordinateSystem: 'geo',
                  data: this.getVisitedCityData('world'),
                  symbolSize: 15,
                  symbol: 'image://static/footprint.png',
                  showEffectOn: 'render',
                  rippleEffect: {
                    brushType: 'stroke'
                  },
                  label: {
                    show: true,
                    position: 'right',
                    formatter: '{b}',
                    color: '#fff'
                  },
                  itemStyle: {
                    color: '#FFD700',
                    shadowBlur: 10,
                    shadowColor: '#333'
                  },
                  emphasis: {
                    scale: true
                  },
                  zlevel: 1
                }
              ]
            }
            
            this.worldMap.setOption(option)
          }
        })
    },

    // 切换地图
    switchMap(type) {
      this.mapType = type
      setTimeout(() => {
        if (type === 'china') {
          this.chinaMap && this.chinaMap.resize()
        } else {
          this.worldMap && this.worldMap.resize()
        }
      }, 100)
    },

    // 获取已访问城市数据
    getVisitedCityData(mapType = 'china') {
      const visitedData = []
      
      // 简化处理，直接返回已访问城市数据
      if (mapType === 'world') {
        // 世界地图数据示例
        return [
          { name: '中国', value: [116.4, 39.9, 1], visitCount: 1 }
        ];
      }
      
      // 返回中国地图数据
      return this.visitedCities;
    },
    
    // 获取城市坐标数据
    getCityCoordinates(mapType) {
      // 这里可以根据实际需要返回城市坐标数据
      // 简化示例，实际项目中可能需要更完整的坐标数据
      return {
        '北京': [116.4, 39.9],
        '上海': [121.4, 31.2],
        '广州': [113.2, 23.1],
        '中国': [116.4, 39.9]
      };
    },
    
    // 获取用户当前位置并添加到足迹
    getUserLocation() {
      // 使用getFuzzyLocation获取模糊位置，因为只申请到了模糊地址接口
      uni.getFuzzyLocation({
        type: 'wgs84',
        success: (res) => {
          // 获取到模糊位置后，提示用户手动输入城市名称
          uni.showModal({
            title: '添加足迹',
            content: '已获取到您的大致位置，请输入您想要添加的城市名称',
            editable: true,
            placeholderText: '例如：北京',
            success: (modalRes) => {
              if (modalRes.confirm && modalRes.content) {
                // 用户输入了城市名称
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
        fail: (err) => {
          console.error('获取位置失败:', err);
          // 如果获取位置失败，也允许用户手动输入
          uni.showModal({
            title: '添加足迹',
            content: '无法获取您的位置，请手动输入您想要添加的城市名称',
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
        }
      });
    },
    
    // 已废弃，改用getFuzzyLocation和手动输入
    _getUserLocation_old() {
      // 使用chooseLocation让用户选择位置
      uni.chooseLocation({
        success: (res) => {
          if (res.name && res.address) {
            // 从选择的位置中提取城市名称
            // 通常地址格式为：省份市区详细地址
            const addressParts = res.address.split(/[省市区县]/);
            let cityName = '';
            
            // 尝试从地址中提取城市名称
            if (addressParts.length > 1) {
              // 假设第二部分是城市名称
              cityName = addressParts[1] || res.name;
            } else {
              // 如果无法解析，直接使用位置名称
              cityName = res.name;
            }
            
            // 添加到足迹
            this.addVisitedCity(cityName);
            uni.showToast({
              title: `已添加${cityName}到足迹`,
              icon: 'success'
            });
          } else {
            uni.showToast({
              title: '无法获取位置信息',
              icon: 'none'
            });
          }
        },
        fail: (err) => {
          console.error('选择位置失败:', err);
          uni.showToast({
            title: '选择位置失败',
            icon: 'none'
          });
        }
      });
    },
    
    // 不再需要单独的getLocationCity方法，直接在getUserLocation中处理
    
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
        
        // 添加到访问城市列表
        this.visitedCities.push({
          name: cleanCityName,
          value: 1
        });
      }
      
      // 保存数据并刷新地图
      this.saveFootprintData();
      this.refreshMaps();
    },
    
    // 保存足迹数据
    saveFootprintData() {
      try {
        // 将数据保存到本地存储
        uni.setStorageSync('footprint_data', JSON.stringify(this.footprintData));
      } catch (e) {
        console.error('保存足迹数据失败:', e);
      }
    },
    
    // 刷新地图
    refreshMaps() {
      if (this.chinaMap) {
        this.chinaMap.setOption({
          series: [{
            data: this.visitedCities
          }, {
            data: this.visitedCities
          }]
        });
      }
      
      if (this.worldMap) {
        this.worldMap.setOption({
          series: [{
            data: this.getVisitedCityData('world')
          }]
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
      
      // 更新统计信息
      this.updateStats();
    },
    
    // 更新统计信息
    updateStats() {
      // 计算已访问城市数量
      const visitedCount = Object.keys(this.footprintData.cities).length;
      
      // 假设中国有34个省级行政区（包括特别行政区和台湾）
      const totalChinaRegions = 34;
      
      // 假设世界有195个国家
      const totalWorldCountries = 195;
      
      // 计算覆盖率
      const chinaRate = ((visitedCount / totalChinaRegions) * 100).toFixed(1);
      const worldRate = ((1 / totalWorldCountries) * 100).toFixed(1); // 假设只访问了中国
      
      // 更新统计信息
      this.stats = {
        totalCities: visitedCount,
        visitedCount: visitedCount,
        chinaRate: chinaRate + '%',
        worldRate: worldRate + '%'
      };
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
}

.map-switch {
  display: flex;
  justify-content: center;
  padding: 12px 0;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 10;
  
  .switch-btn {
    flex: 1;
    max-width: 120px;
    margin: 0 10px;
    padding: 8px 0;
    font-size: 14px;
    border-radius: 20px;
    background: #f5f5f5;
    border: none;
    
    &.active {
      background: #007AFF;
      color: #fff;
    }
  }
}

.stats-panel {
  display: flex;
  justify-content: space-around;
  padding: 15px;
  background: #fff;
  border-bottom: 1px solid #eee;
  
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
  
  .map-canvas {
    width: 100%;
    height: 100%;
    position: absolute;
    left: 0;
    top: 0;
  }
}

.add-location-btn {
  position: fixed;
  right: 20px;
  bottom: 30px;
  display: flex;
  align-items: center;
  padding: 10px 15px;
  background: #007AFF;
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
