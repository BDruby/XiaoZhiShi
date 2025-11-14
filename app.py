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
    
    # 数据库配置
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    
    # 对用户名和密码进行URL编码以处理特殊字符
    import urllib.parse
    encoded_username = urllib.parse.quote_plus(db_username)
    encoded_password = urllib.parse.quote_plus(db_password)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{encoded_username}:{encoded_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化扩展
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager(app)
    jwt = JWTManager(app)
    
    # 登录管理配置
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录以访问此页面。'
    
    # 注册蓝图
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    from .main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])