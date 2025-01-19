from flask import Flask, render_template, request, jsonify
import os
from app import create_app
from app.search.search_manager import SearchManager

app = create_app()
search_manager = SearchManager()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        selected_sites = request.form.getlist('sites[]')  # 获取选中的站点
        print(f"收到搜索请求：{keyword}")
        print(f"选中的站点：{selected_sites}")
        
        if not selected_sites:
            return jsonify({
                "error": "请至少选择一个搜索站点"
            })
            
        # 执行搜索
        results = search_manager.search(keyword, selected_sites)
        return jsonify(results)
        
    # GET请求返回页面
    return render_template('index.html')

@app.route('/api/sites', methods=['GET'])
def get_sites():
    sites = search_manager.get_all_sites()
    return jsonify(sites)

if __name__ == '__main__':
    print("启动 Flask 服务器...")
    app.run(debug=True, host='127.0.0.1', port=5000) 
    