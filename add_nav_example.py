from app import create_app
from app.models import Navigation, db

app = create_app()
with app.app_context():
    # 检查是否已有示例导航项
    example_nav = Navigation.query.filter_by(name='示例导航').first()
    if not example_nav:
        # 创建一个示例导航项
        example_nav = Navigation(
            name='示例导航',
            title='关于我们',
            url='/about',
            position=1,
            is_active=True
        )
        db.session.add(example_nav)
        
        # 创建另一个示例导航项
        example_nav2 = Navigation(
            name='博客',
            title='博客',
            url='/blog',
            position=2,
            is_active=True
        )
        db.session.add(example_nav2)
        
        db.session.commit()
        print("已添加示例导航项")
    else:
        print("示例导航项已存在")
    
    # 显示所有导航项
    navigations = Navigation.query.order_by(Navigation.position.asc()).all()
    print(f'当前导航项数量: {len(navigations)}')
    for nav in navigations:
        print(f'ID: {nav.id}, 名称: {nav.name}, 标题: {nav.title}, URL: {nav.url}, 激活: {nav.is_active}, 位置: {nav.position}')