import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db

def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            # 创建所有表
            db.create_all()
            print("数据库表创建成功！")
            return True
        except Exception as e:
            print(f"数据库表创建失败: {e}")
            return False

if __name__ == "__main__":
    init_database()