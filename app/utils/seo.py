from flask import request, url_for
from app.models import SeoSetting, Post, Category

def get_seo_settings():
    """获取SEO设置"""
    return SeoSetting.query.first()

def generate_meta_tags(title=None, description=None, keywords=None, og_image=None, og_type='website', canonical_url=None):
    """生成SEO元标签"""
    seo_settings = get_seo_settings()
    
    # 基本SEO设置
    site_title = seo_settings.site_title if seo_settings else '现代化博客系统'
    site_description = seo_settings.site_description if seo_settings else ''
    site_keywords = seo_settings.site_keywords if seo_settings else ''
    site_author = seo_settings.site_author if seo_settings else ''
    og_image_default = seo_settings.og_image if seo_settings else ''
    twitter_handle = seo_settings.twitter_handle if seo_settings else ''
    default_canonical = seo_settings.default_canonical_url if seo_settings else None
    
    # 页面特定设置
    page_title = title or ''
    page_description = description or ''
    page_keywords = keywords or ''
    page_og_image = og_image or ''
    
    # 构建最终值
    final_title = f"{page_title} - {site_title}" if page_title else site_title
    final_description = page_description or site_description
    final_keywords = page_keywords or site_keywords
    final_og_image = page_og_image or og_image_default
    
    # 生成元标签
    meta_tags = []
    
    # 基本元标签
    meta_tags.append(f'<title>{final_title}</title>')
    meta_tags.append(f'<meta name="description" content="{final_description}">')
    
    if final_keywords:
        meta_tags.append(f'<meta name="keywords" content="{final_keywords}">')
    
    if site_author:
        meta_tags.append(f'<meta name="author" content="{site_author}">')
    
    # Open Graph标签
    meta_tags.append(f'<meta property="og:title" content="{final_title}">')
    meta_tags.append(f'<meta property="og:description" content="{final_description}">')
    meta_tags.append(f'<meta property="og:type" content="{og_type}">')
    
    # 获取当前URL
    current_url = request.url
    meta_tags.append(f'<meta property="og:url" content="{current_url}">')
    
    if final_og_image:
        meta_tags.append(f'<meta property="og:image" content="{final_og_image}">')
    
    # Twitter Card标签
    meta_tags.append('<meta name="twitter:card" content="summary_large_image">')
    if twitter_handle:
        meta_tags.append(f'<meta name="twitter:site" content="{twitter_handle}">')
    meta_tags.append(f'<meta name="twitter:title" content="{final_title}">')
    meta_tags.append(f'<meta name="twitter:description" content="{final_description}">')
    if final_og_image:
        meta_tags.append(f'<meta name="twitter:image" content="{final_og_image}">')
    
    # 规范URL - 优先级: 1. 传入的canonical_url 2. 默认规范URL 3. 当前URL
    if canonical_url:
        meta_tags.append(f'<link rel="canonical" href="{canonical_url}">')
    elif default_canonical:
        meta_tags.append(f'<link rel="canonical" href="{default_canonical}">')
    else:
        meta_tags.append(f'<link rel="canonical" href="{current_url}">')
    
    # 自定义代码
    if seo_settings and seo_settings.custom_head_code:
        meta_tags.append(seo_settings.custom_head_code)
    
    return '\n    '.join(meta_tags)

def get_post_seo_data(post):
    """获取文章SEO数据"""
    # 文章特定SEO设置优先
    title = post.seo_title or post.title
    description = post.seo_description or (post.excerpt[:160] if post.excerpt else '')
    keywords = post.seo_keywords or ''
    og_image = post.seo_og_image or (post.featured_image if post.featured_image else '')
    
    # 规范URL
    canonical_url = url_for('main.post_detail', slug=post.slug, _external=True)
    
    return {
        'title': title,
        'description': description,
        'keywords': keywords,
        'og_image': og_image,
        'canonical_url': canonical_url
    }

def get_category_seo_data(category):
    """获取分类SEO数据"""
    # 分类特定SEO设置优先
    title = category.seo_title or category.name
    description = category.seo_description or (category.description[:160] if category.description else '')
    keywords = category.seo_keywords or ''
    
    # 规范URL
    canonical_url = url_for('main.category_posts', slug=category.slug, _external=True)
    
    return {
        'title': title,
        'description': description,
        'keywords': keywords,
        'canonical_url': canonical_url
    }

def get_search_seo_data(query):
    """获取搜索页面SEO数据"""
    seo_settings = get_seo_settings()
    site_title = seo_settings.site_title if seo_settings else '现代化博客系统' if seo_settings else '现代化博客系统'
    
    title = f"搜索结果：{query} - {site_title}" if query else f"搜索 - {site_title}"
    description = f"关于 '{query}' 的搜索结果" if query else "网站搜索页面"
    keywords = query if query else ''
    canonical_url = url_for('main.search', q=query, _external=True) if query else url_for('main.search', _external=True)
    
    return {
        'title': title,
        'description': description,
        'keywords': keywords,
        'canonical_url': canonical_url
    }

def register_seo_functions(app):
    """注册SEO相关函数到应用上下文"""
    @app.context_processor
    def inject_seo_functions():
        return dict(
            get_post_seo_data=get_post_seo_data,
            get_category_seo_data=get_category_seo_data,
            get_search_seo_data=get_search_seo_data,
            generate_meta_tags=generate_meta_tags
        )