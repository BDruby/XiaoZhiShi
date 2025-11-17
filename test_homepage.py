import requests
import time

# 等待应用启动
print("等待应用启动...")
time.sleep(3)

try:
    # 测试首页
    response = requests.get('http://127.0.0.1:5000/', timeout=10)
    print(f"首页状态码: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ 首页访问正常")
        print(f"页面长度: {len(response.text)} 字符")
        
        # 检查是否包含SEO相关标签
        if '<title>' in response.text:
            print("✓ 页面包含标题标签")
        if 'meta name="description"' in response.text:
            print("✓ 页面包含描述标签")
        if 'property="og:' in response.text:
            print("✓ 页面包含Open Graph标签")
    else:
        print(f"✗ 首页访问失败，状态码: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("✗ 无法连接到应用，请确保应用正在运行")
except requests.exceptions.Timeout:
    print("✗ 请求超时，请检查应用是否正常启动")
except Exception as e:
    print(f"✗ 发生错误: {e}")

# 测试管理后台
try:
    response = requests.get('http://127.0.0.1:5000/admin/', timeout=10)
    print(f"管理后台状态码: {response.status_code}")
    if response.status_code == 200 or response.status_code == 302:
        print("✓ 管理后台访问正常")
    else:
        print(f"✗ 管理后台访问失败，状态码: {response.status_code}")
except:
    print("✗ 管理后台无法访问")

# 测试SEO设置页面
try:
    response = requests.get('http://127.0.0.1:5000/admin/seo/', timeout=10)
    print(f"SEO设置页面状态码: {response.status_code}")
    if response.status_code in [200, 302, 401, 403]:  # 401/403是正常的（需要登录）
        print("✓ SEO设置页面访问正常（可能需要登录）")
    else:
        print(f"✗ SEO设置页面访问失败，状态码: {response.status_code}")
except:
    print("✗ SEO设置页面无法访问")