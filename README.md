# 医学网站文章搜索与筛选应用

一个基于 Web 的应用程序，用于从多个医学网站搜索、提取和筛选文章。

## 功能特点

- 支持多个医学网站搜索（NCI, ACS, Mayo Clinic等）
- 关键词搜索和内容提取
- 自动翻译功能
- 结果筛选和保存

## 技术栈

- Python 3.x
- Flask (Web框架)
- BeautifulSoup4 (网页解析)
- Requests (HTTP请求)
- Google Translate API (翻译功能)

## 安装说明

1. 克隆项目
2. 安装依赖：

bash
py -m pip install -r requirements.txt


## 项目结构
project/
├── app/
│ ├── config/ # 配置模块
│ ├── search/ # 搜索模块
│ ├── extract/ # 内容提取模块
│ ├── filter/ # 结果筛选模块
│ ├── translate/ # 翻译模块
│ └── output/ # 输出模块
├── config.json # 配置文件
└── run.py # 应用入口


## 使用说明

[待补充]

## 开发计划

- [x] 项目基础架构搭建
- [ ] 实现基本搜索功能
- [ ] 添加翻译功能
- [ ] 实现内容提取
- [ ] 添加结果筛选
- [ ] 完善输出功能