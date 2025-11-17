from app import create_app

def test_seo_context_processor():
    app = create_app()
    
    with app.app_context():
        # 检查上下文处理器是否已注册
        print("检查上下文处理器注册状态:")
        
        # 获取所有上下文处理器
        context_processors = app.template_context_processors[None]
        print(f"注册的上下文处理器数量: {len(context_processors)}")
        
        # 执行所有上下文处理器并合并结果
        merged_context = {}
        for processor in context_processors:
            if callable(processor):
                try:
                    result = processor()
                    if isinstance(result, dict):
                        merged_context.update(result)
                except Exception as e:
                    print(f"执行上下文处理器时出错: {str(e)}")
        
        print(f"合并后的上下文键: {list(merged_context.keys())}")
        
        if 'seo_settings' in merged_context:
            seo_settings = merged_context['seo_settings']
            print(f"SEO设置对象类型: {type(seo_settings)}")
            if seo_settings:
                print(f"站点标题: {seo_settings.site_title}")
                print(f"站点描述: {seo_settings.site_description[:50]}...")
            else:
                print("SEO设置对象为None")
        
        # 测试渲染一个简单的模板以验证上下文处理器
        from flask import render_template_string
        test_template = """
        <html>
        <head>
            <title>{{ seo_settings.site_title if seo_settings else '默认标题' }}</title>
            <meta name="description" content="{{ seo_settings.site_description if seo_settings else '默认描述' }}">
        </head>
        <body>
            <h1>测试页面</h1>
        </body>
        </html>
        """
        
        try:
            rendered = render_template_string(test_template)
            print("\n模板渲染成功！")
            # 检查渲染结果是否包含实际的SEO设置信息
            if "超级个体试验场" in rendered:
                print("渲染结果包含实际SEO设置信息")
            else:
                print("渲染结果使用默认值或未正确获取SEO设置")
        except Exception as e:
            print(f"模板渲染失败: {str(e)}")

if __name__ == "__main__":
    test_seo_context_processor()