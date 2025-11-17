from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, current_app
from flask_login import login_required, current_user
from app.models import db, Post, Category
from app.utils.seo import get_seo_settings
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).limit(10).all()
    return render_template('main/index.html', posts=posts)

@bp.route('/post/<slug>')
def post_detail(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('main/post_detail.html', post=post)

@bp.route('/category/<slug>')
def category_posts(slug):
    from app.models import Category
    category = Category.query.filter_by(slug=slug).first_or_404()
    posts = Post.query.filter_by(category=category, status='published').order_by(Post.created_at.desc()).all()
    return render_template('main/category.html', category=category, posts=posts)

@bp.route('/dashboard')
@login_required
def dashboard():
    # 获取当前用户的文章
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('main/dashboard.html', posts=posts)

@bp.route('/dashboard/posts/create', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        try:
            # 检查必需字段
            title = request.form.get('title', '').strip()
            slug = request.form.get('slug', '').strip()
            content = request.form.get('content', '').strip()
            
            if not title or not slug or not content:
                flash('标题、URL别名和内容是必填项', 'error')
                categories = Category.query.all()
                return render_template('main/create_post.html', categories=categories)
            
            post = Post(
                title=title,
                slug=slug,
                content=content,
                excerpt=request.form.get('excerpt', ''),
                status=request.form.get('status', 'draft'),
                user_id=current_user.id
            )
            
            # 处理分类
            category_id = request.form.get('category_id')
            if category_id:
                post.category_id = category_id
                
            db.session.add(post)
            db.session.commit()
            flash('文章创建成功', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'创建文章时出错: {str(e)}', 'error')
            print(f"创建文章错误: {e}")  # 服务器端日志
            
    categories = Category.query.all()
    return render_template('main/create_post.html', categories=categories)

@bp.route('/dashboard/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    # 确保用户只能编辑自己的文章
    if post.user_id != current_user.id:
        flash('您没有权限编辑此文章', 'error')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        try:
            # 检查必需字段
            title = request.form.get('title', '').strip()
            slug = request.form.get('slug', '').strip()
            content = request.form.get('content', '').strip()
            
            if not title or not slug or not content:
                flash('标题、URL别名和内容是必填项', 'error')
                categories = Category.query.all()
                return render_template('main/edit_post.html', post=post, categories=categories)
            
            post.title = title
            post.slug = slug
            post.content = content
            post.excerpt = request.form.get('excerpt', '')
            post.status = request.form.get('status', post.status)
            
            # 处理分类
            category_id = request.form.get('category_id')
            post.category_id = category_id if category_id else None
                
            db.session.commit()
            flash('文章更新成功', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新文章时出错: {str(e)}', 'error')
            print(f"更新文章错误: {e}")  # 服务器端日志
            
    categories = Category.query.all()
    return render_template('main/edit_post.html', post=post, categories=categories)

@bp.route('/dashboard/posts/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    # 确保用户只能删除自己的文章
    if post.user_id != current_user.id:
        flash('您没有权限删除此文章', 'error')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(post)
    db.session.commit()
    flash('文章删除成功', 'success')
    return redirect(url_for('main.dashboard'))

@bp.route('/sitemap.xml')
def sitemap():
    """生成sitemap.xml"""
    from app.models import Post, Category
    from flask import url_for
    import xml.etree.ElementTree as ET
    from xml.dom import minidom

    # 获取SEO设置和所有文章、分类
    seo_settings = get_seo_settings()
    posts = Post.query.filter_by(status='published').all()
    categories = Category.query.all()
    
    # 创建XML结构
    urlset = ET.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # 添加首页
    url = ET.SubElement(urlset, 'url')
    loc = ET.SubElement(url, 'loc')
    loc.text = url_for('main.index', _external=True)
    lastmod = ET.SubElement(url, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
    changefreq = ET.SubElement(url, 'changefreq')
    changefreq.text = 'daily'
    priority = ET.SubElement(url, 'priority')
    priority.text = '1.0'
    
    # 添加分类页面
    for category in categories:
        url = ET.SubElement(urlset, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = url_for('main.category_posts', slug=category.slug, _external=True)
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = category.created_at.strftime('%Y-%m-%dT%H:%M:%S+00:00') if category.created_at else datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'weekly'
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.8'
    
    # 添加文章页面
    for post in posts:
        url = ET.SubElement(urlset, 'url')
        loc = ET.SubElement(url, 'loc')
        loc.text = url_for('main.post_detail', slug=post.slug, _external=True)
        lastmod = ET.SubElement(url, 'lastmod')
        lastmod.text = post.updated_at.strftime('%Y-%m-%dT%H:%M:%S+00:00') if post.updated_at else post.created_at.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        changefreq = ET.SubElement(url, 'changefreq')
        changefreq.text = 'weekly'
        priority = ET.SubElement(url, 'priority')
        priority.text = '0.7'
    
    # 格式化XML
    rough_string = ET.tostring(urlset, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
    
    # 更新SEO设置中的最后修改时间
    if seo_settings:
        seo_settings.sitemap_lastmod = datetime.now()
        db.session.commit()
    
    # 创建响应
    response = make_response(pretty_xml)
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/robots.txt')
def robots_txt():
    """生成robots.txt"""
    from app.models import SeoSetting
    
    # 获取SEO设置
    seo_setting = SeoSetting.query.first()
    custom_robots_txt = seo_setting.robots_txt if seo_setting and seo_setting.robots_txt else ''
    
    # 如果没有自定义内容，生成默认内容
    if not custom_robots_txt or custom_robots_txt.strip() == '':
        # 生成默认robots.txt内容，包含后台路径的Disallow规则
        robots_content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /login
Disallow: /logout
Disallow: /register
Disallow: /dashboard

Sitemap: """ + url_for('main.sitemap', _external=True)
    else:
        robots_content = custom_robots_txt
    
    # 更新SEO设置中的最后修改时间
    if seo_setting:
        seo_setting.robots_txt_lastmod = datetime.now()
        db.session.commit()
    
    response = make_response(robots_content)
    response.headers['Content-Type'] = 'text/plain'
    return response