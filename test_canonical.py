import requests
import time
import re

print("等待应用启动...")
time.sleep(5)

try:
    # 测试首页的规范URL
    print("测试首页规范URL...")
    response = requests.get('http://127.0.0.1:5000/', timeout=10)
    print(f"首页状态码: {response.status_code}")
    
    if response.status_code == 200:
        content = response.text
        
        # 查找规范URL标签
        canonical_match = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', content)
        if canonical_match:
            canonical_url = canonical_match.group(1)
            print(f"✓ 首页规范URL: {canonical_url}")
            
            # 检查是否为当前URL
            if canonical_url == 'http://127.0.0.1:5000/':
                print("✓ 规范URL正确指向当前页面")
            else:
                print(f"? 规范URL指向: {canonical_url}")
        else:
            print("✗ 未找到规范URL标签")
    else:
        print(f"✗ 首页访问失败，状态码: {response.status_code}")
        
    print()
    
    # 测试文章详情页的规范URL
    print("测试文章详情页规范URL...")
    # 先获取一个文章slug
    index_response = requests.get('http://127.0.0.1:5000/', timeout=10)
    if index_response.status_code == 200:
        # 简单地从首页内容中提取一个文章链接
        post_match = re.search(r'href="/post/([^"]+)"', index_response.text)
        if post_match:
            post_slug = post_match.group(1)
            post_url = f'http://127.0.0.1:5000/post/{post_slug}'
            print(f"测试文章: {post_url}")
            
            post_response = requests.get(post_url, timeout=10)
            if post_response.status_code == 200:
                content = post_response.text
                canonical_match = re.search(r'<link[^>]*rel="canonical"[^>]*href="([^"]*)"', content)
                if canonical_match:
                    canonical_url = canonical_match.group(1)
                    print(f"✓ 文章页规范URL: {canonical_url}")
                    
                    if canonical_url == post_url:
                        print("✓ 规范URL正确指向当前文章页")
                    else:
                        print(f"? 规范URL指向: {canonical_url}")
                else:
                    print("✗ 未找到规范URL标签")
            else:
                print(f"✗ 文章页访问失败，状态码: {post_response.status_code}")
        else:
            print("✗ 首页未找到文章链接")
    else:
        print(f"✗ 首页访问失败，状态码: {index_response.status_code}")
        
except Exception as e:
    print(f"✗ 发生错误: {e}")