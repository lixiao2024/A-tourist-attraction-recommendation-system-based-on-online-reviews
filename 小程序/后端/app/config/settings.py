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
    DB_DRIVER: str = os.getenv("DB_DRIVER", "mysql+pymysql")
    DB_USERNAME: str = os.getenv("DB_USERNAME", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "m5llsjsw")
    DB_HOST: str = os.getenv("DB_HOST", "miniapp-mysql.ns-mprq9108.svc")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_NAME: str = os.getenv("DB_NAME", "miniapp")
    
    # 上传文件配置
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UPLOADS_DIR: str = os.path.join(BASE_DIR, "uploads", "images")
    API_URL: str = os.getenv("API_URL", "http://localhost:8000")
    
    # 构建数据库连接字符串
    @property
    def DATABASE_URL(self) -> str:
        # 如果是PostgreSQL，使用psycopg2驱动
        if self.DB_DRIVER == "postgresql":
            return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # 默认使用MySQL
        return f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True

# 创建设置实例
settings = Settings()
