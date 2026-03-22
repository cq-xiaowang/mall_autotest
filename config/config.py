"""
配置读取模块
支持多环境配置切换
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict


class Config:
    """配置管理类"""
    
    _instance = None
    _config: Dict[str, Any] = {}
    
    # 默认环境
    ENV = os.getenv('TEST_ENV', 'dev')
    
    # 配置文件路径
    CONFIG_DIR = Path(__file__).parent / 'env'
    
    def __new__(cls):
        """单例模式"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """加载配置文件"""
        config_file = self.CONFIG_DIR / f'{self.ENV}.yaml'
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f) or {}
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """获取配置项，支持点分隔的嵌套key"""
        instance = cls()
        keys = key.split('.')
        value = instance._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    @classmethod
    def get_base_url(cls) -> str:
        """获取基础URL"""
        return cls.get('base_url', '')
    
    @classmethod
    def get_api_prefix(cls) -> str:
        """获取API前缀"""
        return cls.get('api_prefix', '/api/v1')
    
    @classmethod
    def get_full_url(cls, endpoint: str) -> str:
        """获取完整URL"""
        base_url = cls.get_base_url()
        api_prefix = cls.get_api_prefix()
        return f"{base_url}{api_prefix}{endpoint}"
    
    @classmethod
    def get_database_config(cls) -> Dict[str, Any]:
        """获取数据库配置"""
        return cls.get('database', {})
    
    @classmethod
    def get_redis_config(cls) -> Dict[str, Any]:
        """获取Redis配置"""
        return cls.get('redis', {})
    
    @classmethod
    def get_test_account(cls, account_type: str = 'admin') -> Dict[str, str]:
        """获取测试账号"""
        return cls.get(f'test_account.{account_type}', {})
    
    @classmethod
    def get_timeout(cls, timeout_type: str = 'request') -> int:
        """获取超时配置"""
        return cls.get(f'timeout.{timeout_type}', 10)
    
    @classmethod
    def reload_config(cls, env: str = None):
        """重新加载配置"""
        if env:
            cls.ENV = env
        cls._instance = None
        return cls()


# 便捷访问实例
config = Config()
