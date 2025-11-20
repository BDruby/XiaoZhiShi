from app import create_app
from app.models import Navigation

app = create_app()
with app.app_context():
    navigations = Navigation.query.all()
    print(f'导航项数量: {len(navigations)}')
    for nav in navigations:
        print(f'ID: {nav.id}, 名称: {nav.name}, 标题: {nav.title}, URL: {nav.url}, 激活: {nav.is_active}, 位置: {nav.position}')