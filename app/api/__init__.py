from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Post, Category, Tag
import os
import requests

bp = Blueprint('api', __name__)

@bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'content': post.content,
        'excerpt': post.excerpt,
        'featured_image': post.featured_image,
        'view_count': post.view_count,
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'first_name': post.author.first_name,
            'last_name': post.author.last_name
        },
        'category': {
            'id': post.category.id,
            'name': post.category.name,
            'slug': post.category.slug
        } if post.category else None,
        'tags': [{'id': tag.id, 'name': tag.name, 'slug': tag.slug} for tag in post.tags]
    } for post in posts])

@bp.route('/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    
    post = Post(
        title=data['title'],
        slug=data['slug'],
        content=data['content'],
        excerpt=data.get('excerpt', ''),
        status=data.get('status', 'draft'),
        user_id=current_user.id
    )
    
    if 'category_id' in data:
        post.category_id = data['category_id']
    
    db.session.add(post)
    db.session.commit()
    
    return jsonify({'message': 'Post created successfully', 'id': post.id}), 201

@bp.route('/ai/generate_post', methods=['POST'])
@login_required
def generate_post_with_ai():
    data = request.get_json()
    topic = data.get('topic')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # 使用DEEPSEEK API生成文章
    api_key = os.getenv('DEEPSEEK_APIKEY')
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
        # 定义优化后的提示词变量（使用三引号以支持多行文本）
    prompt_template = f"""
    你是一位在相关领域拥有多年经验的专家博主。
    请撰写一篇关于 "{topic}" 的深度博客文章。

    文章要求：
    1. 目标受众：想要入门的初学者及寻求进阶的专业人士。
    2. 语气风格：专业、客观，但通俗易懂，避免过于晦涩的术语。
    3. 结构安排：
    - 引人入胜的标题：包含关键词，具有点击欲望。
    - 引言：用一个痛点或故事作为钩子（Hook）吸引读者。
    - 正文：使用 H2 和 H3 标题分层级阐述，包含具体的案例分析或数据支持。
    - 结论：总结全文，并给出一个具体的行动建议。
    4. SEO优化：确保文章自然地包含与主题相关的关键词。

    请使用 Markdown 格式输出。
    """

    # 构建 payload
    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'user', 'content': prompt_template}
        ],
        'stream': False
    }
    
    try:
        response = requests.post(
            'https://api.deepseek.com/chat/completions',
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # 创建文章草稿
            post = Post(
                title=topic,
                slug=topic.replace(' ', '-').lower(),
                content=content,
                status='draft',
                user_id=current_user.id
            )
            
            db.session.add(post)
            db.session.commit()
            
            return jsonify({
                'message': 'Post generated successfully',
                'id': post.id,
                'title': post.title,
                'content': content
            }), 201
        else:
            return jsonify({'error': 'Failed to generate post with AI'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500