from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api import router as api_router
from app.models.database import engine, Base
from app.config.settings import settings

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 确保上传目录存在
os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

app = FastAPI(
    title="旅游景点智能推荐系统API",
    description="基于在线评论的旅游景点智能推荐系统后端API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册静态文件服务
app.mount("/uploads", StaticFiles(directory=os.path.join(settings.BASE_DIR, "uploads")), name="uploads")

# 包含API路由
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "欢迎使用旅游景点智能推荐系统API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
