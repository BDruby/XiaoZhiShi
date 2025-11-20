# XiaoZhiShi (小芝士)英文名：CheesePress - 现代化博客系统

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## 项目简介

XiaoZhiShi (小智识) 是一个基于 Flask 框架开发的现代化博客内容管理系统 (CMS)，提供了完整的博客平台功能，包括用户管理、文章发布、分类标签系统、SEO优化以及AI内容生成等高级功能。

### 核心特性

- **用户管理系统**：支持用户注册、登录、角色管理（普通用户、编辑、管理员）
- **内容管理**：支持文章创建、编辑、发布、分类和标签管理
- **AI内容生成**：集成DEEPSEEK AI API，可自动生成博客内容
- **SEO优化**：全面的SEO支持，包括meta标签、Open Graph、Twitter Card、sitemap.xml和robots.txt
- **响应式设计**：适配各种设备的前端界面
- **媒体管理**：支持上传和管理媒体文件
- **导航管理**：可自定义前台导航菜单
- **搜索功能**：全文搜索支持

## 技术栈

### 后端
- **Flask**: 2.3.2 - Python微框架
- **SQLAlchemy**: 2.0.15 - ORM框架
- **Flask-Login**: 0.6.3 - 用户认证
- **Flask-JWT-Extended**: 4.5.2 - JWT认证
- **Flask-Migrate**: 4.0.5 - 数据库迁移
- **Flask-WTF**: 1.1.1 - 表单处理
- **Flask-CORS**: 4.0.0 - 跨域支持

### 前端
- **Jinja2**: 模板引擎
- **Tailwind CSS**: 3.x - CSS框架
- **JavaScript**: 原生JS + 现代ES6+

### 数据库
- **SQLite**: 开发环境默认
- **PostgreSQL**: 生产环境推荐

### 其他依赖
- **Pillow**: 9.5.0 - 图片处理
- **OpenAI SDK**: 1.3.5 - AI内容生成
- **Gunicorn**: 21.2.0 - WSGI服务器
- **python-dotenv**: 1.0.0 - 环境变量管理

## 项目结构

```
XiaoZhiShi/
├── app.py                      # 应用工厂
├── run.py                      # 应用入口
├── requirements.txt           # Python依赖
├── .env                       # 环境变量配置
├── Dockerfile                 # Docker配置
├── docker-compose.yml         # Docker Compose配置
├── deploy.sh                  # 一键部署脚本
├── README.md                  # 项目文档
├── app/                       # 主应用目录
│   ├── __init__.py           # 应用初始化
│   ├── admin/                # 管理后台
│   │   ├── __init__.py
│   │   ├── ai.py            # AI生成工具
│   │   ├── forms.py         # 后台表单
│   │   ├── seo.py           # SEO设置
│   │   └── settings.py      # 系统设置
│   ├── api/                  # API接口
│   │   └── __init__.py
│   ├── auth/                 # 认证系统
│   │   ├── __init__.py
│   │   └── forms.py
│   ├── main/                 # 前台功能
│   │   ├── __init__.py
│   │   └── ...
│   ├── media/                # 媒体管理
│   │   └── __init__.py
│   ├── models/               # 数据模型
│   │   └── __init__.py
│   ├── static/               # 静态资源
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/         # 上传文件
│   ├── templates/            # HTML模板
│   │   ├── base.html
│   │   ├── admin/
│   │   ├── main/
│   │   └── macros/          # 宏模板
│   └── utils/                # 工具函数
│       ├── ai_generator.py
│       ├── og_image_generator.py
│       └── seo.py
├── instance/                 # 实例目录
│   └── blog.db              # SQLite数据库
├── migrations/               # 数据库迁移
└── tests/                   # 测试文件
```

## 快速开始

### 前置要求

- Python 3.8+
- pip (Python包管理器)
- Git

### 本地安装

1. **克隆项目**
```bash
git clone https://github.com/yourusername/XiaoZhiShi.git
cd XiaoZhiShi
```

2. **创建虚拟环境**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库和API密钥
```

5. **初始化数据库**
```bash
python init_db.py
```

6. **创建管理员账户**
```bash
python create_admin.py
```

7. **运行应用**
```bash
# 开发模式
python run.py

# 或使用Flask命令
flask run

# 生产模式
python run.py
```

访问 http://127.0.0.1:5000 查看前台，http://127.0.0.1:5000/admin 访问后台。

### 环境变量配置

创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=sqlite:///blog.db
# 生产环境建议使用PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost:5432/xiaozhishi

# DEEPSEEK API KEY (用于AI内容生成)
DEEPSEEK_APIKEY=your-deepseek-api-key

# Flask配置
SECRET_KEY=your-secret-key-here
DEBUG=True

# 其他配置
FLASK_APP=run.py
FLASK_ENV=development
```

## Docker部署

### 使用Docker Compose（推荐）

1. **构建并启动服务**
```bash
docker-compose up -d --build
```

2. **初始化数据库**
```bash
docker-compose exec web python init_db.py
```

3. **创建管理员账户**
```bash
docker-compose exec web python create_admin.py
```

4. **查看日志**
```bash
docker-compose logs -f
```

### 使用Docker

1. **构建镜像**
```bash
docker build -t xiaozhishi .
```

2. **运行容器**
```bash
docker run -d \
  --name xiaozhishi \
  -p 5000:5000 \
  -e DATABASE_URL=sqlite:///blog.db \
  -e SECRET_KEY=your-secret-key \
  -e DEEPSEEK_APIKEY=your-api-key \
  xiaozhishi
```

## 生产环境部署

### 使用Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 运行应用
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### 使用Nginx反向代理

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/XiaoZhiShi/app/static;
    }

    location /uploads {
        alias /path/to/XiaoZhiShi/app/static/uploads;
    }
}
```

### 使用systemd服务

创建 `/etc/systemd/system/xiaozhishi.service`:

```ini
[Unit]
Description=XiaoZhiShi Blog
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/XiaoZhiShi
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 启用并启动服务
sudo systemctl enable xiaozhishi
sudo systemctl start xiaozhishi
```

## 使用说明

### 后台管理

访问 `/admin` 路径，使用管理员账户登录：

- **仪表盘**：查看系统概览
- **文章管理**：创建、编辑、删除文章
- **分类管理**：管理文章分类
- **标签管理**：管理文章标签
- **导航管理**：自定义前台导航菜单
- **用户管理**：管理系统用户
- **SEO设置**：配置网站SEO信息
- **系统设置**：网站基本设置

### AI内容生成

在后台的文章创建/编辑页面，可以使用AI生成功能：

1. 输入文章主题
2. 点击"AI生成内容"按钮
3. 系统会自动生成文章标题、内容、分类和SEO信息
4. 编辑并完善生成的内容
5. 发布文章

### 前台功能

- **首页**：展示最新文章
- **文章详情**：查看文章内容
- **分类页面**：按分类浏览文章
- **标签页面**：按标签浏览文章
- **搜索功能**：全文搜索文章
- **用户中心**：注册用户可管理自己的文章

## 开发指南

### 项目启动

```bash
# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 设置环境变量
export FLASK_APP=run.py
export FLASK_ENV=development

# 运行应用
flask run
```

### 数据库迁移

```bash
# 创建迁移
flask db migrate -m "描述变更"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

### 添加新功能

1. 在 `app/models/` 中添加数据模型
2. 在 `app/admin/` 或 `app/main/` 中添加视图函数
3. 在 `app/templates/` 中添加对应的模板
4. 在 `app/static/` 中添加静态资源
5. 更新数据库迁移

## 配置说明

### 数据库配置

支持SQLite和PostgreSQL：

```env
# SQLite (开发)
DATABASE_URL=sqlite:///blog.db

# PostgreSQL (生产)
DATABASE_URL=postgresql://username:password@localhost:5432/xiaozhishi
```

### AI配置

配置DEEPSEEK API：

```env
DEEPSEEK_APIKEY=your-api-key-here
```

### 邮件配置（可选）

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## API文档

项目提供RESTful API接口，通过 `/api` 前缀访问：

### 认证

```http
POST /api/auth/login
Content-Type: application/json

{
    "username": "user",
    "password": "password"
}
```

### 文章API

```http
# 获取文章列表
GET /api/posts

# 获取单篇文章
GET /api/posts/<id>

# 创建文章
POST /api/posts
Authorization: Bearer <token>

# 更新文章
PUT /api/posts/<id>
Authorization: Bearer <token>

# 删除文章
DELETE /api/posts/<id>
Authorization: Bearer <token>
```

详细的API文档请查看 `API_DOCUMENTATION.md`。

## 性能优化

### 数据库优化

- 使用索引优化查询
- 配置连接池
- 定期清理旧数据

### 缓存策略

- 使用Redis缓存热门文章
- 缓存分类和标签数据
- CDN加速静态资源

### 静态资源优化

- 压缩CSS和JavaScript
- 使用WebP格式图片
- 配置浏览器缓存

## 安全建议

1. **生产环境设置**：
   - 设置强SECRET_KEY
   - 禁用DEBUG模式
   - 使用HTTPS
   - 配置安全头部

2. **定期维护**：
   - 更新依赖包
   - 备份数据库
   - 监控日志
   - 定期审计

3. **访问控制**：
   - 限制后台访问IP
   - 使用强密码策略
   - 启用双因素认证（2FA）

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查DATABASE_URL配置
   - 确保数据库服务运行
   - 检查网络连接

2. **AI生成功能不可用**
   - 检查DEEPSEEK_APIKEY配置
   - 验证API密钥有效性
   - 检查网络连接

3. **静态文件加载失败**
   - 检查静态文件路径
   - 配置Nginx静态文件服务
   - 检查文件权限

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 查看错误日志
tail -f logs/error.log

# Docker环境
docker-compose logs -f web
```

## 贡献指南

欢迎贡献代码、报告问题或提出功能建议！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 更新日志

### v1.0.0 (2025-11-20)
- 初始版本发布
- 用户管理系统
- 文章管理功能
- 分类和标签系统
- AI内容生成
- SEO优化
- 响应式设计
- 媒体管理
- 导航管理

## 联系方式

- 项目地址: [https://github.com/yourusername/XiaoZhiShi](https://github.com/yourusername/XiaoZhiShi)
- 问题反馈: [Issues](https://github.com/yourusername/XiaoZhiShi/issues)
- 邮箱: zerwill@outlook.com
## 致谢

- [Flask](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [DEEPSEEK AI](https://deepseek.ai/)
- 所有贡献者和支持者

---

⭐ 如果这个项目对你有帮助，请给个星标支持！
