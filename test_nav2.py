from app import create_app
from app.models import Navigation

app = create_app()
with app.app_context():
    # 查询所有导航项
    all_navs = Navigation.query.all()
    print(f'总导航项数量: {len(all_navs)}')
for nav in all_navs:
    print(f'ID: {nav.id}, 名称: {nav.name}, 标题: {nav.title}, URL: {nav.url}, 激活: {nav.is_active}, 位置: {nav.position}')