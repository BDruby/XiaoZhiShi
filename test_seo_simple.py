import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, SeoSetting

def test_seo_functionality():
    app = create_app()
    
    with app.app_context():
        # 检查SEO设置表是否存在并创建默认设置
        seo_setting = SeoSetting.query.first()
        if not seo_setting:
            print("创建默认SEO设置...")
            seo_setting = SeoSetting(
                site_title="小芝士博客",
                site_description="分享知识和经验的现代化博客系统",
                site_keywords="博客,技术分享,知识",
                site_author="小芝士团队"
            )
            db.session.add(seo_setting)
            db.session.commit()
            print("默认SEO设置已创建")
        else:
            print("SEO设置已存在")
        
        # 验证设置
        seo_setting = SeoSetting.query.first()
        print(f"站点标题: {seo_setting.site_title}")
        print(f"站点描述: {seo_setting.site_description}")
        print("SEO功能测试完成!")

if __name__ == "__main__":
    test_seo_functionality()