from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

db = SQLAlchemy()

# 关联表 - 文章和标签
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default='user')  # user, editor, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    posts = db.relationship('Post', backref='author', lazy=True, foreign_keys='Post.user_id')
    comments = db.relationship('Comment', backref='author', lazy=True, foreign_keys='Comment.user_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # SEO字段
    seo_title = db.Column(db.String(200), nullable=True)
    seo_description = db.Column(db.Text, nullable=True)
    seo_keywords = db.Column(db.Text, nullable=True)
    
    # 自关联关系
    parent = db.relationship('Category', remote_side=[id], backref='subcategories')
    posts = db.relationship('Post', backref='category', lazy=True)


class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', secondary=post_tags, backref='tags')


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text, nullable=True)
    featured_image = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='draft')  # draft, published, archived
    view_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # SEO字段
    seo_title = db.Column(db.String(200), nullable=True)
    seo_description = db.Column(db.Text, nullable=True)
    seo_keywords = db.Column(db.Text, nullable=True)
    seo_og_image = db.Column(db.String(255), nullable=True)
    
    # 关系
    comments = db.relationship('Comment', backref='post', lazy=True)


class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, approved, spam, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 自关联关系
    parent = db.relationship('Comment', remote_side=[id], backref='replies')


class Media(db.Model):
    __tablename__ = 'media'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # in bytes
    mime_type = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alt_text = db.Column(db.String(255), nullable=True)
    caption = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='media_files')


class Setting(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    type = db.Column(db.String(50), default='string')  # string, integer, boolean, json
    description = db.Column(db.String(500), nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SeoSetting(db.Model):
    __tablename__ = 'seo_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String(200), nullable=True)
    site_description = db.Column(db.Text, nullable=True)
    site_keywords = db.Column(db.Text, nullable=True)
    site_author = db.Column(db.String(100), nullable=True)
    site_logo = db.Column(db.String(255), nullable=True)
    favicon = db.Column(db.String(255), nullable=True)
    google_analytics_id = db.Column(db.String(50), nullable=True)
    baidu_analytics_id = db.Column(db.String(50), nullable=True)
    social_media_links = db.Column(db.Text, nullable=True)  # JSON格式存储社交媒体链接
    custom_head_code = db.Column(db.Text, nullable=True)  # 自定义<head>代码
    robots_txt = db.Column(db.Text, nullable=True)
    sitemap_url = db.Column(db.String(255), nullable=True)
    twitter_handle = db.Column(db.String(50), nullable=True)  # Twitter账号
    og_image = db.Column(db.String(255), nullable=True)  # 默认Open Graph图片
    default_canonical_url = db.Column(db.String(255), nullable=True)  # 默认规范URL
    sitemap_lastmod = db.Column(db.DateTime, nullable=True)  # sitemap最后修改时间
    robots_txt_lastmod = db.Column(db.DateTime, nullable=True)  # robots.txt最后修改时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)