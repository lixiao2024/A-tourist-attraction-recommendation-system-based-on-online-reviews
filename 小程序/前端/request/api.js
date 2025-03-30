/**
 * 旅游景点智能推荐系统 API 接口
 */

import request from './request.js';

// 基础URL - 改为你电脑的局域网IP，小程序不能直接访问localhost/127.0.0.1
// 使用如下命令查看你的IP: ipconfig (Windows) 或 ifconfig (Mac/Linux)
const baseURL = 'http://192.168.1.10:8000'; // 使用你的真实局域网IP

/**
 * 上传单张图片
 * @param {Object} file - 图片文件对象
 * @returns {Promise} - 返回上传结果
 */
export function uploadImage(file) {
  // 创建FormData对象
  const formData = new FormData();
  formData.append('file', file);
  
  return request({
    url: '/api/upload',
    method: 'POST',
    header: {
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  });
}

/**
 * 上传多张图片
 * @param {Array} files - 图片文件对象数组
 * @returns {Promise} - 返回上传结果
 */
export function uploadMultipleImages(files) {
  // 创建FormData对象
  const formData = new FormData();
  files.forEach((file, index) => {
    formData.append('files', file);
  });
  
  return request({
    url: '/api/upload/multiple',
    method: 'POST',
    header: {
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  });
}

/**
 * 通过uni-app上传单张图片
 * @param {String} tempFilePath - 临时文件路径
 * @returns {Promise} - 返回上传结果
 */
export function uniUploadImage(tempFilePath) {
  return new Promise((resolve, reject) => {
    uni.uploadFile({
      url: baseURL + '/api/upload',
      filePath: tempFilePath,
      name: 'file',
      header: {
        'Content-Type': 'multipart/form-data',
        'Authorization': uni.getStorageSync('token') ? `Bearer ${uni.getStorageSync('token')}` : ''
      },
      formData: {}, // 添加空的formData对象，确保请求格式正确
      success: (res) => {
        if (res.statusCode === 201) {
          // 上传成功，解析返回数据
          let data = res.data;
          if (typeof data === 'string') {
            try {
              data = JSON.parse(data);
            } catch (e) {
              console.error('解析返回数据失败:', e);
            }
          }
          resolve(data);
        } else {
          reject(new Error('上传失败：状态码 ' + res.statusCode + (res.data ? ', ' + res.data : '')));
        }
      },
      fail: (err) => {
        console.error('上传请求失败:', err);
        reject(err);
      }
    });
  });
}

/**
 * 通过uni-app上传多张图片
 * @param {Array} tempFilePaths - 临时文件路径数组
 * @returns {Promise} - 返回上传结果，包含所有图片的URL
 */
export function uniUploadMultipleImages(tempFilePaths) {
  if (!Array.isArray(tempFilePaths) || tempFilePaths.length === 0) {
    return Promise.reject(new Error('没有要上传的图片'));
  }
  
  console.log('准备上传的图片数量:', tempFilePaths.length);
  console.log('上传服务器地址:', baseURL + '/api/upload/multiple');

  // 如果只有一张图片，使用单图上传
  if (tempFilePaths.length === 1) {
    return uniUploadImage(tempFilePaths[0])
      .then(result => ({
        files: [result]
      }));
  }
  
  // 多张图片逐个上传
  return new Promise((resolve, reject) => {
    const uploads = tempFilePaths.map(path => {
      return uniUploadImage(path);
    });
    
    Promise.all(uploads)
      .then(results => {
        console.log('所有图片上传完成:', results.length);
        resolve({
          files: results
        });
      })
      .catch(err => {
        console.error('图片上传过程中出错:', err);
        reject(err);
      });
  });
}

/**
 * 创建博文
 * @param {Object} postData - 博文数据
 * @returns {Promise} - 返回创建结果
 */
export function createPost(postData) {
  console.log('【DEBUG】createPost - 请求URL:', baseURL + '/api/posts');
  console.log('【DEBUG】createPost - 请求数据:', postData);
  
  return request({
    url: '/api/posts',
    method: 'POST',
    data: postData
  }).then(res => {
    console.log('【DEBUG】createPost - 请求成功:', res);
    return res;
  }).catch(err => {
    console.error('【DEBUG】createPost - 请求失败:', err);
    // 确保错误包含原始服务器响应
    if (err.response && err.response.data) {
      throw err.response.data;
    }
    throw err;
  });
}

/**
 * 获取博文列表
 * @param {Number} skip - 跳过的记录数
 * @param {Number} limit - 返回的最大记录数
 * @param {String} tag - 按标签筛选（可选）
 * @param {Number} userId - 按用户ID筛选（可选）
 * @returns {Promise} - 返回博文列表
 */
export function getPosts(skip = 0, limit = 10, tag = null, userId = null) {
  // 构建查询参数
  let url = `/api/posts?skip=${skip}&limit=${limit}`;
  
  // 添加可选筛选参数
  if (tag) {
    url += `&tag=${encodeURIComponent(tag)}`;
  }
  
  if (userId) {
    url += `&user_id=${userId}`;
  }
  
  console.log('【DEBUG】getPosts - 请求URL:', baseURL + url);
  
  return request({
    url: url,
    method: 'GET'
  }).then(res => {
    console.log('【DEBUG】getPosts - 请求成功:', res);
    // 确保返回的是数组
    if (!res) {
      return [];
    }
    if (!Array.isArray(res)) {
      console.warn('【DEBUG】getPosts - 返回非数组结果:', res);
      return [];
    }
    return res;
  }).catch(err => {
    console.error('【DEBUG】getPosts - 请求失败:', err);
    throw err;
  });
}

/**
 * 获取单个博文详情
 * @param {Number} postId - 博文ID
 * @returns {Promise} - 返回博文详情
 */
export function getPostDetail(postId) {
  if (!postId) {
    console.error('【DEBUG】getPostDetail - 缺少postId参数');
    return Promise.reject(new Error('缺少postId参数'));
  }
  
  console.log('【DEBUG】getPostDetail - 请求URL:', baseURL + `/api/posts/${postId}`);
  
  return request({
    url: `/api/posts/${postId}`,
    method: 'GET'
  }).then(res => {
    console.log('【DEBUG】getPostDetail - 请求成功:', res);
    return res;
  }).catch(err => {
    console.error('【DEBUG】getPostDetail - 请求失败:', err);
    throw err;
  });
}

/**
 * 发布评论（包含图片上传）
 * @param {Object} commentData - 评论数据
 * @param {Array} imagePaths - 图片路径数组
 * @param {String} coverImagePath - 封面图片路径
 * @returns {Promise} - 返回发布结果
 */
export function publishComment(commentData, imagePaths = [], coverImagePath = null) {
  console.log('【DEBUG】publishComment - 开始');
  console.log('【DEBUG】publishComment - 评论数据:', commentData);
  console.log('【DEBUG】publishComment - 图片路径:', imagePaths);
  console.log('【DEBUG】publishComment - 封面图片:', coverImagePath);
  
  return new Promise(async (resolve, reject) => {
    try {
      let uploadedImages = [];
      let coverImageUrl = '';
      
      // 上传图片（如果有）
      if (imagePaths.length > 0) {
        console.log('【DEBUG】publishComment - 开始上传图片');
        const imageResult = await uniUploadMultipleImages(imagePaths);
        console.log('【DEBUG】publishComment - 图片上传结果:', imageResult);
        uploadedImages = imageResult.files.map(file => file.url);
      }
      
      // 上传封面图（如果有）
      if (coverImagePath) {
        console.log('【DEBUG】publishComment - 开始上传封面图');
        const coverResult = await uniUploadImage(coverImagePath);
        console.log('【DEBUG】publishComment - 封面图上传结果:', coverResult);
        coverImageUrl = coverResult.url;
      }
      
      // 构建发布数据
      const postData = {
        title: commentData.title || commentData.content.substring(0, 50) || '旅行分享',
        content: commentData.content,
        images: uploadedImages,
        tags: commentData.topics || [],
        location: commentData.location || '',
        cover_image: coverImageUrl || (uploadedImages.length > 0 ? uploadedImages[0] : '')
      };
      
      console.log('【DEBUG】publishComment - 准备提交博文:', postData);
      
      // 提交博文
      const result = await createPost(postData);
      
      console.log('【DEBUG】publishComment - 博文提交成功:', result);
      
      // 将博文同时保存为笔记
      saveAsNote({
        id: result.id,
        title: postData.title,
        content: postData.content,
        createTime: new Date().toISOString().split('T')[0], // 格式化为YYYY-MM-DD
        location: postData.location,
        likeCount: 0,
        commentCount: 0,
        images: uploadedImages,
        tags: postData.tags,
        cover_image: coverImageUrl || (uploadedImages.length > 0 ? uploadedImages[0] : '')
      });
      
      resolve(result);
    } catch (error) {
      console.error('【DEBUG】publishComment - 出错:', error);
      reject(error);
    }
  });
}

/**
 * 将发布的内容保存为笔记
 * @param {Object} noteData - 笔记数据
 */
function saveAsNote(noteData) {
  try {
    // 从本地存储获取现有笔记
    let userNotes = uni.getStorageSync('userNotes') || [];
    
    // 确保userNotes是数组
    if (!Array.isArray(userNotes)) {
      userNotes = [];
    }
    
    // 处理图片URL，确保使用完整路径
    if (noteData.images && noteData.images.length > 0) {
      noteData.images = noteData.images.map(img => {
        // 检查URL是否完整，如果不是则添加基础URL
        if (img && !img.startsWith('http')) {
          return baseURL + img;
        }
        return img;
      });
    }
    
    // 处理封面图URL
    if (noteData.cover_image && !noteData.cover_image.startsWith('http')) {
      noteData.cover_image = baseURL + noteData.cover_image;
    }
    
    // 添加新笔记到数组开头（最新的笔记显示在最前面）
    userNotes.unshift(noteData);
    
    // 保存回本地存储
    uni.setStorageSync('userNotes', userNotes);
    
    console.log('【DEBUG】saveAsNote - 笔记保存成功:', noteData);
  } catch (e) {
    console.error('【DEBUG】saveAsNote - 保存笔记失败:', e);
  }
}

/**
 * 删除博文
 * @param {Number} postId - 博文ID
 * @returns {Promise} - 返回删除结果
 */
export function deletePost(postId) {
  if (!postId) {
    console.error('【DEBUG】deletePost - 缺少postId参数');
    return Promise.reject(new Error('缺少postId参数'));
  }
  
  console.log('【DEBUG】deletePost - 请求URL:', baseURL + `/api/posts/${postId}`);
  
  return request({
    url: `/api/posts/${postId}`,
    method: 'DELETE'
  }).then(() => {
    console.log('【DEBUG】deletePost - 删除成功');
    return true;
  }).catch(err => {
    console.error('【DEBUG】deletePost - 删除失败:', err);
    throw err;
  });
} 