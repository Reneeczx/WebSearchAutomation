from flask import Flask, render_template, request
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# 设置模板文件夹的路径
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')
app = Flask(__name__, template_folder=template_dir)

def search_cancer_research_uk(keyword):
    # 使用正确的搜索 URL
    base_url = "https://find.cancerresearchuk.org/"
    params = {
        "q": keyword,
        "size": "n_20_n"
    }
    
    try:
        # 发送搜索请求
        print(f"正在搜索关键词: {keyword}")  # 调试信息
        response = requests.get(base_url, params=params)
        print(f"搜索 URL: {response.url}")  # 调试信息
        print(f"状态码: {response.status_code}")  # 调试信息
        response.raise_for_status()
        
        # 打印响应内容的一部分
        print(f"响应内容前500字符: {response.text[:500]}")  # 调试信息
        
        # 解析搜索结果
        soup = BeautifulSoup(response.text, 'html.parser')
        print(f"搜索 URL: {response.url}")  # 打印实际的 URL，用于调试
        
        # 返回一个测试结果，确保模板能正确显示
        return [
            {
                "title": f"测试结果: {keyword}",
                "url": response.url,
                "summary": f"这是搜索 {keyword} 的测试结果"
            }
        ]
    except Exception as e:
        print(f"搜索出错: {str(e)}")  # 调试信息
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    keyword = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        print(f"收到搜索请求，关键词: {keyword}")  # 调试信息
        results = search_cancer_research_uk(keyword)
        print(f"搜索结果: {results}")  # 调试信息
    return render_template('index.html', keyword=keyword, results=results)

if __name__ == '__main__':
    app.run(debug=True) 
    