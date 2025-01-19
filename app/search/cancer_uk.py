import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException  # 导入 TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
from urllib.parse import urlencode, quote_plus
import time

logger = logging.getLogger(__name__)

def get_chrome_driver():
    """初始化Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    try:
        # 使用webdriver_manager获取正确的chromedriver路径
        driver_path = ChromeDriverManager().install()
        logger.info(f"ChromeDriver路径: {driver_path}")
        
        # 修正Windows路径问题
        if os.name == 'nt':  # Windows系统
            if 'chromedriver-win32' in driver_path:
                driver_path = os.path.join(os.path.dirname(driver_path), 'chromedriver.exe')
                logger.info(f"修正后的ChromeDriver路径: {driver_path}")
        
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        logger.error(f"初始化ChromeDriver失败: {str(e)}")
        raise

def search_articles(keyword, site_config):
    """
    在Cancer Research UK网站搜索文章
    Args:
        keyword: 搜索关键词
        site_config: 站点配置信息
    Returns:
        list: 搜索结果列表
    """
    logger.info(f"开始搜索 Cancer UK，关键词: {keyword}")
    logger.debug(f"站点配置: {site_config}")
    
    if not keyword.strip():
        logger.error("搜索关键词为空")
        return []
    
    driver = None
    try:
        # 初始化WebDriver
        driver = get_chrome_driver()
        base_url = site_config['url']
        
        # 构造完整的查询参数
        params = {
            'q': keyword,           # 搜索关键词参数
            'size': 'n_20_n'       # 每页显示结果数
        }
        
        # 使用 urlencode 构造查询字符串
        search_url = f"{base_url}/?{urlencode(params, quote_via=quote_plus)}"
        logger.info(f"访问页面: {search_url}")
        
        # 访问搜索页面
        driver.get(search_url)
        
        # 统一的WebDriverWait实例
        wait = WebDriverWait(driver, 10)

        # 等待页面加载,直到出现main标签
        logger.info("等待页面加载...")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))


        # 检查并处理 Cookie 确认对话框（如果存在）
        try:
            wait.until(
                EC.presence_of_element_located((By.ID, "onetrust-banner-sdk"))
            )
            logger.info("Cookie 对话框已出现")

            # 找到并点击"接受"按钮
            accept_button = wait.until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            accept_button.click()
            logger.info("已点击 '接受' 按钮")
            # 确认对话框消失
            wait.until(EC.invisibility_of_element_located((By.ID, 'onetrust-banner-sdk')))
        except TimeoutException:
            logger.debug("未发现 Cookie 确认对话框，继续处理")
        except Exception as e:
            logger.warning(f"处理 Cookie 确认对话框时出错: {str(e)}")

        # 等待动态内容加载
        time.sleep(2)

        # 等待页面加载
        logger.info("等待页面加载...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".main-search-app")))
        
        # 保存调试信息
        debug_dir = "debug"
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
            
        with open(os.path.join(debug_dir, "raw_response.html"), "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        logger.info(f"原始响应已保存到 {os.path.join(debug_dir, 'raw_response.html')}")
        
        
        # 解析结果
        results = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        with open(os.path.join(debug_dir, "formatted_page.html"), "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        logger.info(f"格式化的HTML已保存到 {os.path.join(debug_dir, 'formatted_page.html')}")
        
        # 查找搜索结果
        try:
            # 等待结果容器加载
            result_container = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul.sui-results-container"))
            )
            
            # 获取所有结果卡片
            result_cards = result_container.find_elements(By.CSS_SELECTOR, "li")
            
            for card in result_cards:
                try:
                    # 获取链接元素
                    link = card.find_element(By.CSS_SELECTOR, "a.chakra-card")
                    
                    # 获取标题
                    title = link.find_element(By.CSS_SELECTOR, "h2.chakra-heading").text.strip()
                    
                    # 获取URL
                    url = link.get_attribute("href")
                    
                    # 获取摘要和类型信息
                    summary_elems = link.find_elements(By.CSS_SELECTOR, "p.chakra-text")
                    # summary = summary_elems[0].text.strip() if summary_elems else ""
                    # type_info = summary_elems[-1].text.strip() if len(summary_elems) > 1 else ""
                    

                    # 调试日志，看看找到了哪些元素
                    logger.debug(f"找到 {len(summary_elems)} 个文本元素:")
                    for i, elem in enumerate(summary_elems):
                        logger.debug(f"  元素 {i}: {elem.text.strip()}")

                    # 根据内容特征判断
                    for elem in summary_elems:
                        text = elem.text.strip()
                        if text.startswith("Cancer type:"):
                            type_info = text
                        else:
                            summary = text

                    try:
                        category = link.find_element(By.CSS_SELECTOR, "p.chakra-text.label-text").text.strip()
                    except:
                        category = ""
                    
                    result = {
                        'title': title,
                        'url': url,
                        'summary': summary,
                        'type': type_info,
                        'category': category
                    }

                    logger.debug(f"找到结果: {result}")

                    results.append(result)
                   
                    
                except Exception as e:
                    logger.error(f"解析结果项时出错: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"等待结果容器时出错: {str(e)}")
        
        logger.info(f"搜索完成，找到 {len(results)} 个结果")
        return results
        
    except Exception as e:
        logger.error(f"搜索过程出错: {str(e)}")
        return []
        
    finally:
        if driver:
            driver.quit()