from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Post, Category

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