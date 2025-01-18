from flask import Flask, render_template, request
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# 设置模板文件夹的路径
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
app = Flask(__name__, template_folder=template_dir)

def search_cancer_research_uk(keyword):
    # 验证关键词
    if not keyword.strip() or keyword.startswith('http'):
        print("无效的搜索关键词")
        return []
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        print(f"正在搜索关键词: {keyword}")
        driver = webdriver.Chrome(options=chrome_options)
        
        # 访问搜索页面
        url = f"https://find.cancerresearchuk.org/?q={keyword}"
        driver.get(url)
        print(f"搜索 URL: {url}")
        
        # 添加调试信息
        print("页面标题:", driver.title)
        
        # 等待页面加载
        wait = WebDriverWait(driver, 10)
        try:
            # 等待任意一个结果卡片加载完成
            results_container = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "chakra-card"))
            )
            print("找到结果容器")
            
            # 获取所有搜索结果
            results = []
            search_results = driver.find_elements(By.CLASS_NAME, "chakra-card")
            print(f"找到 {len(search_results)} 个结果卡片")
            
            for result in search_results:
                try:
                    # 获取标题
                    title_elem = result.find_element(By.CLASS_NAME, "chakra-heading")
                    # 获取URL（从卡片的href属性）
                    url = result.get_attribute("href")
                    # 获取摘要
                    summary_elems = result.find_elements(By.CLASS_NAME, "chakra-text")
                    # 第一个非label-text的chakra-text元素是摘要
                    summary = ""
                    for elem in summary_elems:
                        if 'label-text' not in elem.get_attribute("class"):
                            summary = elem.text.strip()
                            break
                    
                    if title_elem and url:
                        results.append({
                            "title": title_elem.text.strip(),
                            "url": url,
                            "summary": summary
                        })
                except Exception as e:
                    print(f"解析结果时出错: {str(e)}")
                    continue
            
            print(f"成功解析 {len(results)} 个结果")
            return results
            
        except Exception as e:
            print(f"等待页面加载时出错: {str(e)}")
            return []
            
    except Exception as e:
        print(f"搜索出错: {str(e)}")
        return []
    finally:
        try:
            driver.quit()
        except:
            pass

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    keyword = ''
    if request.method == 'POST':
        # 获取并清理关键词
        keyword = request.form.get('keyword', '').strip()
        # 确保不是URL
        if keyword and not keyword.startswith('http'):
            print(f"收到搜索请求，关键词: {keyword}")
            results = search_cancer_research_uk(keyword)
            print(f"搜索结果: {results}")
        else:
            print("无效的搜索关键词")
    return render_template('index.html', keyword=keyword, results=results)

if __name__ == '__main__':
    app.run(debug=True) 
    