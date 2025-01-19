from flask import Blueprint, jsonify, request, render_template
from .search.search_manager import SearchManager

bp = Blueprint('main', __name__)
search_manager = SearchManager()

@bp.route('/', methods=['GET', 'POST'])
def index():
    """处理主页请求和搜索请求"""
    if request.method == 'GET':
        return render_template('index.html')
        
    # POST请求处理搜索
    try:
        keyword = request.form.get('keyword')
        selected_sites = request.form.getlist('sites[]')
        
        if not keyword:
            return jsonify({"error": "请输入搜索关键词"}), 400
            
        if not selected_sites:
            return jsonify({"error": "请选择至少一个搜索站点"}), 400
            
        results = search_manager.search(keyword, selected_sites)
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@bp.route('/api/sites', methods=['GET'])
def get_sites():
    """获取所有搜索站点配置"""
    return jsonify(search_manager.get_all_sites())

@bp.route('/api/sites', methods=['POST'])
def add_site():
    """添加新的搜索站点"""
    data = request.json
    search_manager.add_site(
        name=data['name'],
        url=data['url'],
        search_path=data['search_path']
    )
    return jsonify({"status": "success"})

@bp.route('/api/sites/<name>', methods=['PUT'])
def update_site(name):
    """更新搜索站点配置"""
    try:
        data = request.json
        search_manager.update_site(
            name=name,
            url=data.get('url'),
            search_path=data.get('search_path'),
            enabled=data.get('enabled')
        )
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@bp.route('/api/sites/<name>', methods=['DELETE'])
def delete_site(name):
    """删除搜索站点"""
    try:
        search_manager.remove_site(name)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400 