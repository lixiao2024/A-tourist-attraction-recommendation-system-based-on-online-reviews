'use strict';
const crypto = require('crypto')

// 微信小程序配置（请替换为实际值）
const APPID = 'wx605cbaa175f26b8d' // 替换为实际AppID
const SECRET = '570f6455ffbc736f1afa310ad678ff8f' // 替换为实际Secret

exports.main = async (event, context) => {
	const { code, userInfo } = event
	try {
		// 获取微信session
		const res = await uniCloud.httpclient.request(
			`https://api.weixin.qq.com/sns/jscode2session?appid=${APPID}&secret=${SECRET}&js_code=${code}&grant_type=authorization_code`,
			{ dataType: 'json' }
		)
		
		if (res.status !== 200 || res.data.errcode) {
			return { code: 500, msg: '微信登录失败', error: res.data }
		}

		const { openid, session_key } = res.data
		const db = uniCloud.database()
		const users = db.collection('users')
		
		// 用户数据操作
		const countRes = await users.where({ openid }).count()
		const existed = countRes.result || { total: 0 }

		console.log('用户存在检查:', { openid, existed })

		const loginLog = {
			ip: context.CLIENTIP || '未知IP',
			device: context.DEVICEID || '未知设备',
			timestamp: Date.now()
		}

		if (existed.total === 0) {
			 const addRes = await users.add({
				openid,
				nickname: userInfo.nickName || '未命名用户',
				avatar: userInfo.avatarUrl || '',
				last_login: Date.now(),
				login_log: [loginLog]
			})
			console.log('新增用户结果:', addRes)
		} else {
			const updateRes = await users.where({ openid }).update({
				last_login: Date.now(),
				login_log: db.command.push(loginLog)
			})
			console.log('更新用户结果:', updateRes)
		}

		// 生成简单token
		const tokenPayload = {
			uid: openid,
			role: 'user',
			exp: Math.floor(Date.now()/1000) + 7200
		}
		
		// Base64编码token
		const token = Buffer.from(JSON.stringify(tokenPayload)).toString('base64')

		return {
			code: 200,
			data: {
				token,
				userInfo: {
					openid,
					nickname: userInfo.nickName || '未命名用户',
					avatar: userInfo.avatarUrl || ''
				}
			}
		}
	} catch (error) {
		console.error('云函数执行错误：', error)
		return {
			code: 500,
			msg: '云函数执行异常',
			error: error.message
		}
	}
}
