import os
import openai
from dotenv import load_dotenv
from flask import current_app

# 加载环境变量
load_dotenv()

def get_deepseek_completion(prompt, model="deepseek-chat"):
    """
    调用DEEPSEEK API生成内容
    """
    # 从环境变量获取API密钥
    api_key = os.getenv('DEEPSEEK_APIKEY')
    if not api_key:
        raise ValueError("DEEPSEEK_APIKEY未在环境变量中设置")
    
    # 配置OpenAI客户端，使用DEEPSEEK的API端点
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        current_app.logger.error(f"调用DEEPSEEK API时出错: {str(e)}")
        raise e


def generate_blog_content(topic):
    """
    根据主题生成完整的博客内容
    """
    import os
import json
import requests
from dotenv import load_dotenv
from flask import current_app

# 加载环境变量
load_dotenv()

def get_deepseek_completion(prompt, model="deepseek-chat"):
    """
    通过HTTP请求调用DEEPSEEK API生成内容
    """
    # 从环境变量获取API密钥
    api_key = os.getenv('DEEPSEEK_APIKEY')
    if not api_key:
        raise ValueError("DEEPSEEK_APIKEY未在环境变量中设置")
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
        "stream": False  # 非流式响应
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=data,
            timeout=60  # 60秒超时
        )
        response.raise_for_status()  # 检查HTTP错误
        
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"调用DEEPSEEK API时出错: {str(e)}")
        raise e
    except KeyError as e:
        current_app.logger.error(f"解析DEEPSEEK API响应时出错: {str(e)}, 响应: {response.text}")
        raise ValueError(f"解析API响应失败: {str(e)}")


def generate_blog_content(topic):
    """
    根据主题生成完整的博客内容
    """
    prompt = f"""
    请根据主题 "{topic}" 生成一篇完整的博客文章。请严格按照以下JSON格式返回内容，不要添加其他文字：

    {{
        "title": "博客标题",
        "slug": "url-别名",
        "category": "分类名称",
        "excerpt": "文章摘要，不超过200字",
        "content": "完整的文章内容，使用HTML格式",
        "seo_title": "SEO标题",
        "seo_description": "SEO描述，不超过160个字符",
        "seo_keywords": "关键词1,关键词2,关键词3",
        "status": "draft"
    }}

    请确保slug使用英文和连字符，SEO关键词使用中文，内容结构清晰，包含适当的HTML标签。
    """
    
    try:
        result = get_deepseek_completion(prompt)
        
        # 解析返回的JSON
        import json
        import re
        
        # 从返回结果中提取JSON部分
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            try:
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError:
                current_app.logger.error(f"JSON解析失败: {json_str}")
                raise ValueError("AI返回的JSON格式不正确")
        else:
            raise ValueError("AI未返回有效的JSON格式")
            
    except Exception as e:
        current_app.logger.error(f"生成博客内容时出错: {str(e)}")
        raise e
    
    try:
        result = get_deepseek_completion(prompt)
        
        # 解析返回的JSON
        import json
        import re
        
        # 从返回结果中提取JSON部分
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            # 修复可能的JSON格式问题
            # 首先尝试直接解析
            try:
                data = json.loads(json_str)
                return data
            except json.JSONDecodeError:
                # 如果直接解析失败，尝试一些常见的修复
                # 移除可能的问题字符
                json_str = json_str.replace('\n', '\n').replace('\t', '\t')
                json_str = json_str.replace('\n', '\n').replace('\t', '\t')
                try:
                    data = json.loads(json_str)
                    return data
                except json.JSONDecodeError:
                    current_app.logger.error(f"JSON解析失败: {json_str}")
                    raise ValueError("AI返回的JSON格式不正确")
        else:
            raise ValueError("AI未返回有效的JSON格式")
            
    except Exception as e:
        current_app.logger.error(f"生成博客内容时出错: {str(e)}")
        raise e
