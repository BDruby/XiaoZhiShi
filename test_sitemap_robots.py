import requests
import time
import xml.etree.ElementTree as ET

print("等待应用启动...")
time.sleep(5)

try:
    # 测试sitemap.xml
    print("测试sitemap.xml...")
    sitemap_response = requests.get('http://127.0.0.1:5000/sitemap.xml', timeout=10)
    print(f"sitemap.xml状态码: {sitemap_response.status_code}")
    
    if sitemap_response.status_code == 200:
        print("✓ sitemap.xml 访问正常")
        print(f"内容类型: {sitemap_response.headers.get('Content-Type')}")
        
        # 检查是否包含基本的sitemap元素
        content = sitemap_response.text
        if '<urlset' in content and 'http://www.sitemaps.org/schemas/sitemap/0.9' in content:
            print("✓ sitemap.xml 格式正确")
            
            # 尝试解析XML
            try:
                root = ET.fromstring(content)
                urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
                print(f"✓ sitemap.xml 包含 {len(urls)} 个URL")
                
                # 打印前几个URL
                for i, url in enumerate(urls[:3]):
                    loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                    if loc is not None:
                        print(f"  - {loc.text}")
            except ET.ParseError as e:
                print(f"✗ sitemap.xml XML解析错误: {e}")
        else:
            print("✗ sitemap.xml 格式不正确")
    else:
        print(f"✗ sitemap.xml 访问失败，状态码: {sitemap_response.status_code}")
    
    print()
    
    # 测试robots.txt
    print("测试robots.txt...")
    robots_response = requests.get('http://127.0.0.1:5000/robots.txt', timeout=10)
    print(f"robots.txt状态码: {robots_response.status_code}")
    
    if robots_response.status_code == 200:
        print("✓ robots.txt 访问正常")
        print(f"内容类型: {robots_response.headers.get('Content-Type')}")
        
        content = robots_response.text
        if 'User-agent:' in content and 'Sitemap:' in content:
            print("✓ robots.txt 格式正确")
            print("robots.txt内容:")
            print(content[:500] + ("..." if len(content) > 500 else ""))
        else:
            print("✗ robots.txt 格式不正确")
    else:
        print(f"✗ robots.txt 访问失败，状态码: {robots_response.status_code}")
        
except Exception as e:
    print(f"✗ 发生错误: {e}")