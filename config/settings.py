"""
全局设置模块
"""
import os
from pathlib import Path


class Settings:
    """全局设置"""
    
    # 项目根目录
    BASE_DIR = Path(__file__).parent.parent
    
    # 测试环境
    ENV = os.getenv('TEST_ENV', 'dev')
    
    # 日志配置
    LOG_DIR = BASE_DIR / 'logs'
    LOG_LEVEL = 'DEBUG'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_FILE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 报告配置
    REPORT_DIR = BASE_DIR / 'reports' / 'html'
    REPORT_TITLE = '商城后台管理系统测试报告'
    
    # 测试数据目录
    DATA_DIR = BASE_DIR / 'test_data'
    
    # allure报告目录
    ALLURE_DIR = BASE_DIR / 'reports' / 'allure'
    
    # 截图目录
    SCREENSHOT_DIR = BASE_DIR / 'reports' / 'screenshots'
    
    @classmethod
    def ensure_dirs(cls):
        """确保必要目录存在"""
        dirs = [
            cls.LOG_DIR,
            cls.REPORT_DIR,
            cls.ALLURE_DIR,
            cls.SCREENSHOT_DIR,
            cls.DATA_DIR
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)


# 初始化时创建必要目录
Settings.ensure_dirs()
