import os

class Config:
    # Flask应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    
    # 路径配置
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SEARCH_CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'search_sites.json') 