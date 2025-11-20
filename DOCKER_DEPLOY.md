# Docker部署指南

本文档详细介绍了如何使用Docker部署XiaoZhiShi博客系统。

## 目录

1. [前置要求](#前置要求)
2. [快速开始](#快速开始)
3. [Docker部署方式](#docker部署方式)
4. [Docker Compose部署（推荐）](#docker-compose部署推荐)
5. [环境变量配置](#环境变量配置)
6. [数据持久化](#数据持久化)
7. [日志管理](#日志管理)
8. [性能优化](#性能优化)
9. [故障排除](#故障排除)
10. [安全建议](#安全建议)

## 前置要求

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

### 安装Docker

**Ubuntu/Debian:**
```bash
# 更新包索引
sudo apt-get update

# 安装必要的包
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release

# 添加Docker官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置稳定版仓库
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 安装Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 验证安装
docker --version
docker compose version
```

**CentOS/RHEL:**
```bash
# 安装必要的包
sudo yum install -y yum-utils device-mapper-persistent-data lvm2

# 添加Docker仓库
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装Docker Engine
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
docker compose version
```

**Windows:**
1. 下载Docker Desktop: https://www.docker.com/products/docker-desktop
2. 安装并启动Docker Desktop
3. 验证安装:
```powershell
docker --version
docker compose version
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/XiaoZhiShi.git
cd XiaoZhiShi
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# Flask配置
SECRET_KEY=your-secret-key-here-change-this
DEBUG=False
FLASK_APP=run.py
FLASK_ENV=production

# 数据库配置（PostgreSQL）
DATABASE_URL=postgresql://xiaozhishi:xiaozhishi@db:5432/xiaozhishi

# DEEPSEEK API配置
DEEPSEEK_APIKEY=your-deepseek-api-key-here

# 其他配置
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
```

**注意：** 在生产环境中，务必更改以下配置：
- `SECRET_KEY`: 使用强随机密钥
- `DEEPSEEK_APIKEY`: 配置您的API密钥
- 数据库密码: 使用强密码

### 3. Docker Compose部署（推荐）

```bash
# 构建并启动服务
docker-compose up -d --build

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 初始化数据库
docker-compose exec web python init_db.py

# 创建管理员账户
docker-compose exec web python create_admin.py
```

### 4. 验证部署

访问以下地址验证部署：

- **前台**: http://localhost
- **后台**: http://localhost/admin
- **API文档**: http://localhost/api/docs (如果有)

## Docker部署方式

### 方式一：Docker Compose（推荐）

Docker Compose是部署XiaoZhiShi最简单的方式，它会自动管理所有服务（Web应用、数据库、Nginx）。

#### 启动服务

```bash
# 后台运行
docker-compose up -d

# 前台运行（调试用）
docker-compose up
```

#### 管理服务

```bash
# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs web      # Web应用日志
docker-compose logs db       # 数据库日志
docker-compose logs nginx    # Nginx日志

# 实时查看日志
docker-compose logs -f

# 查看服务状态
docker-compose ps

# 进入容器
docker-compose exec web bash
```

#### 更新服务

```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
docker-compose up -d --build

# 数据库迁移
docker-compose exec web flask db upgrade
```

### 方式二：单独使用Docker

如果您不想使用Docker Compose，可以手动运行各个容器。

#### 1. 创建Docker网络

```bash
docker network create xiaozhishi-network
```

#### 2. 启动PostgreSQL数据库

```bash
docker run -d \
  --name xiaozhishi-db \
  --network xiaozhishi-network \
  -e POSTGRES_USER=xiaozhishi \
  -e POSTGRES_PASSWORD=xiaozhishi \
  -e POSTGRES_DB=xiaozhishi \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:15-alpine
```

#### 3. 构建并启动Web应用

```bash
# 构建镜像
docker build -t xiaozhishi .

# 启动容器
docker run -d \
  --name xiaozhishi-web \
  --network xiaozhishi-network \
  -p 5000:5000 \
  -e DATABASE_URL=postgresql://xiaozhishi:xiaozhishi@xiaozhishi-db:5432/xiaozhishi \
  -e SECRET_KEY=your-secret-key \
  -e DEEPSEEK_APIKEY=your-api-key \
  -v $(pwd)/instance:/app/instance \
  -v $(pwd)/app/static/uploads:/app/app/static/uploads \
  xiaozhishi
```

#### 4. 初始化数据库

```bash
docker exec xiaozhishi-web python init_db.py
docker exec xiaozhishi-web python create_admin.py
```

## 环境变量配置

### 必需环境变量

```env
# Flask密钥（必须修改）
SECRET_KEY=your-secret-key-here-change-this-to-a-random-string

# 数据库URL
DATABASE_URL=postgresql://xiaozhishi:xiaozhishi@db:5432/xiaozhishi

# DEEPSEEK API密钥（如果使用AI功能）
DEEPSEEK_APIKEY=your-deepseek-api-key
```

### 可选环境变量

```env
# Flask配置
DEBUG=False
FLASK_APP=run.py
FLASK_ENV=production

# 数据库连接池
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# 邮件配置（如果需要邮件功能）
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# 文件上传限制
MAX_CONTENT_LENGTH=16777216  # 16MB

# 日志级别
LOG_LEVEL=INFO
```

### 生成SECRET_KEY

```bash
# Linux/Mac
openssl rand -hex 32

# PowerShell
-join ((65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

## 数据持久化

Docker Compose配置中已经包含了数据持久化：

### 数据库数据

```yaml
volumes:
  postgres_data:
    driver: local
```

数据库数据存储在Docker卷中，即使删除容器，数据也不会丢失。

### 上传文件

```yaml
volumes:
  - ./app/static/uploads:/app/static/uploads
```

上传的文件存储在宿主机的 `./app/static/uploads` 目录中。

### 实例数据

```yaml
volumes:
  - ./instance:/app/instance
```

应用实例数据（如配置文件）存储在宿主机的 `./instance` 目录中。

### 备份数据

```bash
# 备份数据库
docker-compose exec db pg_dump -U xiaozhishi xiaozhishi > backup_$(date +%Y%m%d).sql

# 备份上传文件
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz ./app/static/uploads

# 恢复数据库
cat backup.sql | docker-compose exec -T db psql -U xiaozhishi xiaozhishi
```

## 日志管理

### 查看日志

```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# 实时查看日志
docker-compose logs -f

# 查看最后100行日志
docker-compose logs --tail=100 web

# 查看特定时间段的日志
docker-compose logs --since=2025-01-01 --until=2025-01-31 web
```

### 日志轮转

在 `docker-compose.yml` 中添加日志配置：

```yaml
services:
  web:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 集中式日志管理

如果使用ELK Stack：

```yaml
services:
  web:
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://localhost:5000"
        tag: "xiaozhishi"
```

## 性能优化

### 1. 调整Gunicorn配置

修改 `docker-compose.yml` 中的Gunicorn参数：

```yaml
services:
  web:
    command: >
      gunicorn
      --bind 0.0.0.0:5000
      --workers 4              # 根据CPU核心数调整
      --threads 2              # 每个worker的线程数
      --timeout 120            # 超时时间
      --keep-alive 5           # keep-alive超时
      --max-requests 1000      # 每个worker处理的最大请求数
      --max-requests-jitter 50 # 随机抖动，避免同时重启
      --access-logfile -
      --error-logfile -
      app:app
```

### 2. 数据库优化

```yaml
services:
  db:
    environment:
      - POSTGRES_USER=xiaozhishi
      - POSTGRES_PASSWORD=xiaozhishi
      - POSTGRES_DB=xiaozhishi
      - POSTGRES_MAX_CONNECTIONS=100
      - POSTGRES_SHARED_BUFFERS=256MB
      - POSTGRES_EFFECTIVE_CACHE_SIZE=1GB
```

### 3. Nginx优化

在 `nginx.conf` 中添加缓存配置：

```nginx
# 静态文件缓存
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# Gzip压缩优化
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 6;
gzip_types ...
```

### 4. 使用Redis缓存

添加Redis服务：

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: xiaozhishi-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  web:
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - db
```

## 故障排除

### 1. 容器无法启动

```bash
# 查看容器状态
docker-compose ps

# 查看详细错误
docker-compose logs web

# 进入容器排查
docker-compose exec web bash
```

### 2. 数据库连接失败

```bash
# 检查数据库容器
docker-compose logs db

# 进入数据库容器
docker-compose exec db psql -U xiaozhishi -d xiaozhishi

# 测试连接
docker-compose exec web python -c "from app import create_app; app = create_app(); print('Database connected')"
```

### 3. 静态文件加载失败

```bash
# 检查文件权限
docker-compose exec web ls -la /app/static/

# 检查Nginx配置
docker-compose logs nginx
```

### 4. 内存不足

```bash
# 查看内存使用
docker stats

# 限制容器内存
docker-compose up -d --build
# 然后在 docker-compose.yml 中添加：
# services:
#   web:
#     mem_limit: 512M
#     mem_reservation: 256M
```

### 5. 端口冲突

```bash
# 查看端口占用
netstat -tuln | grep 5000

# 修改端口
docker-compose down
# 修改 docker-compose.yml 中的 ports 配置
docker-compose up -d
```

## 安全建议

### 1. 使用非root用户运行容器

```dockerfile
# Dockerfile
RUN groupadd -r xiaozhishi && useradd -r -g xiaozhishi xiaozhishi
USER xiaozhishi
```

### 2. 定期更新镜像

```bash
# 拉取最新基础镜像
docker-compose pull

# 重新构建应用
docker-compose up -d --build

# 清理旧镜像
docker image prune -a
```

### 3. 使用Secrets管理敏感信息

```bash
# 创建secret
echo "your-secret-key" | docker secret create secret_key -
echo "your-api-key" | docker secret create deepseek_api_key -

# docker-compose.yml (Swarm模式)
version: '3.8'

services:
  web:
    secrets:
      - secret_key
      - deepseek_api_key

secrets:
  secret_key:
    external: true
  deepseek_api_key:
    external: true
```

### 4. 配置防火墙

```bash
# 仅允许必要端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 5. 使用HTTPS

```bash
# 获取SSL证书（使用Let's Encrypt）
docker run -it --rm \
  -p 80:80 \
  -p 443:443 \
  -v /etc/letsencrypt:/etc/letsencrypt \
  certbot/certbot certonly --standalone -d your-domain.com

# 配置Nginx使用SSL（修改nginx.conf）
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    # ...
}
```

## 监控和维护

### 1. 监控容器状态

```bash
# 查看容器资源使用
docker stats

# 查看容器详细信息
docker inspect xiaozhishi-web
```

### 2. 自动重启

```yaml
# docker-compose.yml
services:
  web:
    restart: unless-stopped
    
  db:
    restart: unless-stopped
    
  nginx:
    restart: unless-stopped
```

### 3. 定期备份

创建备份脚本 `backup.sh`：

```bash
#!/bin/bash
BACKUP_DIR="/backup/xiaozhishi/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T db pg_dump -U xiaozhishi xiaozhishi > $BACKUP_DIR/database.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads.tar.gz ./app/static/uploads

# 备份配置文件
cp .env $BACKUP_DIR/
cp docker-compose.yml $BACKUP_DIR/

# 删除30天前的备份
find /backup/xiaozhishi -type d -mtime +30 -exec rm -rf {} +
```

### 4. 日志轮转

```bash
# 使用logrotate创建配置文件 /etc/logrotate.d/xiaozhishi
/path/to/XiaoZhiShi/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 root root
}
```

## 升级指南

### 1. 备份数据

```bash
# 停止服务
docker-compose down

# 备份数据
cp -r app/static/uploads uploads_backup_$(date +%Y%m%d)
docker-compose exec db pg_dump -U xiaozhishi xiaozhishi > backup_$(date +%Y%m%d).sql
```

### 2. 更新代码

```bash
# 拉取最新代码
git pull origin main
```

### 3. 更新配置

```bash
# 检查配置文件是否有更新
git diff docker-compose.yml
git diff .env.example
```

### 4. 重新部署

```bash
# 重新构建并启动
docker-compose up -d --build

# 数据库迁移（如果需要）
docker-compose exec web flask db upgrade
```

### 5. 验证升级

```bash
# 检查服务状态
docker-compose ps

# 查看日志
docker-compose logs -f --tail=100

# 测试功能
```

## 卸载

```bash
# 停止并删除所有容器
docker-compose down -v

# 删除镜像
docker rmi xiaozhishi-web

# 删除数据卷（谨慎操作）
docker volume rm xiaozhishi_postgres_data

# 删除网络
docker network rm xiaozhishi-network
```

## 获取更多帮助

- [Docker官方文档](https://docs.docker.com/)
- [Docker Compose官方文档](https://docs.docker.com/compose/)
- [项目GitHub Issues](https://github.com/yourusername/XiaoZhiShi/issues)
- [项目Wiki](https://github.com/yourusername/XiaoZhiShi/wiki)

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
