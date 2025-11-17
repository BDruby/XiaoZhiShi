from jinja2 import Environment, DictLoader

# 模拟SEO设置对象
class MockSeoSetting:
    def __init__(self):
        self.site_title = "超级个体试验场：AIGC/AGENT CLI/AI工具教程/vibe coding | AI变现进阶指南 | 小芝士"
        self.site_description = "小芝士博客专注于AIGC、IFLOW CLI、vibe coding等前沿AI技术和命令行工具实战教程"
        self.site_keywords = "AI, AIGC, IFLOW CLI"
        self.site_author = "THE RED STON"
        self.og_image = ""
        self.twitter_handle = "@richBD9"
        self.custom_head_code = ""

# 模拟模板环境
templates = {
    'test': '''
{# 使用更可靠的条件判断 #}
{% if seo_settings %}
    {% set site_title = seo_settings.site_title or '现代化博客系统' %}
    {% set site_description = seo_settings.site_description or '' %}
    {% set site_keywords = seo_settings.site_keywords or '' %}
    {% set site_author = seo_settings.site_author or '' %}
    {% set og_image_default = seo_settings.og_image or '' %}
    {% set twitter_handle = seo_settings.twitter_handle or '' %}
{% else %}
    {% set site_title = '现代化博客系统' %}
    {% set site_description = '' %}
    {% set site_keywords = '' %}
    {% set site_author = '' %}
    {% set og_image_default = '' %}
    {% set twitter_handle = '' %}
{% endif %}

{% set final_title = (title + ' - ' + site_title) if title and title != '' else site_title %}
{% set final_description = description if description and description != '' else site_description %}
{% set final_keywords = keywords if keywords and keywords != '' else site_keywords %}
{% set final_og_image = og_image if og_image and og_image != '' else og_image_default %}

<title>{{ final_title }}</title>
<meta name="description" content="{{ final_description }}">
'''
}

env = Environment(loader=DictLoader(templates))

# 测试1: 空字符串参数
template = env.get_template('test')
seo_settings = MockSeoSetting()

result1 = template.render(
    seo_settings=seo_settings,
    title='',
    description='',
    keywords=''
)

print("测试1 - 空字符串参数:")
print(result1)
print()

# 测试2: None参数
result2 = template.render(
    seo_settings=seo_settings,
    title=None,
    description=None,
    keywords=None
)

print("测试2 - None参数:")
print(result2)
print()

# 测试3: 带值参数
result3 = template.render(
    seo_settings=seo_settings,
    title='首页',
    description='欢迎来到首页',
    keywords='首页,博客'
)

print("测试3 - 带值参数:")
print(result3)