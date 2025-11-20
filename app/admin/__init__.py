from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import login_required, current_user
from app.models import db, User, Post, Category, Tag
from app.auth.forms import RegisterForm
from app.admin.forms import AdminEditUserForm
from sqlalchemy import func

bp = Blueprint('admin', __name__, url_prefix='/admin')

# 导入SEO模块（这里导入是为了注册路由，即使没有直接使用变量）
from app.admin import seo, settings

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
    search = request.args.get('search', '', type=str)
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.username.contains(search)) | 
            (User.email.contains(search)) |
            (User.first_name.contains(search)) |
            (User.last_name.contains(search))
        )
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/users/index.html', users=users, search=search)

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
    form = AdminEditUserForm(original_username=user.username, original_email=user.email, obj=user)
    
    if form.validate_on_submit():
        # 更新用户信息
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.role = form.role.data
        user.is_active = form.is_active.data
        user.bio = form.bio.data
        
        # 如果提供了新密码，则更新密码
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
    
    # 检查用户是否有文章
    post_count = Post.query.filter_by(user_id=user.id).count()
    if post_count > 0:
        flash('该用户有文章，不能删除。请先转移或删除该用户的文章。', 'error')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('用户删除成功', 'success')
    return redirect(url_for('admin.users'))

# 文章管理
@bp.route('/posts')
def posts():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Post.query
    
    if search:
        query = query.filter(
            Post.title.contains(search) | Post.content.contains(search) | Post.excerpt.contains(search)
        )
    
    posts = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('admin/posts/index.html', posts=posts, search=search)

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
                all_tags = Tag.query.all()
                return render_template('admin/posts/create.html', categories=categories, all_tags=all_tags)
            
            post = Post(
                title=title,
                slug=slug,
                content=content,
                excerpt=request.form.get('excerpt', ''),
                status=request.form.get('status', 'draft'),
                featured_image=request.form.get('featured_image', ''),
                user_id=current_user.id,
                # SEO字段
                seo_title=request.form.get('seo_title', ''),
                seo_description=request.form.get('seo_description', ''),
                seo_keywords=request.form.get('seo_keywords', ''),
                seo_og_image=request.form.get('seo_og_image', '')
            )
            
            # 处理分类
            category_id = request.form.get('category_id')
            if category_id:
                post.category_id = category_id
                
            # 处理标签
            tag_ids = request.form.getlist('tag_ids')
            if tag_ids:
                tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
                post.tags = tags
                
            db.session.add(post)
            db.session.commit()
            flash('文章创建成功', 'success')
            return redirect(url_for('admin.posts'))
        except Exception as e:
            db.session.rollback()
            flash(f'创建文章时出错: {str(e)}', 'error')
            print(f"创建文章错误: {e}")  # 服务器端日志
            
    categories = Category.query.all()
    all_tags = Tag.query.all()
    return render_template('admin/posts/create.html', categories=categories, all_tags=all_tags)

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
            post.featured_image = request.form.get('featured_image', '')
            
            # SEO字段
            post.seo_title = request.form.get('seo_title', '')
            post.seo_description = request.form.get('seo_description', '')
            post.seo_keywords = request.form.get('seo_keywords', '')
            post.seo_og_image = request.form.get('seo_og_image', '')
            
            # 处理分类
            category_id = request.form.get('category_id')
            post.category_id = category_id if category_id else None
                
            # 处理标签
            tag_ids = request.form.getlist('tag_ids')
            if tag_ids:
                tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
                post.tags = tags
            else:
                post.tags = []  # 清空标签
                
            db.session.commit()
            flash('文章更新成功', 'success')
            return redirect(url_for('admin.posts'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新文章时出错: {str(e)}', 'error')
            print(f"更新文章错误: {e}")  # 服务器端日志
    
    categories = Category.query.all()
    all_tags = Tag.query.all()
    return render_template('admin/posts/edit.html', post=post, categories=categories, all_tags=all_tags)

@bp.route('/posts/<int:id>/delete', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('文章删除成功', 'success')
    return redirect(url_for('admin.posts'))

# 标签管理
@bp.route('/tags')
def tags():
    tags = Tag.query.order_by(Tag.created_at.desc()).all()
    return render_template('admin/tags/index.html', tags=tags)

@bp.route('/tags/create', methods=['GET', 'POST'])
def create_tag():
    if request.method == 'POST':
        name = request.form['name'].strip()
        slug = request.form['slug'].strip()
        if not name or not slug:
            flash('标签名称和URL别名不能为空', 'error')
            return render_template('admin/tags/create.html')
        
        # 检查标签是否已存在
        existing_tag = Tag.query.filter((Tag.name == name) | (Tag.slug == slug)).first()
        if existing_tag:
            flash('标签名称或URL别名已存在', 'error')
            return render_template('admin/tags/create.html')
        
        tag = Tag(name=name, slug=slug)
        db.session.add(tag)
        db.session.commit()
        flash('标签创建成功', 'success')
        return redirect(url_for('admin.tags'))
    
    return render_template('admin/tags/create.html')

@bp.route('/tags/<int:id>/edit', methods=['GET', 'POST'])
def edit_tag(id):
    tag = Tag.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name'].strip()
        slug = request.form['slug'].strip()
        if not name or not slug:
            flash('标签名称和URL别名不能为空', 'error')
            return render_template('admin/tags/edit.html', tag=tag)
        
        # 检查标签是否已存在（排除当前标签）
        existing_tag = Tag.query.filter(
            ((Tag.name == name) | (Tag.slug == slug)) & (Tag.id != id)
        ).first()
        if existing_tag:
            flash('标签名称或URL别名已存在', 'error')
            return render_template('admin/tags/edit.html', tag=tag)
        
        tag.name = name
        tag.slug = slug
        db.session.commit()
        flash('标签更新成功', 'success')
        return redirect(url_for('admin.tags'))
    
    return render_template('admin/tags/edit.html', tag=tag)

@bp.route('/tags/<int:id>/delete', methods=['POST'])
def delete_tag(id):
    tag = Tag.query.get_or_404(id)
    # 检查是否有文章使用此标签
    post_count = Post.query.filter(Post.tags.any(id=id)).count()
    if post_count > 0:
        flash('该标签下还有文章，不能删除', 'error')
        return redirect(url_for('admin.tags'))
    
    db.session.delete(tag)
    db.session.commit()
    flash('标签删除成功', 'success')
    return redirect(url_for('admin.tags'))

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
            description=request.form.get('description', ''),
            # SEO字段
            seo_title=request.form.get('seo_title', ''),
            seo_description=request.form.get('seo_description', ''),
            seo_keywords=request.form.get('seo_keywords', '')
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
        # SEO字段
        category.seo_title = request.form.get('seo_title', '')
        category.seo_description = request.form.get('seo_description', '')
        category.seo_keywords = request.form.get('seo_keywords', '')
        
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


# 密码修改表单
class ChangePasswordForm(FlaskForm):
    password = PasswordField('新密码', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('确认新密码', validators=[
        DataRequired(),
        EqualTo('password', message='密码不匹配')
    ])
    submit = SubmitField('更新密码')


@bp.route('/users/<int:id>/change-password', methods=['GET', 'POST'])
def change_user_password(id):
    user = User.query.get_or_404(id)
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('用户密码更新成功', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/users/change_password.html', form=form, user=user)