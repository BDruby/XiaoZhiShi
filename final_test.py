import time
import requests

print("等待应用启动...")
time.sleep(5)

try:
    response = requests.get('http://127.0.0.1:5000/', timeout=10)
    print(f"状态码: {response.status_code}")
    
    import re
    title_match = re.search(r'<title>(.*?)</title>', response.text)
    if title_match:
        title = title_match.group(1)
        print(f"标题: {title}")
        
        if "超级个体试验场" in title:
            print("✓ SEO设置已应用成功！")
        elif "现代化博客系统" in title:
            print("✗ 仍在使用默认标题")
        else:
            print("? 标题内容:", title[:100])
    else:
        print("未找到标题标签")
        
except Exception as e:
    print(f"连接失败: {e}")