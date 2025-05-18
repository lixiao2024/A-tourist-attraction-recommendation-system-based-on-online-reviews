from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
import httpx
import logging
import json
from app.config.settings import settings

# 设置日志
logger = logging.getLogger(__name__)

class AssistantService:
    def __init__(self, db: Session):
        self.db = db
        # 阿里百炼API配置，从配置文件中获取
        self.app_id = settings.ALIBAILIAN_APP_ID
        self.api_key = settings.ALIBAILIAN_API_KEY
        self.base_url = f"https://dashscope.aliyuncs.com/api/v1/apps/{self.app_id}/completion"
        
    async def chat_with_assistant(
        self,
        user_message: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        调用阿里百炼API进行对话
        
        Args:
            user_message: 用户发送的消息
            session_id: 可选的会话ID，用于维持对话上下文
            
        Returns:
            Dict[str, Any]: 包含AI回复文本和会话ID的字典
        """
        logger.info(f"准备调用阿里百炼API, 会话ID: {session_id}")
        
        # 准备请求数据
        request_data = {
            "input": {
                "prompt": user_message
            },
            "parameters": {},
            "debug": {}
        }
        
        # 如果有会话ID，添加到请求中
        if session_id:
            request_data["input"]["session_id"] = session_id
        
        # 设置请求头
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            # 使用httpx异步发送请求
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.base_url,
                    json=request_data,
                    headers=headers
                )
                
                # 检查响应状态
                response.raise_for_status()
                
                # 解析响应
                response_data = response.json()
                logger.info(f"阿里百炼API调用成功: {json.dumps(response_data, ensure_ascii=False)[:200]}...")
                
                # 从响应中提取文本和会话ID
                output = response_data.get("output", {})
                text = output.get("text", "")
                new_session_id = output.get("session_id", "")
                
                return {
                    "text": text,
                    "session_id": new_session_id
                }
                
        except httpx.HTTPStatusError as e:
            logger.error(f"API调用返回错误状态码: {e.response.status_code}")
            logger.error(f"响应内容: {e.response.text}")
            raise Exception(f"API调用失败: {e.response.text}")
            
        except httpx.RequestError as e:
            logger.error(f"API请求失败: {str(e)}")
            raise Exception(f"网络请求失败: {str(e)}")
            
        except Exception as e:
            logger.error(f"调用阿里百炼API时发生未知错误: {str(e)}")
            raise Exception(f"处理API请求时发生错误: {str(e)}") 