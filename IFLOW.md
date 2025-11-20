# XiaoZhiShi (小智识) - 博客系统项目文档

## 项目概述

XiaoZhiShi (小智识) 是一个现代化的博客内容管理系统 (CMS)，采用 Flask 框架开发。该项目提供了一个完整的博客平台，支持用户管理、文章发布、分类标签系统、SEO 优化以及 AI 内容生成等功能。

### 核心特性

1. **用户管理系统**：支持用户注册、登录、角色管理（普通用户、编辑、管理员）
2. **内容管理**：支持文章创建、编辑、发布、分类和标签管理
3. **AI 内容生成**：集成 DEEPSEEK AI API，可自动生成博客内容
4. **SEO 优化**：全面的 SEO 支持，包括 meta 标签、Open Graph、Twitter Card、sitemap.xml 和 robots.txt
5. **响应式设计**：适配各种设备的前端界面
6. **媒体管理**：支持上传和管理媒体文件

### 技术栈

- **后端框架**: Flask 2.3.2
- **数据库**: SQLAlchemy (支持 SQLite, PostgreSQL)
- **前端模板**: Jinja2
- **表单处理**: Flask-WTF
- **用户认证**: Flask-Login
- **API 支持**: Flask-JWT-Extended
- **数据库迁移**: Flask-Migrate
- **AI 集成**: OpenAI SDK (用于调用 DEEPSEEK API)
- **其他依赖**: 详见 requirements.txt

## 项目结构

```
XiaoZhiShi/
├── app.py                 # 应用工厂创建
├── run.py                 # 应用运行入口
├── requirements.txt       # 项目依赖
├── .env                  # 环境变量配置
├── app/                  # 主应用目录
│   ├── __init__.py       # 应用工厂
│   ├── admin/            # 管理后台模块
│   ├── api/              # API 接口模块
│   ├── auth/             # 用户认证模块
│   ├── main/             # 前端主功能模块
│   ├── media/            # 媒体文件管理模块
│   ├── models/           # 数据模型
│   ├── static/           # 静态资源 (CSS, JS, 上传文件)
│   ├── templates/        # HTML 模板
│   └── utils/            # 工具函数
├── instance/             # 实例目录 (包含数据库文件)
├── migrations/           # 数据库迁移文件
└── ...
```

## 数据模型

### 用户模型 (User)
- 用户名、邮箱、密码哈希
- 姓名、个人简介、头像
- 角色 (user, editor, admin)
- 激活状态、创建/更新时间

### 文章模型 (Post)
- 标题、URL别名、内容、摘要
- 特色图片、状态 (草稿/已发布/归档)
- 访问量、作者、分类
- SEO 相关字段 (SEO标题、描述、关键词、OG图片)

### 分类模型 (Category)
- 名称、URL别名、描述
- 父级分类 (支持层级结构)
- SEO 相关字段

### 标签模型 (Tag)
- 名称、URL别名
- 与文章的多对多关系

### 评论模型 (Comment)
- 内容、用户、文章
- 父级评论 (支持嵌套评论)
- 状态管理

## 功能模块

### 管理后台 (Admin)
- 用户管理 (创建、编辑、删除)
- 文章管理 (创建、编辑、删除)
- 分类管理 (创建、编辑、删除，支持层级)
- 标签管理 (创建、编辑、删除)
- SEO 设置管理
- AI 内容生成工具

### 前端功能 (Main)
- 首页展示文章列表
- 文章详情页
- 分类文章页
- 搜索功能
- 用户仪表盘 (管理个人文章)
- 个人文章创建/编辑

### 认证系统 (Auth)
- 用户登录/注册/登出
- 邮箱或用户名登录
- 用户角色权限控制

### SEO 系统 (Utils/SEO)
- 自动生成 meta 标签
- Open Graph 和 Twitter Card 支持
- 动态 sitemap.xml 生成
- 动态 robots.txt 生成

### AI 集成 (Utils/AI)
- 基于 DEEPSEEK API 的内容生成
- 生成完整博客文章 (标题、内容、分类、SEO信息)

## 环境配置

### 环境变量
项目使用 .env 文件配置环境变量：

```
# 数据库配置
DATABASE_URL=sqlite:///blog.db

# DEEPSEEK API KEY (用于AI内容生成)
DEEPSEEK_APIKEY=your-deepseek-api-key

# Flask配置
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 依赖安装

```bash
pip install -r requirements.txt
```

## 构建和运行

### 初始化数据库

```bash
python init_db.py
```

### 运行应用

```bash
python run.py
```

或使用 Flask 命令：

```bash
flask run
```

### 创建管理员账户

运行以下命令创建管理员账户：

```bash
python create_admin.py
```

## 开发约定

### 代码风格
- 遵循 PEP 8 Python 编码规范
- 使用 Flask 标准模式和最佳实践
- 模型使用 SQLAlchemy ORM
- 表单使用 Flask-WTF

### 数据库操作
- 使用 Flask-Migrate 进行数据库迁移
- 所有数据库操作通过模型方法进行
- 事务处理和异常处理

### 前端模板
- 使用 Jinja2 模板引擎
- 遵循响应式设计原则
- SEO 友好性考虑

### 安全性
- 密码哈希存储
- CSRF 保护
- 用户权限验证
- 输入验证和过滤

## API 接口

项目包含 RESTful API 接口支持，通过 `/api/` 前缀访问。

## 部署说明

### 生产环境配置
- 将 DEBUG 设置为 False
- 使用更安全的 SECRET_KEY
- 配置生产数据库 (推荐 PostgreSQL)
- 配置反向代理 (Nginx)
- 使用 Gunicorn 运行应用

### 部署命令示例

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## 扩展功能

### AI 内容生成
项目集成了 DEEPSEEK AI API，可以：
- 根据主题自动生成文章内容
- 包含标题、摘要、分类、SEO 信息
- 自动格式化为 HTML 内容

### SEO 优化
- 完整的 meta 标签支持
- 动态生成 Open Graph 和 Twitter Card
- 自定义 sitemap.xml 和 robots.txt
- 规范 URL 支持

### 媒体管理
- 文件上传和管理
- 图片缩略图生成
- 媒体文件元数据管理

## 项目维护

### 数据库迁移
使用 Flask-Migrate 管理数据库结构变更：

```bash
flask db migrate -m "描述变更"
flask db upgrade
```

### 日志记录
项目记录关键操作和错误日志，便于调试和维护。

## 总结

XiaoZhiShi 是一个功能丰富的现代化博客系统，具备完整的用户管理、内容管理、SEO 优化和 AI 集成功能。项目结构清晰，代码规范，易于扩展和维护。