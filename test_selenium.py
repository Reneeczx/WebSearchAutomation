from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os

def test_selenium():
    print("=== Selenium 环境检查 ===")
    print(f"Python 版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"Selenium 版本: {webdriver.__version__}")
    
    try:
        print("\n1. 配置 Chrome 选项...")
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # 设置Chrome的二进制文件路径
        chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        if os.path.exists(chrome_path):
            chrome_options.binary_location = chrome_path
            print(f"Chrome路径: {chrome_path}")
        else:
            print("未找到Chrome，将使用默认路径")
        
        print("\n2. 初始化 ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"ChromeDriver 路径: {driver_path}")
        
        # 修正ChromeDriver路径
        if os.name == 'nt' and 'chromedriver-win32' in driver_path:
            base_dir = os.path.dirname(driver_path)
            driver_path = os.path.join(base_dir, 'chromedriver.exe')
            print(f"修正后的ChromeDriver路径: {driver_path}")
        
        print("\n3. 创建WebDriver...")
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("\n4. 访问测试页面...")
        driver.get("https://www.google.com")
        
        print(f"页面标题: {driver.title}")
        print("\n测试成功完成!")
        
    except Exception as e:
        print(f"\n测试失败: {str(e)}")
        print(f"错误类型: {type(e).__name__}")
        import traceback
        print(f"错误详情:\n{traceback.format_exc()}")
        
    finally:
        if 'driver' in locals():
            driver.quit()
            print("\n浏览器已关闭")

if __name__ == "__main__":
    test_selenium()