/**
 * 请求封装模块
 */

// 基础URL - 使用局域网IP替代localhost
const BASE_URL = 'http://192.168.1.10:8000';

// 超时时间（毫秒）
const TIMEOUT = 15000;

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
  let errMsg = '请求失败';
  if (response.data) {
    if (typeof response.data === 'string') {
      errMsg = response.data;
    } else if (response.data.detail) {
      errMsg = response.data.detail;
    } else if (response.data.message) {
      errMsg = response.data.message;
    }
  }
  
  uni.showToast({
    title: errMsg,
    icon: 'none'
  });
  
  return Promise.reject({
    statusCode: response.statusCode,
    message: errMsg,
    data: response.data
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
    timeout: options.timeout || TIMEOUT
  };
  
  console.log('【DEBUG】request - 开始请求:', config.url);
  console.log('【DEBUG】request - 请求方法:', config.method);
  console.log('【DEBUG】request - 请求头:', config.header);
  console.log('【DEBUG】request - 请求数据:', config.data);
  
  // 处理请求拦截
  const finalConfig = requestInterceptor(config);
  
  // 网络检查
  return new Promise((resolve, reject) => {
    // 检查网络状态
    uni.getNetworkType({
      success: (networkRes) => {
        if (networkRes.networkType === 'none') {
          uni.showToast({
            title: '网络连接不可用，请检查网络设置',
            icon: 'none'
          });
          reject(new Error('网络连接不可用'));
          return;
        }
        
        // 发起请求
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
            
            let errorMsg = '网络请求失败';
            // 处理常见错误
            if (error.errMsg) {
              if (error.errMsg.includes('timeout')) {
                errorMsg = '请求超时，请稍后再试';
              } else if (error.errMsg.includes('abort')) {
                errorMsg = '请求已取消';
              } else if (error.errMsg.includes('fail')) {
                // 检查是否是因为服务器不可达
                if (error.errMsg.includes('fail:')) {
                  errorMsg = '无法连接到服务器，请检查网络';
                }
              }
            }
            
            uni.showToast({
              title: errorMsg,
              icon: 'none'
            });
            
            reject({
              ...error,
              message: errorMsg
            });
          }
        });
      },
      fail: () => {
        uni.showToast({
          title: '无法获取网络状态',
          icon: 'none'
        });
        reject(new Error('无法获取网络状态'));
      }
    });
  });
} 