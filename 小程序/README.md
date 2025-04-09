# 基于在线评论的旅游景点智能推荐系统

这是一个基于在线评论的旅游景点智能推荐系统，包含前端小程序和后端服务。

## 项目结构

- `前端/`: 小程序前端代码
- `后端/`: 后端服务代码
- `Dockerfile`: 后端服务的 Docker 配置文件
- `docker-compose.yml`: Docker 编排配置文件

## 使用 Docker 运行

### 前提条件

- 安装 [Docker](https://www.docker.com/get-started)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)

### 运行步骤

1. 克隆项目到本地

```bash
git clone <项目地址>
cd <项目目录>
```

2. 使用 Docker Compose 启动服务

```bash
docker-compose up -d
```

3. 拉取 Qwen 模型（首次运行需要）

```bash
docker exec -it <项目目录>_ollama_1 ollama pull shiroi/qwen7b-q4:latest
```

4. 访问服务

- 后端 API 服务: http://localhost:8000
- Ollama 服务: http://localhost:11434

### 停止服务

```bash
docker-compose down
```

## 开发说明

### 后端开发

后端使用 FastAPI 框架开发，主要文件：

- `simple_app.py`: 主应用入口
- `qwen_api.py`: Qwen 模型 API 调用

### 前端开发

前端使用 uni-app 框架开发，主要目录：

- `pages/`: 页面文件
- `request/`: API 请求封装

## 注意事项

1. 首次运行时，需要拉取 Qwen 模型，这可能需要一些时间
2. 确保 Docker 有足够的资源（CPU 和内存）运行 Ollama 服务
3. 如果需要修改后端代码，可以直接修改`后端/`目录下的文件，Docker 会自动重新加载

## 项目文件说明

创建了 Dockerfile，用于构建后端服务
创建了 docker-compose.yml 文件，用于编排整个应用
创建了.dockerignore 文件，排除不需要的文件
创建了 README.md 文件，提供项目说明和使用 Docker 运行的方法
创建了 start.sh 和 start.bat 文件，方便用户一键启动整个项目
修改了后端代码，使其能够从环境变量中读取 Ollama API 的地址
创建了.env 文件，用于存储环境变量
创建了.gitignore 文件，排除不需要提交到版本控制的文件
现在，您可以使用以下命令在其他电脑上运行整个项目：
克隆项目到本地
运行 docker-compose up -d 启动服务
运行 docker exec -it <项目目录>\_ollama_1 ollama pull shiroi/qwen7b-q4:latest 拉取 Qwen 模型
访问后端 API 服务：http://localhost:8000
访问 Ollama 服务：http://localhost:11434
或者，您可以直接运行 start.sh（Linux/Mac）或 start.bat（Windows）文件，一键启动整个项目。
这样，您就可以在其他电脑上轻松运行整个项目了。
