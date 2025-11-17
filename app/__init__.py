import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # 配置
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # 数据库配置 - 使用SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化扩展
    from app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager(app)
    jwt = JWTManager(app)
    
    # 登录管理配置
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问此页面。'
    
    # 必须添加用户加载回调
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 添加上下文处理器
    from app.utils.seo import get_seo_settings, register_seo_functions
    @app.context_processor
    def inject_seo_settings():
        return dict(seo_settings=get_seo_settings())
    
    # 注册SEO函数
    register_seo_functions(app)
    
    # 注册蓝图
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    from .media import bp as media_bp
    app.register_blueprint(media_bp)
    
    from .admin.seo import bp as seo_bp
    app.register_blueprint(seo_bp)
    
    return app