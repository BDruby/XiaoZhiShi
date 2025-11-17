from app import create_app
from app.utils.seo import get_seo_settings

def test_homepage_seo():
    app = create_app()
    
    # 创建一个测试请求上下文
    with app.test_request_context('/'):
        # 获取实际的SEO设置
        seo_settings = get_seo_settings()
        if seo_settings:
            print("后台SEO设置:")
            print(f"  站点标题: {seo_settings.site_title}")
            print(f"  站点描述: {seo_settings.site_description}")
            print(f"  站点关键词: {seo_settings.site_keywords}")
            print()
        
        # 测试渲染首页模板
        from flask import render_template_string
        
        # 模拟首页模板的meta_tags块内容
        homepage_meta_template = """
        {{ generate_meta_tags(
            title='首页'
        ) | safe }}
        """
        
        try:
            rendered_meta = render_template_string(homepage_meta_template)
            print("首页渲染的SEO标签:")
            print(rendered_meta)
            print()
            
            # 检查是否包含后台设置的描述和关键词
            if seo_settings:
                if seo_settings.site_description in rendered_meta:
                    print("✓ 首页正确使用了后台设置的描述")
                else:
                    print("✗ 首页未使用后台设置的描述")
                
                if seo_settings.site_keywords in rendered_meta:
                    print("✓ 首页正确使用了后台设置的关键词")
                else:
                    print("✗ 首页未使用后台设置的关键词")
        except Exception as e:
            print(f"渲染首页SEO标签时出错: {str(e)}")

if __name__ == "__main__":
    test_homepage_seo()