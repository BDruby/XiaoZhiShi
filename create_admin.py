import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User

def create_admin_user():
    app = create_app()
    
    with app.app_context():
        # 检查是否已存在管理员账户
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("管理员账户已存在")
            return
        
        # 创建管理员账户
        admin = User(
            username='admin',
            email='admin@xiaozhishi.com',
            first_name='管理员',
            last_name='',
            role='admin'
        )
        admin.set_password('admin123')  # 设置默认密码
        
        db.session.add(admin)
        db.session.commit()
        
        print("管理员账户创建成功！")
        print("用户名: admin")
        print("默认密码: admin123")
        print("请登录后立即修改密码！")

if __name__ == "__main__":
    create_admin_user()