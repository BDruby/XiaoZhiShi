import psycopg2
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量获取数据库配置
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

# 对用户名和密码进行URL编码以处理特殊字符
import urllib.parse
encoded_username = urllib.parse.quote_plus(db_username)
encoded_password = urllib.parse.quote_plus(db_password)

try:
    # 尝试连接到数据库
    conn = psycopg2.connect(
        host=db_host.split(':')[0],  # 取主机地址
        port=db_host.split(':')[1],  # 取端口
        database=db_name,
        user=db_username,  # 使用原始用户名，不进行编码
        password=db_password   # 使用原始密码，不进行编码
    )
    
    print("数据库连接成功！")
    
    # 测试查询
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"数据库版本: {db_version[0]}")
    
    # 检查表是否存在
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    tables = cur.fetchall()
    print(f"现有表: {[table[0] for table in tables]}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"数据库连接失败: {e}")