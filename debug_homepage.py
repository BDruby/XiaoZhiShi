import requests
import time
import re

# 等待应用启动
print("等待应用启动...")
time.sleep(3)

try:
    # 获取首页内容
    response = requests.get('http://127.0.0.1:5000/', timeout=10)
    
    if response.status_code == 200:
        print("✓ 首页访问正常")
        
        # 提取并检查SEO标签
        content = response.text
        
        # 保存首页内容到文件以便检查
        with open('homepage_debug.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ 首页内容已保存到 homepage_debug.html")
        
        # 检查标题标签
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            title = title_match.group(1)
            print(f"✓ 页面标题: {title}")
        else:
            print("✗ 未找到标题标签")
        
        # 检查描述标签
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', content)
        if desc_match:
            description = desc_match.group(1)
            print(f"✓ 页面描述: {description}")
        else:
            print("✗ 未找到描述标签")
        
        # 检查关键词标签
        kw_match = re.search(r'<meta[^>]*name="keywords"[^>]*content="([^"]*)"', content)
        if kw_match:
            keywords = kw_match.group(1)
            print(f"✓ 页面关键词: {keywords}")
        else:
            print("✓ 未找到关键词标签")
        
        # 检查是否包含站点特定的内容
        if "超级个体试验场" in content:
            print("✓ 页面包含站点标题内容")
        else:
            print("✗ 页面未包含站点标题内容")
            
        if "AIGC" in content:
            print("✓ 页面包含站点描述内容")
        else:
            print("✗ 页面未包含站点描述内容")
    
    else:
        print(f"✗ 首页访问失败，状态码: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("✗ 无法连接到应用，请确保应用正在运行")
except requests.exceptions.Timeout:
    print("✗ 请求超时，请检查应用是否正常启动")
except Exception as e:
    print(f"✗ 发生错误: {e}")