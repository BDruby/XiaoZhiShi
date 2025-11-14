from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.models import db, Media, Post
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
from PIL import Image

bp = Blueprint('media', __name__, url_prefix='/media')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_thumbnail(image_path, thumbnail_path, size=(200, 200)):
    """创建缩略图"""
    try:
        with Image.open(image_path) as img:
            # 保持宽高比
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, optimize=True, quality=85)
        return True
    except Exception as e:
        print(f"创建缩略图失败: {e}")
        return False

@bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    media_files = Media.query.filter_by(user_id=current_user.id).order_by(Media.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    return render_template('media/index.html', media_files=media_files)

@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件被选择'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '没有文件被选择'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        
        # 确保上传目录存在
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)
        
        # 如果是图片，创建缩略图
        thumbnail_filename = None
        if file.content_type.startswith('image/'):
            try:
                # 创建缩略图
                thumbnail_filename = f"thumb_{unique_filename}"
                thumbnail_path = os.path.join(upload_folder, thumbnail_filename)
                create_thumbnail(file_path, thumbnail_path)
            except Exception as e:
                print(f"创建缩略图失败: {e}")
        
        # 保存到数据库
        media = Media(
            filename=unique_filename,
            original_filename=filename,
            file_path=f'/static/uploads/{unique_filename}',
            file_size=os.path.getsize(file_path),
            mime_type=file.content_type,
            user_id=current_user.id
        )
        db.session.add(media)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'original_filename': filename,
            'file_path': f'/static/uploads/{unique_filename}',
            'id': media.id
        })
    else:
        return jsonify({'error': '不支持的文件格式'}), 400

@bp.route('/insert_to_post', methods=['POST'])
@login_required
def insert_to_post():
    data = request.get_json()
    media_id = data.get('media_id')
    post_id = data.get('post_id')
    
    media = Media.query.get_or_404(media_id)
    
    if media.user_id != current_user.id:
        return jsonify({'error': '无权限访问此文件'}), 403
    
    # 返回图片URL用于插入到文章中
    return jsonify({
        'url': media.file_path,
        'alt': media.alt_text or media.original_filename
    })


@bp.route('/get_image_info/<int:media_id>', methods=['GET'])
@login_required
def get_image_info(media_id):
    """获取图片信息用于插入到编辑器中"""
    try:
        media = Media.query.get_or_404(media_id)
        
        if media.user_id != current_user.id:
            return jsonify({'error': '无权限访问此文件'}), 403
        
        # 验证文件是否存在
        file_path = os.path.join(current_app.root_path, media.file_path[1:])  # 移除开头的/
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
        
        return jsonify({
            'url': media.file_path,
            'alt': media.alt_text or media.original_filename,
            'filename': media.original_filename,
            'size': media.file_size
        })
    except Exception as e:
        print(f"获取图片信息错误: {e}")
        return jsonify({'error': '获取图片信息时发生错误'}), 500

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    media = Media.query.get_or_404(id)
    
    if media.user_id != current_user.id:
        flash('无权限删除此文件', 'error')
        return redirect(url_for('media.index'))
    
    # 删除文件
    file_path = os.path.join(current_app.root_path, media.file_path[1:])  # 移除开头的/
    if os.path.exists(file_path):
        os.remove(file_path)
    
    # 从数据库删除记录
    db.session.delete(media)
    db.session.commit()
    
    flash('文件删除成功', 'success')
    return redirect(url_for('media.index'))