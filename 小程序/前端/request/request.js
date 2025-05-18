/**
 * 请求封装模块
 */

// 基础URL - 使用局域网IP替代localhost
const BASE_URL = 'http://192.168.1.10:8000';

// 超时时间（毫秒）- 增加到30秒，因为短信发送可能需要更长时间
const TIMEOUT = 30000;

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
  
  // 日志请求详情
  console.log('【DEBUG】请求配置:', {
    url: config.url,
    method: config.method,
    data: config.data,
    header: config.header
  });
  
  return config;
};

// 响应拦截器
const responseInterceptor = (response, requestConfig) => {
  // 请求成功
  if (response.statusCode >= 200 && response.statusCode < 300) {
    return response.data;
  }
  
  // 未授权，处理未登录的情况
  if (response.statusCode === 401) {
    // 判断请求的URL是否是/api/posts或其它不需要强制登录的接口
    const requestUrl = requestConfig?.url || '';
    const requestMethod = requestConfig?.method || '';
    
    if (requestUrl.includes('/api/posts') && !requestUrl.includes('/api/posts/') && requestMethod === 'GET') {
      // 获取帖子列表的请求不需要强制登录，返回空数组
      console.log('【DEBUG】未登录获取帖子列表，返回空数据');
      return [];
    } else {
      // 其他请求需要登录，清除token并跳转登录页
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
const request = (options) => {
  // 显示加载提示
  if (!options.hideLoading) {
    try {
      uni.showLoading({
        title: '加载中...',
        mask: true
      });
    } catch (err) {
      console.warn('showLoading failed:', err);
    }
  }

  // 设置默认超时时间 - 使用全局定义的TIMEOUT
  if (!options.timeout) {
    options.timeout = TIMEOUT;
  }
  
  // SMS请求单独设置更长的超时时间
  if (options.url && (options.url.includes('/phone/send-code') || options.url.includes('/phone/verify-and-bind'))) {
    options.timeout = TIMEOUT * 2; // 短信相关请求使用双倍超时时间
    console.log('【DEBUG】检测到短信相关请求，设置更长的超时时间:', options.timeout);
  }

  // 添加重试机制
  const maxRetries = 3;
  let retryCount = 0;

  const executeRequest = () => {
    return new Promise((resolve, reject) => {
      // 应用请求拦截器
      const processedOptions = requestInterceptor(options);
      
      uni.request({
        url: processedOptions.url.startsWith('http') ? processedOptions.url : (BASE_URL + processedOptions.url),
        method: processedOptions.method || 'GET',
        data: processedOptions.data,
        header: {
          'content-type': 'application/json',
          ...processedOptions.header
        },
        timeout: processedOptions.timeout,
        success: (res) => {
          console.log('【DEBUG】request - 请求成功, 状态码:', res.statusCode, '请求URL:', processedOptions.url);
          
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(res.data);
          } else {
            // 应用响应拦截器处理错误
            try {
              const interceptedRes = responseInterceptor(res, processedOptions);
              resolve(interceptedRes);
            } catch (interceptorError) {
              const error = {
                statusCode: res.statusCode,
                message: res.data?.detail || '请求失败',
                data: res.data
              };
              reject(error);
            }
          }
        },
        fail: (err) => {
          console.error('【DEBUG】request - 请求失败:', err);
          
          // 短信相关请求，如果是超时错误，尝试继续操作
          if (processedOptions.url && 
             (processedOptions.url.includes('/phone/send-code') || 
              processedOptions.url.includes('/phone/verify-and-bind')) && 
              err.errMsg.includes('timeout')) {
            
            console.log('【DEBUG】短信请求超时，但可能已成功发送，返回默认成功状态');
            
            // 如果是发送验证码请求，返回一个默认的成功响应，让用户继续输入验证码
            if (processedOptions.url.includes('/phone/send-code')) {
              resolve({
                success: true,
                message: "验证码可能已发送，请检查手机短信",
                details: "请求超时，但短信可能已发送成功"
              });
              return;
            }
          }
          
          if (retryCount < maxRetries && (err.errMsg.includes('timeout') || err.errMsg.includes('fail'))) {
            retryCount++;
            console.log(`【DEBUG】request - 第${retryCount}次重试`);
            setTimeout(() => {
              executeRequest().then(resolve).catch(reject);
            }, 1000 * retryCount); // 重试延迟递增
          } else {
            reject({
              statusCode: -1,
              message: err.errMsg || '网络请求失败',
              data: err
            });
          }
        },
        complete: () => {
          if (!options.hideLoading) {
            try {
              uni.hideLoading();
            } catch (err) {
              console.warn('hideLoading failed:', err);
            }
          }
        }
      });
    });
  };

  return executeRequest();
};

// 默认配置
request.defaults = {
  baseURL: BASE_URL
};

export default request; 