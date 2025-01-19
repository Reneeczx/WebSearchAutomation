import json
from pathlib import Path
import importlib
import logging

logger = logging.getLogger(__name__)

class SearchManager:
    """搜索管理器"""
    
    def __init__(self, config_path="config/search_sites.json"):
        self.config_path = Path(config_path)
        self.sites = self._load_config()
    
    def _load_config(self):
        """加载搜索站点配置"""
        if not self.config_path.exists():
            return {}
            
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            return {}
    
    def _save_config(self):
        """保存配置到文件"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.sites, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存配置文件失败: {str(e)}")
    
    def get_all_sites(self):
        """获取所有站点配置"""
        return self.sites
    
    def add_site(self, name, url, search_path, module_name=None):
        """
        添加搜索站点
        Args:
            name: 站点名称
            url: 站点URL
            search_path: 搜索路径
            module_name: 搜索模块名称，默认与name相同
        """
        if module_name is None:
            module_name = name
            
        self.sites[name] = {
            "url": url,
            "search_path": search_path,
            "enabled": True,
            "module": module_name
        }
        self._save_config()
    
    def remove_site(self, name):
        """删除搜索站点"""
        if name in self.sites:
            del self.sites[name]
            self._save_config()
    
    def update_site(self, name, url=None, search_path=None, enabled=None):
        """更新搜索站点配置"""
        if name not in self.sites:
            return
            
        if url is not None:
            self.sites[name]["url"] = url
        if search_path is not None:
            self.sites[name]["search_path"] = search_path
        if enabled is not None:
            self.sites[name]["enabled"] = enabled
            
        self._save_config()
    
    def search(self, keyword, selected_sites=None):
        """
        在指定站点中搜索
        Args:
            keyword: 搜索关键词
            selected_sites: 指定搜索的站点列表，为None时搜索所有启用的站点
        Returns:
            dict: 各站点的搜索结果
        """
        results = {}
        
        # 确定要搜索的站点
        sites_to_search = self.sites.items()
        if selected_sites is not None:
            sites_to_search = [(name, self.sites[name]) 
                             for name in selected_sites 
                             if name in self.sites]
        
        for name, site in sites_to_search:
            if not site.get("enabled", True):
                continue
                
            try:
                # 使用配置中指定的模块名
                module_name = site.get("module", name)
                module = importlib.import_module(f"app.search.{module_name}")
                search_func = getattr(module, "search_articles")
                
                # 传递站点配置到搜索函数
                results[name] = search_func(keyword, site)
            except Exception as e:
                logger.error(f"搜索站点 {name} 时出错: {str(e)}")
                results[name] = []
        
        return results 