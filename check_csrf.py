from app import create_app

def check_csrf():
    app = create_app()
    with app.app_context():
        csrf_available = 'csrf_token' in app.jinja_env.globals
        print(f"CSRF Token available: {csrf_available}")
        
        if csrf_available:
            print("CSRF token function:", app.jinja_env.globals['csrf_token'])
        else:
            print("CSRF token not available in Jinja globals")
            
            # 检查Flask-WTF配置
            from flask_wtf.csrf import CSRFProtect
            print("Flask-WTF CSRFProtect available")

if __name__ == "__main__":
    check_csrf()