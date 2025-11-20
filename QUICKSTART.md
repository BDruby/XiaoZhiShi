# XiaoZhiShi 快速开始指南

## 项目部署完成！

恭喜！XiaoZhiShi博客系统已经准备就绪，可以部署到GitHub了。

## 📦 已创建的文件

### 文档文件
- ✅ **README.md** - 项目主文档，包含完整的功能介绍、安装说明、使用指南
- ✅ **DOCKER_DEPLOY.md** - Docker部署详细指南
- ✅ **QUICKSTART.md** - 本快速开始指南

### 部署脚本
- ✅ **deploy.ps1** - Windows一键部署PowerShell脚本
- ✅ **Dockerfile** - Docker镜像构建文件
- ✅ **docker-compose.yml** - Docker Compose配置
- ✅ **nginx.conf** - Nginx反向代理配置

### 配置文件
- ✅ **.gitignore** - Git忽略文件配置
- ✅ **requirements.txt** - Python依赖包列表

## 🚀 三种部署方式

### 方式一：一键部署（Windows推荐）

```powershell
# 1. 克隆项目
git clone https://github.com/yourusername/XiaoZhiShi.git
cd XiaoZhiShi

# 2. 运行一键部署脚本（自动完成环境配置、依赖安装、数据库初始化）
.\deploy.ps1

# 3. 按照提示完成部署
```

**特点**：
- 自动检查Python环境
- 自动创建虚拟环境
- 自动安装依赖
- 自动初始化数据库
- 自动创建管理员账户
- 支持开发和生产模式

### 方式二：Docker部署（跨平台推荐）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/XiaoZhiShi.git
cd XiaoZhiShi

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置必要参数

# 3. 启动服务
docker-compose up -d --build

# 4. 初始化数据库
docker-compose exec web python init_db.py

# 5. 创建管理员
docker-compose exec web python create_admin.py
```

**特点**：
- 跨平台支持（Windows/Linux/Mac）
- 隔离环境，避免依赖冲突
- 一键启动所有服务（Web+DB+Nginx）
- 易于扩展和维护
- 适合生产环境

### 方式三：手动部署（开发者推荐）

```bash
# 1. 克隆项目
git clone https://github.com/yourusername/XiaoZhiShi.git
cd XiaoZhiShi

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 5. 初始化数据库
python init_db.py

# 6. 创建管理员
python create_admin.py

# 7. 运行应用
python run.py
# 或
flask run
```

**特点**：
- 完全控制部署过程
- 适合开发和调试
- 易于定制和扩展

## ⚙️ 环境变量配置

创建 `.env` 文件：

```env
# Flask配置（必须修改）
SECRET_KEY=your-secret-key-here-change-this-to-random-string
DEBUG=False
FLASK_APP=run.py
FLASK_ENV=production

# 数据库配置
# SQLite（开发）
DATABASE_URL=sqlite:///blog.db
# PostgreSQL（生产/Docker）
# DATABASE_URL=postgresql://xiaozhishi:xiaozhishi@db:5432/xiaozhishi

# DEEPSEEK API配置（如果使用AI功能）
DEEPSEEK_APIKEY=your-deepseek-api-key-here

# 邮件配置（可选）
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
```

## 🔐 首次访问

部署完成后，访问以下地址：

- **前台首页**: http://localhost:5000 (或 http://localhost)
- **管理后台**: http://localhost:5000/admin
- **API接口**: http://localhost:5000/api

默认管理员账户：
- 用户名: admin
- 密码: admin123

**⚠️ 安全提醒**：首次登录后请立即修改默认密码！

## 📁 项目结构

```
XiaoZhiShi/
├── app/                      # 主应用目录
│   ├── admin/               # 后台管理
│   ├── api/                 # API接口
│   ├── auth/                # 认证系统
│   ├── main/                # 前台功能
│   ├── media/               # 媒体管理
│   ├── models/              # 数据模型
│   ├── static/              # 静态资源
│   ├── templates/           # HTML模板
│   └── utils/               # 工具函数
├── instance/                # 实例数据
├── migrations/              # 数据库迁移
├── app.py                   # 应用工厂
├── run.py                   # 应用入口
├── requirements.txt         # Python依赖
├── Dockerfile              # Docker配置
├── docker-compose.yml      # Docker Compose配置
├── nginx.conf              # Nginx配置
├── deploy.ps1              # Windows一键部署脚本
├── README.md               # 项目文档
├── DOCKER_DEPLOY.md        # Docker部署指南
├── QUICKSTART.md           # 快速开始指南
└── .gitignore              # Git忽略配置
```

## 🎯 核心功能

### 用户管理
- ✅ 用户注册/登录/注销
- ✅ 角色权限管理（管理员、编辑、普通用户）
- ✅ 个人资料管理

### 内容管理
- ✅ 文章创建、编辑、发布、删除
- ✅ 文章分类和标签管理
- ✅ 富文本编辑器支持
- ✅ 文章草稿和发布状态管理

### AI功能
- ✅ 集成DEEPSEEK AI API
- ✅ 自动生成文章标题、内容、摘要
- ✅ 智能分类和标签建议
- ✅ SEO优化建议

### SEO优化
- ✅ 自定义meta标签
- ✅ Open Graph支持
- ✅ Twitter Card支持
- ✅ 自动生成sitemap.xml
- ✅ 自动生成robots.txt
- ✅ 规范URL支持

### 媒体管理
- ✅ 图片上传和管理
- ✅ 图片缩略图生成
- ✅ 媒体库管理

### 导航管理
- ✅ 自定义前台导航菜单
- ✅ 多级导航支持
- ✅ 导航排序和激活状态

### 其他功能
- ✅ 全文搜索
- ✅ 响应式设计
- ✅ 用户仪表盘
- ✅ 评论系统（可扩展）

## 🔧 常用命令

### 数据库管理

```bash
# 初始化数据库
python init_db.py

# 创建管理员
python create_admin.py

# 数据库迁移
flask db migrate -m "描述变更"
flask db upgrade
flask db downgrade
```

### Docker管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec web bash

# 重启服务
docker-compose restart

# 重新构建
docker-compose up -d --build
```

### 应用管理

```bash
# 开发模式
python run.py

# 生产模式
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 查看日志
tail -f logs/app.log
```

## 📖 详细文档

- **完整项目文档**: [README.md](README.md)
- **Docker部署指南**: [DOCKER_DEPLOY.md](DOCKER_DEPLOY.md)
- **API文档**: 访问 `/api` 端点查看

## 🐛 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -ano | findstr :5000  # Windows
   netstat -tuln | grep 5000     # Linux
   
   # 修改端口
   # 在 .env 文件中修改，或在启动时指定
   ```

2. **数据库连接失败**
   ```bash
   # 检查数据库服务
   docker-compose ps db
   
   # 查看数据库日志
   docker-compose logs db
   ```

3. **依赖安装失败**
   ```bash
   # 升级pip
   pip install --upgrade pip
   
   # 清除pip缓存
   pip cache purge
   ```

4. **静态文件加载失败**
   ```bash
   # 检查文件权限
   chmod -R 755 app/static/
   ```

## 🆘 获取帮助

- **GitHub Issues**: [提交Issue](https://github.com/yourusername/XiaoZhiShi/issues)
- **项目Wiki**: [查看Wiki](https://github.com/yourusername/XiaoZhiShi/wiki)
- **邮箱支持**: your-email@example.com

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出功能建议！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🎉 部署完成！

现在您已经成功部署了XiaoZhiShi博客系统！

### 下一步建议：

1. **配置域名**: 将域名指向您的服务器IP
2. **配置HTTPS**: 使用Let's Encrypt免费SSL证书
3. **配置CDN**: 使用Cloudflare等CDN加速静态资源
4. **配置备份**: 定期备份数据库和上传文件
5. **监控告警**: 配置监控和告警系统
6. **SEO优化**: 配置Google Analytics、百度统计等
7. **内容创作**: 开始创作您的第一篇博客文章！

### 生产环境建议：

- ✅ 使用PostgreSQL代替SQLite
- ✅ 配置Nginx反向代理
- ✅ 配置HTTPS
- ✅ 配置防火墙
- ✅ 定期更新系统和依赖
- ✅ 配置日志监控
- ✅ 配置自动备份

祝您使用愉快！🎊
