import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_context_processor():
    app = create_app()
    
    with app.app_context():
        # 直接测试get_seo_settings函数
        from app.utils.seo import get_seo_settings
        seo_settings = get_seo_settings()
        if seo_settings:
            print("直接调用get_seo_settings函数:")
            print(f"  站点标题: {seo_settings.site_title}")
            print(f"  站点描述: {seo_settings.site_description}")
        else:
            print("get_seo_settings函数返回None")
        
        # 测试上下文处理器 - 需要调用app.context_processor装饰器函数
        from app.utils.seo import get_seo_settings
        seo_ctx = get_seo_settings()
        print(f"\n手动获取SEO设置结果类型: {type(seo_ctx)}")
        if seo_ctx:
            print(f"  标题: {seo_ctx.site_title if hasattr(seo_ctx, 'site_title') else 'N/A'}")

if __name__ == "__main__":
    test_context_processor()