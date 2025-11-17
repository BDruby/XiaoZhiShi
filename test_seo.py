#!/usr/bin/env python3
"""
SEO功能测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, SeoSetting

def test_seo_settings():
    """测试SEO设置功能"""
    app = create_app()
    
    with app.app_context():
        # 创建或获取SEO设置
        seo_setting = SeoSetting.query.first()
        if not seo_setting:
            seo_setting = SeoSetting()
            db.session.add(seo_setting)
        
        # 设置测试值
        seo_setting.site_title = "测试博客系统"
        seo_setting.site_description = "这是一个用于测试SEO功能的博客系统"
        seo_setting.site_keywords = "测试,SEO,博客"
        seo_setting.site_author = "测试用户"
        seo_setting.google_analytics_id = "UA-12345678-1"
        
        try:
            db.session.commit()
            print("✓ SEO设置保存成功")
        except Exception as e:
            db.session.rollback()
            print(f"✗ SEO设置保存失败: {e}")
            return False
        
        # 验证设置
        seo_setting = SeoSetting.query.first()
        if seo_setting and seo_setting.site_title == "测试博客系统":
            print("✓ SEO设置验证成功")
            return True
        else:
            print("✗ SEO设置验证失败")
            return False

def test_seo_meta_tags():
    """测试SEO元标签生成功能"""
    try:
        from app.utils.seo import generate_meta_tags, get_seo_settings
        
        app = create_app()
        with app.app_context():
            # 获取SEO设置
            seo_settings = get_seo_settings()
            if seo_settings:
                print("✓ SEO设置获取成功")
                
                # 生成元标签
                meta_tags = generate_meta_tags(
                    title="测试页面",
                    description="这是一个测试页面的描述",
                    keywords="测试,页面",
                    og_image="/static/test-image.jpg"
                )
                
                if meta_tags and "测试页面" in meta_tags:
                    print("✓ SEO元标签生成成功")
                    return True
                else:
                    print("✗ SEO元标签生成失败")
                    return False
            else:
                print("✗ 无法获取SEO设置")
                return False
    except Exception as e:
        print(f"✗ SEO元标签测试失败: {e}")
        return False

def main():
    """主函数"""
    print("开始测试SEO功能...")
    
    # 测试SEO设置
    if not test_seo_settings():
        print("SEO设置测试失败")
        return 1
    
    # 测试SEO元标签
    if not test_seo_meta_tags():
        print("SEO元标签测试失败")
        return 1
    
    print("\n所有SEO功能测试通过!")
    return 0

if __name__ == "__main__":
    sys.exit(main())