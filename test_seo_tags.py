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
        
        # 检查标题标签
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            title = title_match.group(1)
            print(f"✓ 页面标题: {title}")
            
            # 检查是否包含站点标题
            if "超级个体试验场" in title or "小芝士" in title:
                print("✓ 标题包含站点设置")
            else:
                print("✗ 标题未包含站点设置")
        else:
            print("✗ 未找到标题标签")
        
        # 检查描述标签
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', content)
        if desc_match:
            description = desc_match.group(1)
            print(f"✓ 页面描述: {description[:100]}...")  # 只显示前100个字符
            
            # 检查是否包含站点描述
            if "AIGC" in description or "AI工具" in description:
                print("✓ 描述包含站点设置")
            else:
                print("✗ 描述未包含站点设置")
        else:
            print("✗ 未找到描述标签")
        
        # 检查关键词标签
        kw_match = re.search(r'<meta[^>]*name="keywords"[^>]*content="([^"]*)"', content)
        if kw_match:
            keywords = kw_match.group(1)
            print(f"✓ 页面关键词: {keywords}")
            
            # 检查是否包含站点关键词
            if "AI" in keywords and "AIGC" in keywords:
                print("✓ 关键词包含站点设置")
            else:
                print("✗ 关键词未包含站点设置")
        else:
            print("✓ 未找到关键词标签（可能没有设置站点关键词）")
            
        # 检查Open Graph标签
        og_title_match = re.search(r'<meta[^>]*property="og:title"[^>]*content="([^"]*)"', content)
        if og_title_match:
            og_title = og_title_match.group(1)
            print(f"✓ OG标题: {og_title}")
        
        og_desc_match = re.search(r'<meta[^>]*property="og:description"[^>]*content="([^"]*)"', content)
        if og_desc_match:
            og_description = og_desc_match.group(1)
            print(f"✓ OG描述: {og_description[:100]}...")
        
        # 检查Twitter Card标签
        tw_title_match = re.search(r'<meta[^>]*name="twitter:title"[^>]*content="([^"]*)"', content)
        if tw_title_match:
            tw_title = tw_title_match.group(1)
            print(f"✓ Twitter标题: {tw_title}")
        
        tw_desc_match = re.search(r'<meta[^>]*name="twitter:description"[^>]*content="([^"]*)"', content)
        if tw_desc_match:
            tw_description = tw_desc_match.group(1)
            print(f"✓ Twitter描述: {tw_description[:100]}...")
    
    else:
        print(f"✗ 首页访问失败，状态码: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("✗ 无法连接到应用，请确保应用正在运行")
except requests.exceptions.Timeout:
    print("✗ 请求超时，请检查应用是否正常启动")
except Exception as e:
    print(f"✗ 发生错误: {e}")