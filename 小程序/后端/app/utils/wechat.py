import requests
from app.config.settings import settings
from typing import Dict, Any

# 微信接口基本URL
WECHAT_API_URL = "https://api.weixin.qq.com"

def get_session_key(code: str) -> Dict[str, Any]:
    """
    通过微信登录的临时 code 获取 session_key 和 openid
    
    Args:
        code: 小程序登录时获取的临时 code
        
    Returns:
        包含 session_key, openid 等信息的字典
    """
    url = f"{WECHAT_API_URL}/sns/jscode2session"
    params = {
        "appid": settings.WECHAT_APPID,
        "secret": settings.WECHAT_SECRET,
        "js_code": code,
        "grant_type": "authorization_code"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 如果请求失败，抛出异常
        
        result = response.json()
        if "errcode" in result and result["errcode"] != 0:
            return {
                "success": False,
                "message": f"微信API错误: {result.get('errmsg', '未知错误')}",
                "error_code": result.get("errcode")
            }
        
        return {
            "success": True,
            "session_key": result.get("session_key"),
            "openid": result.get("openid"),
            "unionid": result.get("unionid")  # 如果有的话
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "message": f"请求微信API失败: {str(e)}",
            "error_code": -1
        }
