import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, Navigation

def init_database():
    app = create_app()
    
    with app.app_context():
        try:
            # 创建所有表
            db.create_all()
            print("数据库表创建成功！")
            
            # 检查是否已有导航项，如果没有则创建默认导航
            if Navigation.query.count() == 0:
                # 创建默认导航项
                default_nav = Navigation(
                    name='首页',
                    title='首页',
                    url='/',
                    position=0,
                    is_active=True
                )
                db.session.add(default_nav)
                db.session.commit()
                print("默认导航项已创建")
            
            return True
        except Exception as e:
            print(f"数据库表创建失败: {e}")
            return False

if __name__ == "__main__":
    init_database()