# 项目目录说明

这是一个基于pytest框架的商城后台管理系统自动化测试项目。

## 目录结构

```
MallAutoTest/
├── config/                     # 配置中心
│   ├── __init__.py
│   ├── config.py               # 配置读取模块
│   ├── settings.py             # 全局设置
│   └── env/                    # 环境配置文件
│       ├── dev.yaml            # 开发环境配置
│       ├── test.yaml           # 测试环境配置
│       └── prod.yaml           # 生产环境配置
│
├── mock/                       # Mock配置模块
│   ├── __init__.py
│   └── mock_server.py          # Mock服务
│
├── test_data/                  # 测试数据集
│   ├── __init__.py
│   ├── user_data.py            # 用户相关测试数据
│   ├── product_data.py         # 商品相关测试数据
│   └── category_data.py        # 类目相关测试数据
│
├── common/                     # 通用模块
│   ├── __init__.py
│   ├── db_handler.py           # 数据库连接
│   ├── file_handler.py         # 文件读取
│   ├── thread_handler.py       # 多线程处理
│   ├── request_handler.py      # HTTP请求封装
│   └── logger.py               # 日志模块
│
├── page_objects/               # UI自动化页面对象
│   ├── __init__.py
│   ├── base_page.py            # 基础页面类
│   ├── login_page.py           # 登录页面
│   ├── product_page.py         # 商品管理页面
│   └── user_page.py            # 用户管理页面
│
├── test_cases/                 # 测试用例集合
│   ├── __init__.py
│   ├── api/                    # 单接口测试
│   │   ├── __init__.py
│   │   ├── test_user_api.py
│   │   ├── test_product_api.py
│   │   ├── test_category_api.py
│   │   ├── test_permission_api.py
│   │   ├── test_sms_api.py
│   │   └── test_statistics_api.py
│   │
│   ├── scenario/               # 场景自动化测试
│   │   ├── __init__.py
│   │   ├── test_product_flow.py
│   │   └── test_user_flow.py
│   │
│   └── ui/                     # UI自动化测试
│       ├── __init__.py
│       ├── test_login_ui.py
│       └── test_product_ui.py
│
├── reports/                    # 测试报告输出
│   ├── html/                   # HTML报告
│   ├── allure/                 # Allure报告
│   └── screenshots/            # 截图
│
├── logs/                       # 日志目录
│
├── conftest.py                 # pytest配置和fixtures
├── pytest.ini                  # pytest配置文件
├── requirements.txt            # 依赖包
└── run.py                      # 执行入口
```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境
修改 `config/env/dev.yaml` 配置文件，设置正确的测试环境信息。

### 3. 执行测试

# 执行所有测试
python run.py --env dev

# 执行API测试
python run.py --env dev -m api

# 执行UI测试
python run.py --env dev -m ui --browser chrome

# 生成Allure报告
python run.py --env dev --allure
allure open reports/allure

# 并行执行
python run.py --env dev -n 4

## 测试分类

- **api**: 单接口测试，验证各API的正确性
- **scenario**: 场景测试，验证完整业务流程
- **ui**: UI自动化测试，验证页面功能
