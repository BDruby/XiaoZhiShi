from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from app.models import db, SeoSetting
from app.admin.utils import admin_required
import json
from datetime import datetime

bp = Blueprint('admin_seo', __name__, url_prefix='/admin/seo')

@bp.route('/')
@login_required
@admin_required
def index():
    """SEO设置管理页面"""
    seo_setting = SeoSetting.query.first()
    if not seo_setting:
        # 如果没有SEO设置，创建一个默认的
        seo_setting = SeoSetting()
        db.session.add(seo_setting)
        db.session.commit()
    
    return render_template('admin/seo/index.html', seo_setting=seo_setting)

@bp.route('/update', methods=['POST'])
@login_required
@admin_required
def update():
    """更新SEO设置"""
    seo_setting = SeoSetting.query.first()
    if not seo_setting:
        seo_setting = SeoSetting()
        db.session.add(seo_setting)
    
    # 更新基本设置
    seo_setting.site_title = request.form.get('site_title')
    seo_setting.site_description = request.form.get('site_description')
    seo_setting.site_keywords = request.form.get('site_keywords')
    seo_setting.site_author = request.form.get('site_author')
    seo_setting.site_logo = request.form.get('site_logo')
    seo_setting.favicon = request.form.get('favicon')
    seo_setting.google_analytics_id = request.form.get('google_analytics_id')
    seo_setting.baidu_analytics_id = request.form.get('baidu_analytics_id')
    seo_setting.social_media_links = request.form.get('social_media_links')
    seo_setting.custom_head_code = request.form.get('custom_head_code')
    seo_setting.robots_txt = request.form.get('robots_txt')
    seo_setting.sitemap_url = request.form.get('sitemap_url')
    seo_setting.twitter_handle = request.form.get('twitter_handle')
    seo_setting.og_image = request.form.get('og_image')
    seo_setting.default_canonical_url = request.form.get('default_canonical_url')
    
    try:
        db.session.commit()
        flash('SEO设置已更新', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'更新失败: {str(e)}', 'error')
    
    return redirect(url_for('admin_seo.index'))