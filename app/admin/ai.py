from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models import db, Post, Category
from app.utils.ai_generator import generate_blog_content
from flask_wtf.csrf import validate_csrf

bp = Blueprint('admin_ai', __name__, url_prefix='/admin/ai')

@bp.route('/generate-content', methods=['POST'])
def generate_content():
    """通过AI生成文章内容"""
    try:
        data = request.get_json()
        topic = data.get('topic', '').strip()
        
        if not topic:
            return jsonify({'success': False, 'message': '主题不能为空'}), 400
        
        # 调用AI生成内容
        ai_content = generate_blog_content(topic)
        
        # 如果AI生成的分类不存在，尝试匹配现有分类
        category_name = ai_content.get('category', '')
        if category_name:
            # 尝试在现有分类中找到匹配项
            category = Category.query.filter(Category.name.ilike(f'%{category_name}%')).first()
            if category:
                ai_content['category_id'] = category.id
            else:
                # 如果没有找到匹配的分类，使用第一个分类或留空
                existing_categories = Category.query.all()
                if existing_categories:
                    ai_content['category_id'] = existing_categories[0].id
                else:
                    ai_content['category_id'] = None
        else:
            ai_content['category_id'] = None
        
        return jsonify({
            'success': True,
            'content': ai_content
        })
    except Exception as e:
        print(f"AI生成文章错误: {e}")  # 服务器端日志
        return jsonify({
            'success': False, 
            'message': f'AI生成失败: {str(e)}'
        }), 500