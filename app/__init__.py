import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from config.app_config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 确保logs目录存在
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # 配置日志格式    
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    
    # 配置文件处理器
    file_handler = RotatingFileHandler(
        'logs/search.log',
        maxBytes=10240000,
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # 设置为DEBUG级别以捕获所有日志
    
    # 配置控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)  # 控制台只显示INFO及以上级别
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # 设置为DEBUG级别以捕获所有日志
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 设置Flask应用日志
    app.logger.setLevel(logging.DEBUG)
    
    # 输出初始日志
    app.logger.info('='*50)
    app.logger.info('搜索应用启动')
    app.logger.info(f'日志文件: {os.path.abspath("logs/search.log")}')
    
    # 注册蓝图
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app 