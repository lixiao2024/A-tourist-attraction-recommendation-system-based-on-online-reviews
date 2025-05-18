from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import uvicorn
import traceback
import os

# 初始化FastAPI应用
app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 从环境变量中读取Ollama API地址，如果未设置则使用默认值
OLLAMA_API_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
MODEL_NAME = "shiroi/qwen7b-q4:latest"

print(f"使用Ollama API地址: {OLLAMA_API_BASE}")

class QwenRequest(BaseModel):
    question: str
    history: list = []

@app.post("/api/qwen-chat")
async def chat(request: QwenRequest):
    try:
        print(f"收到问题: {request.question}")
        print(f"历史记录: {request.history}")
        
        # 构建Ollama API请求的消息列表
        messages = []
        
        # 添加历史消息
        for item in request.history:
            if isinstance(item, dict) and "role" in item and "content" in item:
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })
        
        # 添加当前问题
        messages.append({
            "role": "user",
            "content": request.question
        })
        
        print(f"准备调用Ollama API，消息列表: {messages}")
        
        # 调用Ollama API
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                print(f"发送请求到 {OLLAMA_API_BASE}/api/generate")
                
                # 构建完整提示词，包含历史对话
                full_prompt = ""
                for item in messages:
                    role = item.get("role", "")
                    content = item.get("content", "")
                    if role == "user":
                        full_prompt += f"用户: {content}\n"
                    elif role == "assistant":
                        full_prompt += f"助手: {content}\n"
                
                # 添加当前问题
                if not full_prompt.endswith(f"用户: {request.question}\n"):
                    full_prompt += f"用户: {request.question}\n"
                full_prompt += "助手: "
                
                print(f"完整提示词: {full_prompt}")
                
                response = await client.post(
                    f"{OLLAMA_API_BASE}/api/generate",
                    json={
                        "model": MODEL_NAME,
                        "prompt": full_prompt,
                        "stream": False,
                        "temperature": 0.7,
                    },
                    timeout=60.0
                )
                
                if response.status_code != 200:
                    error_msg = f"Ollama API调用失败: 状态码 {response.status_code}, 响应内容: {response.text}"
                    print(error_msg)
                    raise HTTPException(
                        status_code=500,
                        detail=error_msg
                    )
                
                result = response.json()
                print(f"收到Ollama响应: {result}")
                
                # 使用正确的响应字段
                assistant_response = result.get("response", "")
                if not assistant_response:
                    assistant_response = "抱歉，我无法回答您的问题。"
                
                return {
                    "response": assistant_response,
                    "history": messages + [{
                        "role": "assistant",
                        "content": assistant_response
                    }]
                }
        except httpx.RequestError as e:
            error_msg = f"请求Ollama API时发生错误: {str(e)}"
            print(error_msg)
            print(f"详细错误: {traceback.format_exc()}")
            raise HTTPException(status_code=500, detail=error_msg)
            
    except Exception as e:
        error_msg = f"与Qwen模型交互时出错: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    print("启动API服务...")
    print("使用Ollama的Qwen-7B模型")
    print("API服务将在 http://localhost:8001 上运行")
    print(f"Ollama API地址: {OLLAMA_API_BASE}")
    uvicorn.run(app, host="0.0.0.0", port=8001) 