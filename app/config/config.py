import json
from typing import Dict, Any
import os

class Config:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {self.config_path} 未找到")
        except json.JSONDecodeError:
            raise ValueError(f"配置文件 {self.config_path} 格式错误")

    def save_config(self, config_data: Dict[str, Any]) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            self.config_data = config_data
        except Exception as e:
            raise Exception(f"保存配置文件失败: {str(e)}")

    def get_website_config(self, website_name: str) -> Dict[str, Any]:
        """获取指定网站的配置信息"""
        for website in self.config_data.get("websites", []):
            if website["name"] == website_name:
                return website
        raise ValueError(f"未找到网站 {website_name} 的配置信息") 