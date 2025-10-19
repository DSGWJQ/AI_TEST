# FIRST_MIX

一个现代化的前后端分离项目模板：后端（Python）与前端（Vue 3 + Vite + Tailwind CSS），支持 Docker 部署、Windows/WSL2 本地开发以及基础测试。

> 提示：本文档包含 Docker 与 Docker Compose 的示例，后端启动命令以 FastAPI/Uvicorn 为例，请根据实际入口与依赖进行调整（参考 <mcfile name="main.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\main.py"></mcfile>）。

---

## 特性

- 模块化后端，包含数据库、缓存、邮件、加密与脚本执行
  - 数据库：<mcfile name="database.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\app\\database.py"></mcfile>
  - Redis 客户端：<mcfile name="redis_client.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\app\\redis_client.py"></mcfile>
  - 邮件发送：<mcfile name="mail.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\app\\mail.py"></mcfile>
  - 安全与加密：<mcfile name="crypto.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\app\\crypto.py"></mcfile>
  - 输入清洗：<mcfile name="sanitizer.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\app\\sanitizer.py"></mcfile>
  - 脚本执行：<mcfile name="script_executor.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\app\\script_executor.py"></mcfile>
- 现代化前端工程（Vue 3 + Vite + Tailwind + PNPM）
  - 前端 Docker 支持：<mcfile name="Dockerfile" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\frontend\\vue-project\\Dockerfile"></mcfile>
  - Nginx 配置：<mcfile name="nginx.conf" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\frontend\\vue-project\\nginx.conf"></mcfile>
- 环境变量模板：<mcfile name=".env.example" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\.env.example"></mcfile>
- 测试报告样例：<mcfile name="pytest_report.html" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\test_reports\\pytest_report.html"></mcfile>

## 技术栈

- 后端：Python 3.12+/3.13（建议）、Uvicorn/FastAPI（以项目结构推测，实际以代码为准）
- 缓存：Redis（如使用 <mcfile name="redis_client.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\app\\redis_client.py"></mcfile>）
- 前端：Vue 3、Vite、Tailwind CSS、PNPM
- 部署：Docker、可选 Docker Compose

## 目录结构

```plaintext
c:\\Users\\23225\\PycharmProjects\\FIRST_MIX
├── .env.example
├── .gitattributes
├── .gitignore
├── README.md
├── backend\\
│   ├── app\\
│   │   ├── crud.py
│   │   ├── crypto.py
│   │   ├── database.py
│   │   ├── mail.py
│   │   ├── redis_client.py
│   │   ├── sanitizer.py
│   │   └── script_executor.py
│   └── main.py
├── frontend\\
│   ├── package.json
│   ├── pnpm-lock.yaml
│   └── vue-project\\
│       ├── Dockerfile
│       ├── nginx.conf
│       ├── package.json
│       ├── pnpm-lock.yaml
│       ├── public\\
│       ├── src\\
│       └── vite.config.js
├── package.json
├── package-lock.json
├── scripts\\
├── test_backend.py
└── test_reports\\
    ├── assets\\
    │   └── style.css
    └── pytest_report.html
```

## 开发指南（Windows/WSL2）

### 前置条件

- Windows 11（建议安装 Docker Desktop 与启用 WSL2）
- Python 3.12+/3.13
- Node.js 18+ 与 PNPM（前端）
- 如需缓存，安装并运行 Redis

### 环境变量

复制示例环境变量文件：

```bash
copy .env.example .env
```

根据实际情况填充数据库、Redis、邮件等配置。

### 后端启动（示例为 FastAPI/Uvicorn）

> 运行 Python 命令前，请先激活你的虚拟环境。

创建虚拟环境：

```bash
py -m venv .venv
```

激活虚拟环境：

```bash
.\.venv\Scripts\activate
```

安装依赖（若使用 requirements.txt）：

```bash
pip install -r backend\requirements.txt
```

启动后端（根据 <mcfile name="main.py" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend\\main.py"></mcfile> 调整模块与对象名）：

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动（Vite）

进入前端工程目录：

```bash
cd frontend\vue-project
```

安装依赖：

```bash
pnpm install
```

启动开发服务器（默认 5173）：

```bash
pnpm dev
```

## Docker 部署

### 前端（已有 Dockerfile）

构建镜像：

```bash
docker build -t first-mix-web -f frontend\vue-project\Dockerfile frontend\vue-project
```

运行容器（映射到 8080）：

```bash
docker run -d -p 8080:80 --name first-mix-web first-mix-web
```

Nginx 配置参考：<mcfile name="nginx.conf" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\frontend\\vue-project\\nginx.conf"></mcfile>

### 后端（新增 Dockerfile 示例）

在 <mcfile name="backend" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\backend"></mcfile> 目录新增 Dockerfile（示例以 requirements.txt 为例，按需调整）：

```dockerfile:c%3A%5C%5CUsers%5C%5C23225%5C%5CPycharmProjects%5C%5CFIRST_MIX%5C%5Cbackend%5C%5CDockerfile
FROM python:3.13-slim
WORKDIR /app

# 安装依赖
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# 复制后端源代码
COPY . /app

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# 如果入口不是 main:app，请根据 backend/main.py 调整
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建后端镜像：

```bash
docker build -t first-mix-api -f backend\Dockerfile backend
```

运行后端容器：

```bash
docker run -d -p 8000:8000 --name first-mix-api first-mix-api
```

### 使用 Docker Compose（可选）

在项目根目录新增 docker-compose.yml：

```yaml:c%3A%5C%5CUsers%5C%5C23225%5C%5CPycharmProjects%5C%5CFIRST_MIX%5C%5Cdocker-compose.yml
version: "3.9"
services:
  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped

  web:
    build:
      context: ./frontend/vue-project
      dockerfile: Dockerfile
    ports:
      - "8080:80"
    depends_on:
      - api
    restart: unless-stopped
```

启动所有服务：

```bash
docker compose up -d --build
```

停止并清理：

```bash
docker compose down
```

### WSL2 与网络注意事项

- 建议在 Windows 11 上启用 WSL2 与使用 Docker Desktop，以获得更好的性能与兼容性。
- 如遇端口冲突（8000/8080/5173），请在启动命令或配置中调整对应端口。

## 测试

安装 pytest 后运行：

```bash
python -m pytest
```

测试报告示例可参见：<mcfile name="pytest_report.html" path="c:\\Users\\23225\\PycharmProjects\\FIRST_MIX\\test_reports\\pytest_report.html"></mcfile>

## 提交到 GitHub

初始化本地仓库：

```bash
git init
```

暂存文件：

```bash
git add .
```

首次提交：

```bash
git commit -m "chore: init project"
```

切换默认分支：

```bash
git branch -M main
```

添加远程：

```bash
git remote add origin https://github.com/YOUR_NAME/REPO.git
```

推送：

```bash
git push -u origin main
```

> 可在 README 顶部加入来自 Shields.io 的徽章（如 License、Build、Docker、Issues 等），提升信息密度与可读性。

## 许可证

建议选择 MIT 或 Apache-2.0，并在仓库根目录添加 LICENSE 文件；在 README 中标注许可证类型与链接。

---

如你使用 Poetry/PDM 等依赖管理工具，请告知我以便更新后端 Dockerfile 与安装命令；若后端并非 FastAPI/Uvicorn，也请提供实际启动入口（模块与对象名）以便修正启动命令。