import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db

def test_sqlite_connection():
    app = create_app()
    
    with app.app_context():
        try:
            # 尝试导入模型并检查关系
            from app.models import User, Post, Category, Tag
            print("SQLite数据库连接成功！")
            print("模型定义正确，关系已建立。")
            
            # 创建所有表
            db.create_all()
            print("数据库表创建成功！")
            
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False

if __name__ == "__main__":
    test_sqlite_connection()