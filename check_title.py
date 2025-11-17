import requests
import time

# 等待应用启动
print("等待应用启动...")
time.sleep(3)

try:
    response = requests.get('http://127.0.0.1:5000/', timeout=10)
    if response.status_code == 200:
        content = response.text
        
        # 提取标题
        import re
        title_match = re.search(r'<title>(.*?)</title>', content)
        if title_match:
            title = title_match.group(1)
            print(f"页面标题: {title}")
            
            # 检查是否包含站点标题
            if "超级个体试验场" in title:
                print("✓ 标题正确使用了站点SEO设置")
            elif "现代化博客系统" in title:
                print("✗ 标题仍在使用默认值")
            else:
                print("? 标题内容: " + title[:50] + "...")
        else:
            print("✗ 未找到标题标签")
    else:
        print(f"✗ 请求失败，状态码: {response.status_code}")
except Exception as e:
    print(f"✗ 发生错误: {e}")