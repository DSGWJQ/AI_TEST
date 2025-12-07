# 使用官方 Node.js 镜像作为基础镜像
FROM node:20

# 设置工作目录
WORKDIR /app

# 复制 package.json 和 pnpm-lock.yaml（如果存在）
COPY package*.json ./
COPY pnpm-lock.yaml* ./

# 安装 pnpm
RUN npm install -g pnpm

# 安装依赖
RUN pnpm install

# 复制项目文件
COPY . .

# 暴露端口 5173
EXPOSE 5173

# 启动开发服务器（确保参数透传）
CMD ["pnpm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]