"""
日志处理模块
支持控制台和文件日志输出
"""
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from config.settings import Settings


class Logger:
    """日志处理类"""
    
    _instances = {}
    
    def __new__(cls, name: str = 'MallAutoTest'):
        """单例模式，按名称区分不同logger"""
        if name not in cls._instances:
            instance = super().__new__(cls)
            instance._init_logger(name)
            cls._instances[name] = instance
        return cls._instances[name]
    
    def _init_logger(self, name: str):
        """初始化logger"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加handler
        if self.logger.handlers:
            return
        
        # 日志格式
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器
        log_dir = Settings.LOG_DIR
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 按日期生成日志文件
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = log_dir / f'{name}_{today}.log'
        
        file_handler = logging.FileHandler(
            log_file,
            encoding='utf-8',
            mode='a'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, msg: str):
        """调试日志"""
        self.logger.debug(msg)
    
    def info(self, msg: str):
        """信息日志"""
        self.logger.info(msg)
    
    def warning(self, msg: str):
        """警告日志"""
        self.logger.warning(msg)
    
    def error(self, msg: str):
        """错误日志"""
        self.logger.error(msg)
    
    def critical(self, msg: str):
        """严重错误日志"""
        self.logger.critical(msg)
    
    def exception(self, msg: str):
        """异常日志（包含堆栈信息）"""
        self.logger.exception(msg)
    
    def log_test_start(self, test_name: str):
        """记录测试开始"""
        self.info(f"{'=' * 60}")
        self.info(f"测试开始: {test_name}")
        self.info(f"{'=' * 60}")
    
    def log_test_end(self, test_name: str, status: str = 'PASS'):
        """记录测试结束"""
        self.info(f"测试结束: {test_name} - {status}")
        self.info(f"{'=' * 60}\n")
    
    def log_api_request(self, method: str, url: str, 
                        params: dict = None, data: dict = None):
        """记录API请求"""
        self.debug(f"API请求: {method} {url}")
        if params:
            self.debug(f"请求参数: {params}")
        if data:
            self.debug(f"请求数据: {data}")
    
    def log_api_response(self, status_code: int, response: dict = None):
        """记录API响应"""
        self.debug(f"响应状态码: {status_code}")
        if response:
            self.debug(f"响应数据: {response}")


# 便捷访问
logger = Logger()


def get_logger(name: str = 'MallAutoTest') -> Logger:
    """获取Logger实例"""
    return Logger(name)
