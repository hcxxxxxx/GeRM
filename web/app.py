import os
import sys
from flask import Flask

# 确保可以导入src包
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from web.routes import register_routes

def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)
    
    # 配置应用
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 限制上传大小为50MB
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
    app.config["GENERATE_FOLDER"] = os.path.join(app.config["UPLOAD_FOLDER"], "generated")
    
    # 确保上传和生成目录存在
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["GENERATE_FOLDER"], exist_ok=True)
    
    # 注册路由
    register_routes(app)
    
    return app

if __name__ == "__main__":
    # 创建应用
    app = create_app()
    
    # 运行开发服务器
    app.run(debug=True, host="0.0.0.0", port=8000)