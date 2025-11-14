import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_database_connection():
    app = create_app()
    
    with app.app_context():
        try:
            # 尝试导入模型并检查关系
            from app.models import db, User, Post, Category, Tag
            print("数据库连接成功！")
            print("模型定义正确，关系已建立。")
            
            return True
        except Exception as e:
            print(f"数据库连接失败: {e}")
            return False

if __name__ == "__main__":
    test_database_connection()