"""
Mock服务模块
用于模拟第三方接口或外部依赖服务
"""
import json
from typing import Any, Dict, Optional, Callable
from functools import wraps
from unittest.mock import Mock, patch


class MockServer:
    """Mock服务管理类"""
    
    def __init__(self):
        self._mock_data: Dict[str, Any] = {}
        self._mock_handlers: Dict[str, Callable] = {}
    
    def register_mock(self, name: str, response_data: Any):
        """注册mock数据"""
        self._mock_data[name] = response_data
    
    def get_mock_data(self, name: str, default: Any = None) -> Any:
        """获取mock数据"""
        return self._mock_data.get(name, default)
    
    def register_handler(self, name: str, handler: Callable):
        """注册mock处理器"""
        self._mock_handlers[name] = handler
    
    def get_handler(self, name: str) -> Optional[Callable]:
        """获取mock处理器"""
        return self._mock_handlers.get(name)


# ===================== 短信服务Mock =====================
class SMSMock:
    """短信服务Mock"""
    
    @staticmethod
    def send_sms_success():
        """短信发送成功响应"""
        return {
            "code": 200,
            "message": "success",
            "data": {
                "msg_id": "mock_msg_id_12345",
                "status": "sent"
            }
        }
    
    @staticmethod
    def send_sms_fail():
        """短信发送失败响应"""
        return {
            "code": 500,
            "message": "短信发送失败",
            "data": None
        }
    
    @staticmethod
    def verify_code_mock(code: str = "123456"):
        """验证码Mock"""
        return {
            "code": 200,
            "message": "success",
            "data": {
                "verify_code": code,
                "expire_time": 300
            }
        }


# ===================== 支付服务Mock =====================
class PaymentMock:
    """支付服务Mock"""
    
    @staticmethod
    def create_payment_success():
        """创建支付成功"""
        return {
            "code": 200,
            "message": "success",
            "data": {
                "payment_id": "mock_payment_12345",
                "pay_url": "https://mock-pay.example.com/pay/12345",
                "expire_time": 1800
            }
        }
    
    @staticmethod
    def payment_callback_success():
        """支付回调成功"""
        return {
            "code": 200,
            "message": "success",
            "data": {
                "status": "paid",
                "transaction_id": "mock_trans_12345"
            }
        }


# ===================== OSS服务Mock =====================
class OSSMock:
    """对象存储服务Mock"""
    
    @staticmethod
    def upload_success():
        """上传成功"""
        return {
            "code": 200,
            "message": "success",
            "data": {
                "url": "https://mock-oss.example.com/images/mock_file.jpg",
                "file_id": "mock_file_12345"
            }
        }
    
    @staticmethod
    def get_upload_token():
        """获取上传凭证"""
        return {
            "code": 200,
            "message": "success",
            "data": {
                "upload_token": "mock_token_xxxxxxxxxxxx",
                "expire_time": 3600
            }
        }


# ===================== Mock装饰器 =====================
def mock_response(mock_data: Dict[str, Any]):
    """
    Mock响应装饰器
    
    Usage:
        @mock_response({"code": 200, "message": "success"})
        def test_something():
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 可以在这里实现mock逻辑
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 全局Mock服务实例
mock_server = MockServer()

# 注册默认Mock数据
mock_server.register_mock('sms_send_success', SMSMock.send_sms_success())
mock_server.register_mock('sms_send_fail', SMSMock.send_sms_fail())
mock_server.register_mock('payment_success', PaymentMock.create_payment_success())
mock_server.register_mock('oss_upload_success', OSSMock.upload_success())
