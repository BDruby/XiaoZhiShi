import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import SeoSetting

def check_seo_settings():
    app = create_app()
    
    with app.app_context():
        seo_setting = SeoSetting.query.first()
        if seo_setting:
            print("当前SEO设置:")
            print(f"  站点标题: {seo_setting.site_title}")
            print(f"  站点描述: {seo_setting.site_description}")
            print(f"  站点关键词: {seo_setting.site_keywords}")
            print(f"  站点作者: {seo_setting.site_author}")
            print(f"  Twitter账号: {seo_setting.twitter_handle}")
            print(f"  默认OG图片: {seo_setting.og_image}")
        else:
            print("未找到SEO设置")

if __name__ == "__main__":
    check_seo_settings()