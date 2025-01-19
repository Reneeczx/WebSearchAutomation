# 医学网站文章搜索与筛选应用

一个基于 Web 的应用程序，用于从多个医学网站搜索、提取和筛选文章。支持多站点配置和管理，提供统一的搜索界面。

## 功能特点

- 支持多个医学网站搜索（Cancer Research UK, NCI, ACS, Mayo Clinic等）
- 动态配置和管理搜索站点
- 支持选择性搜索（可选择特定站点进行搜索）
- 统一的搜索结果展示
- 详细的错误处理和日志记录

## 技术栈

### 后端
- Python 3.7+
- Flask (Web框架)
- Selenium (网页爬取)
- Chrome WebDriver
- logging (日志管理)

### 前端
- Bootstrap 5 (UI框架)
- JavaScript (异步请求和动态更新)
- HTML5/CSS3

## 项目结构

medical_search/              # 项目根目录
├── app/                    # Flask应用包
│   ├── __init__.py        # Flask应用工厂
│   ├── routes.py          # 路由处理
│   ├── templates/         # 前端模板
│   │   └── index.html     # 主页面
│   └── search/            # 搜索相关模块
│       ├── search_manager.py  # 搜索管理器
│       ├── webdriver_manager.py  # WebDriver管理
│       └── cancer_uk.py   # Cancer UK搜索实现
├── config/                 # 配置目录
│   ├── app_config.py      # 应用配置类
│   └── search_sites.json  # 搜索站点配置
├── logs/                  # 日志目录
│   └── search.log        # 应用日志文件
├── debug/                 # 调试目录
│   ├── raw_response.html # 原始响应
│   └── formatted_page.html # 格式化页面
├── tests/                 # 测试目录
│   ├── __init__.py
│   └── test_selenium.py  # Selenium环境测试
├── setup_chromedriver.py  # ChromeDriver安装脚本
└── run.py                # 应用入口

## 配置管理

### 配置文件
1. `config/app_config.py`: 应用级配置
   - Flask 应用配置
   - 路径配置
   - 环境变量

2. `config/search_sites.json`: 搜索站点配置
   - 站点 URL
   - 搜索路径
   - 启用状态

### 配置调用流程
mermaid
flowchart TD
A[search_sites.json] -->|1. 加载配置| B[SearchManager]
B -->|2. 初始化| C[run.py]
C -->|3. 创建应用| D[app/init.py]
D -->|4. 注册蓝图| E[routes.py]
E -->|5. 处理请求| F[search_manager.search]
F -->|6. 执行搜索| G[cancer_uk.py]
```

## 安装和配置

1. **安装 Python 依赖**:

2. **安装 Chrome WebDriver**:
   - 检查 Chrome 浏览器版本
   - 运行 `python setup_chromedriver.py`
   - 或手动下载对应版本的 ChromeDriver

3. **配置搜索站点**:
   - 编辑 `config/search_sites.json`
   - 或通过 Web 界面管理

4. **运行应用**:
```bash
python run.py
```

## 调试功能

### 日志系统
- 日志文件：`logs/search.log`
- 日志级别：
  - 文件：DEBUG 及以上
  - 控制台：INFO 及以上

### 调试文件
- 原始响应：`debug/raw_response.html`
- 格式化页面：`debug/formatted_page.html`

## 使用说明

### 站点管理
1. 在侧边栏点击"添加站点"按钮添加新的搜索站点
2. 填写站点信息：
   - 站点名称：唯一标识符
   - 站点URL：基础URL
   - 搜索路径：搜索页面的路径
3. 可以启用/禁用或删除已有站点

### 搜索功能
1. 在搜索框输入关键词
2. 选择要搜索的站点（可多选）
3. 点击搜索按钮开始搜索
4. 结果将分站点显示，包含：
   - 文章标题
   - 摘要
   - 原文链接

## 开发状态

### 已完成
- [x] 基础项目架构
- [x] Flask应用配置
- [x] 搜索管理器实现
- [x] Cancer Research UK 搜索实现
- [x] 前端界面实现
- [x] 站点配置管理
- [x] 错误处理和日志记录
- [x] 调试功能实现

### 进行中
- [ ] 添加更多搜索源
- [ ] 搜索结果缓存
- [ ] 用户认证功能
- [ ] 搜索历史记录

### 计划中
- [ ] 结果导出功能
- [ ] 高级搜索选项
- [ ] 搜索结果分析
- [ ] API 文档

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

[MIT License](LICENSE)

## 联系方式

[待补充]

## 致谢

- [Selenium](https://www.selenium.dev/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)