from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, User, Post, Category, Tag
from app.auth.forms import RegisterForm
from sqlalchemy import func

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.before_request
@login_required
def check_admin():
    # 检查用户是否为管理员
    if current_user.role not in ['admin', 'editor']:
        flash('您没有权限访问管理后台', 'error')
        return redirect(url_for('main.index'))

@bp.route('/')
def dashboard():
    # 统计数据
    user_count = User.query.count()
    post_count = Post.query.count()
    category_count = Category.query.count()
    tag_count = Tag.query.count()
    
    # 最近的文章
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # 最近的用户
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count,
                          post_count=post_count,
                          category_count=category_count,
                          tag_count=tag_count,
                          recent_posts=recent_posts,
                          recent_users=recent_users)

@bp.route('/users')
def users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/users/index.html', users=users)

@bp.route('/users/create', methods=['GET', 'POST'])
def create_user():
    form = RegisterForm()
    # 移除确认密码的验证，因为我们是在管理员创建用户
    del form.password2
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=request.form.get('role', 'user')
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('用户创建成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/create.html', form=form)

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)
    form = RegisterForm(obj=user)
    # 移除确认密码的验证
    del form.password2
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.role = request.form.get('role', user.role)
        
        # 只有在输入新密码时才更新密码
        if form.password.data:
            user.set_password(form.password.data)
            
        db.session.commit()
        flash('用户信息更新成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/edit.html', form=form, user=user)

@bp.route('/users/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('不能删除自己的账户', 'error')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.users'))

# 文章管理
@bp.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/posts/index.html', posts=posts)

@bp.route('/posts/create', methods=['GET', 'POST'])
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
                return render_template('admin/posts/create.html', categories=categories)
            
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
            return redirect(url_for('admin.posts'))
        except Exception as e:
            db.session.rollback()
            flash(f'创建文章时出错: {str(e)}', 'error')
            print(f"创建文章错误: {e}")  # 服务器端日志
            
    categories = Category.query.all()
    return render_template('admin/posts/create.html', categories=categories)

@bp.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            post.title = request.form['title']
            post.slug = request.form['slug']
            post.content = request.form['content']
            post.excerpt = request.form.get('excerpt', '')
            post.status = request.form.get('status', post.status)
            
            # 处理分类
            category_id = request.form.get('category_id')
            post.category_id = category_id if category_id else None
                
            db.session.commit()
            flash('文章更新成功', 'success')
            return redirect(url_for('admin.posts'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新文章时出错: {str(e)}', 'error')
            print(f"更新文章错误: {e}")  # 服务器端日志
    
    categories = Category.query.all()
    return render_template('admin/posts/edit.html', post=post, categories=categories)

@bp.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('文章删除成功', 'success')
    return redirect(url_for('admin.posts'))

# 分类管理
@bp.route('/categories')
def categories():
    categories = Category.query.order_by(Category.created_at.desc()).all()
    return render_template('admin/categories/index.html', categories=categories)

@bp.route('/categories/create', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        category = Category(
            name=request.form['name'],
            slug=request.form['slug'],
            description=request.form.get('description', '')
        )
        
        # 处理父级分类
        parent_id = request.form.get('parent_id')
        if parent_id:
            category.parent_id = parent_id
            
        db.session.add(category)
        db.session.commit()
        flash('分类创建成功', 'success')
        return redirect(url_for('admin.categories'))
    
    categories = Category.query.all()
    return render_template('admin/categories/create.html', categories=categories)

@bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    
    if request.method == 'POST':
        category.name = request.form['name']
        category.slug = request.form['slug']
        category.description = request.form.get('description', '')
        
        # 处理父级分类
        parent_id = request.form.get('parent_id')
        category.parent_id = parent_id if parent_id and parent_id != str(category.id) else None
            
        db.session.commit()
        flash('分类更新成功', 'success')
        return redirect(url_for('admin.categories'))
    
    categories = Category.query.filter(Category.id != category.id).all()
    return render_template('admin/categories/edit.html', category=category, categories=categories)

@bp.route('/categories/<int:id>/delete', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    # 检查是否有文章使用此分类
    post_count = Post.query.filter_by(category_id=id).count()
    if post_count > 0:
        flash('该分类下还有文章，不能删除', 'error')
        return redirect(url_for('admin.categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('分类删除成功', 'success')
    return redirect(url_for('admin.categories'))