/**
 * 请求封装模块
 */

// 基础URL - 使用局域网IP替代localhost
const BASE_URL = 'http://192.168.1.10:8000';

// 请求拦截器
const requestInterceptor = (config) => {
  // 获取token
  const token = uni.getStorageSync('token');
  if (token) {
    config.header = {
      ...config.header,
      'Authorization': `Bearer ${token}`
    };
  }
  return config;
};

// 响应拦截器
const responseInterceptor = (response) => {
  // 请求成功
  if (response.statusCode >= 200 && response.statusCode < 300) {
    return response.data;
  }
  
  // 未授权，清除token并跳转登录页
  if (response.statusCode === 401) {
    uni.removeStorageSync('token');
    uni.showToast({
      title: '登录已过期，请重新登录',
      icon: 'none'
    });
    
    setTimeout(() => {
      uni.navigateTo({
        url: '/pages/login/login'
      });
    }, 1500);
    
    return Promise.reject(new Error('未授权'));
  }
  
  // 422验证错误，直接返回详细错误信息以便上层处理
  if (response.statusCode === 422) {
    console.log('【DEBUG】验证错误:', response.data);
    return Promise.reject({
      statusCode: 422,
      ...response.data
    });
  }
  
  // 其他错误
  uni.showToast({
    title: response.data.detail || '请求失败',
    icon: 'none'
  });
  
  return Promise.reject({
    statusCode: response.statusCode,
    ...response.data
  });
};

/**
 * 统一请求方法
 * @param {Object} options - 请求配置
 * @returns {Promise} - 返回请求结果
 */
export default function request(options) {
  // 合并请求配置
  const config = {
    url: BASE_URL + (options.url || ''),
    method: options.method || 'GET',
    data: options.data || {},
    header: options.header || {
      'Content-Type': 'application/json'
    },
    timeout: options.timeout || 30000
  };
  
  console.log('【DEBUG】request - 开始请求:', config.url);
  console.log('【DEBUG】request - 请求方法:', config.method);
  console.log('【DEBUG】request - 请求头:', config.header);
  console.log('【DEBUG】request - 请求数据:', config.data);
  
  // 处理请求拦截
  const finalConfig = requestInterceptor(config);
  console.log('【DEBUG】request - 拦截器处理后:', finalConfig);
  
  // 发起请求
  return new Promise((resolve, reject) => {
    uni.request({
      ...finalConfig,
      success: (res) => {
        console.log('【DEBUG】request - 请求成功, 状态码:', res.statusCode);
        console.log('【DEBUG】request - 响应数据:', res.data);
        try {
          const result = responseInterceptor(res);
          resolve(result);
        } catch (error) {
          console.error('【DEBUG】request - 响应拦截器错误:', error);
          reject(error);
        }
      },
      fail: (error) => {
        console.error('【DEBUG】request - 请求失败:', error);
        uni.showToast({
          title: '网络请求失败',
          icon: 'none'
        });
        reject(error);
      }
    });
  });
} 