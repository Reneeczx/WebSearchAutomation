from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os

logger = logging.getLogger(__name__)

def get_chrome_driver():
    """
    获取配置好的Chrome WebDriver
    Returns:
        webdriver.Chrome: 配置好的Chrome WebDriver实例
    """
    try:
        # 配置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无界面模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # 设置下载路径和缓存目录
        driver_cache_path = os.path.join(os.getcwd(), "drivers")
        os.makedirs(driver_cache_path, exist_ok=True)
        
        logger.info(f"正在安装/更新 ChromeDriver...")
        driver_path = ChromeDriverManager(path=driver_cache_path).install()
        logger.info(f"ChromeDriver 路径: {driver_path}")
        
        # 创建服务
        service = Service(driver_path)
        
        # 创建 WebDriver 实例
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Chrome WebDriver 初始化成功")
        return driver
        
    except Exception as e:
        logger.error(f"Chrome WebDriver 初始化失败: {str(e)}")
        logger.error(f"当前工作目录: {os.getcwd()}")
        logger.error(f"Python路径: {os.sys.executable}")
        raise 