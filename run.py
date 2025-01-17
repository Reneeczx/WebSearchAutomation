from flask import Flask
from app.config.config import Config

def create_app():
    app = Flask(__name__)
    
    # 加载配置
    config = Config()
    app.config['APP_CONFIG'] = config.config_data
    
    # 这里后续会注册其他模块的蓝图
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) 