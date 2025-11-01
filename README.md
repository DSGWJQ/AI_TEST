# FIRST_MIX 🚀

一款现代化的前后端分离全栈项目模板，集成最新的技术栈和最佳实践，助力快速开发高质量应用。

> ✨ 基于 Python 3.12+ 后端 + Vue 3 前端，支持 Docker 容器化部署，Windows/WSL2 本地开发

## 🎥 项目亮点

### 1. 模块化后端架构
采用分层设计模式，提供完整的企业级后端解决方案，包含数据库操作、缓存管理、邮件服务、加密安全等核心模块。

### 2. 现代化前端体验
基于 Vue 3 + Vite + Tailwind CSS 构建响应式用户界面，支持热重载和现代化构建流程。

### 3. 一键部署方案
完整的 Docker 容器化支持，前后端分离部署，支持生产环境快速上线。

## ✨ 核心特性

🎯 **模块化设计** - 清晰的后端架构分层，易于维护和扩展
📝 **现代化前端** - Vue 3 + Vite + Tailwind CSS 技术栈
🔄 **容器化部署** - Docker + Docker Compose 完整支持
🤖 **多环境支持** - 开发、测试、生产环境配置分离
🔒 **安全架构** - 内置加密、输入清洗、安全防护
📊 **测试覆盖** - 完整的测试体系和报告生成
🛠️ **开发友好** - 热重载、自动重启、开发工具集成

## 🚀 技术栈

### 后端技术
- **Python 3.12+** - 现代 Python 版本支持
- **FastAPI** - 高性能异步 Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **Redis** - 高性能缓存服务
- **Pydantic** - 数据验证和序列化

### 前端技术
- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Tailwind CSS** - 实用优先的 CSS 框架
- **TypeScript** - 类型安全的 JavaScript
- **PNPM** - 高效的包管理器

### 部署和工具
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排
- **Nginx** - 高性能 Web 服务器
- **Pytest** - Python 测试框架

## 📦 快速开始

### 1. 环境要求

- Python 3.12+ 和 pip
- Node.js 18+ 和 PNPM
- Docker 和 Docker Compose（可选）
- Redis（可选，用于缓存）

### 2. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/FIRST_MIX.git
cd FIRST_MIX
```

### 3. 环境配置

复制环境变量模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件，配置你的 API 密钥和数据库连接：

```env
# OpenRouter API Key
VITE_OPENROUTER_API_KEY=your_openrouter_api_key_here

# Ollama URL
VITE_OLLAMA_URL=http://localhost:11434/v1
```

## 🔧 开发指南

### 后端开发

1. **创建虚拟环境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.\.venv\Scripts\activate  # Windows
```

2. **安装依赖**
```bash
pip install -r backend/requirements.txt
```

3. **启动开发服务器**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

1. **进入前端目录**
```bash
cd frontend/vue-project
```

2. **安装依赖**
```bash
pnpm install
```

3. **启动开发服务器**
```bash
pnpm dev
```

## 🐳 Docker 部署

### 构建镜像

```bash
# 构建前端镜像
docker build -t first-mix-web -f frontend/vue-project/Dockerfile frontend/vue-project

# 构建后端镜像
docker build -t first-mix-api -f backend/Dockerfile backend
```

### 运行容器

```bash
# 运行前端容器
docker run -d -p 8080:80 --name first-mix-web first-mix-web

# 运行后端容器
docker run -d -p 8000:8000 --name first-mix-api first-mix-api
```

### Docker Compose（推荐）

```bash
# 启动所有服务
docker-compose up -d

# 停止服务
docker-compose down
```

## 📁 项目结构

```
FIRST_MIX/
├── backend/                    # 后端源码
│   ├── app/                   # 应用核心模块
│   │   ├── crud.py           # 数据库 CRUD 操作
│   │   ├── crypto.py         # 加密解密工具
│   │   ├── database.py       # 数据库连接
│   │   ├── mail.py           # 邮件服务
│   │   ├── redis_client.py   # Redis 客户端
│   │   ├── sanitizer.py      # 输入清洗
│   │   └── script_executor.py # 脚本执行器
│   └── main.py               # FastAPI 入口
├── frontend/vue-project/     # Vue 3 前端项目
│   ├── src/                  # 源码目录
│   ├── public/               # 静态资源
│   ├── Dockerfile            # 前端 Docker 配置
│   └── nginx.conf            # Nginx 配置
├── test_reports/              # 测试报告
├── scripts/                   # 脚本工具
├── docker-compose.yml         # Docker Compose 配置
└── README.md                 # 项目文档
```

## 🧪 测试

运行后端测试：

```bash
pytest
```

查看测试报告：
打开 `test_reports/pytest_report.html` 查看详细的测试结果。

## 📝 开发建议

### 后端开发
- 使用类型提示提高代码可读性
- 遵循 PEP 8 编码规范
- 编写单元测试和集成测试
- 使用环境变量管理配置

### 前端开发
- 使用 TypeScript 提高类型安全
- 遵循 Vue 3 Composition API 最佳实践
- 组件化开发，提高复用性
- 使用 Tailwind CSS 工具类快速构建界面

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [FastAPI](https://fastapi.tiangolo.com/) - 现代、快速的后端框架
- [Tailwind CSS](https://tailwindcss.com/) - 实用优先的 CSS 框架
- [Vite](https://vitejs.dev/) - 下一代前端构建工具

---

⭐ 如果这个项目对你有帮助，请给个 Star！

💡 有任何问题或建议，欢迎提交 Issue 或 Pull Request！