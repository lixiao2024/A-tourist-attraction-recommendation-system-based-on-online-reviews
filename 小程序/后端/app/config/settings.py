from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    # 微信小程序配置
    WECHAT_APPID: str = os.getenv("WECHAT_APPID", "wx605cbaa175f26b8d")
    WECHAT_SECRET: str = os.getenv("WECHAT_SECRET", "50bf76c87e2bf43b50a6cde8632443fe")
    
    # JWT 配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    # 数据库配置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:1111@localhost:5432/postgres")
    
    # 上传文件配置
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UPLOADS_DIR: str = os.path.join(BASE_DIR, "uploads", "images")
    API_URL: str = os.getenv("API_URL", "http://localhost:8000")
    
    # 阿里百炼API配置
    ALIBAILIAN_APP_ID: str = os.getenv("ALIBAILIAN_APP_ID", "a004749b7ab34735bd4c0574a0d8e2f2")
    ALIBAILIAN_API_KEY: str = os.getenv("ALIBAILIAN_API_KEY", "sk-b5e444efee24456898a9b1756994b0e5")
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True
     # 添加新字段
    OLLAMA_API_BASE: Optional[str] = None
    MODEL_NAME: Optional[str] = None 
    DASHSCOPE_API_KEY: Optional[str] = None

# 创建设置实例
settings = Settings()
