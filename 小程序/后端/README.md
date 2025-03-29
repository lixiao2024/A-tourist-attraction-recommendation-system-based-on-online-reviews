# 旅游景点智能推荐系统后端

基于 FastAPI 开发的旅游景点智能推荐系统后端服务。

## 技术栈

- Python 3.8+
- FastAPI
- SQLAlchemy
- MySQL
- Uvicorn

## 安装和运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 运行服务：

```bash
uvicorn main:app --reload
```

服务将在 http://localhost:8000 启动，API 文档可在 http://localhost:8000/docs 查看。

## 项目结构

```
.
├── main.py          # 主应用入口
├── requirements.txt # 项目依赖
└── README.md       # 项目说明
```

## API 文档

启动服务后，可以通过以下地址访问 API 文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**每次使用项目需要激活环境**：
.\venv\Scripts\Activate.ps1
退出环境：deactivate
运行项目执行：uvicorn main:app --reload

---

访问 http://localhost:8000 查看 API 的欢迎页面
访问 http://localhost:8000/docs 查看交互式 API 文档
访问 http://localhost:8000/redoc 查看另一种风格的 API 文档

---

当您需要添加新的 Python 包时，确保在虚拟环境激活的状态下安装，并更新 requirements.txt：
pip install 新包名
pip freeze > requirements.txt
