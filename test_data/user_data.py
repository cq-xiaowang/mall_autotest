"""
用户相关测试数据
"""
from typing import Dict, List, Any
import time


class UserData:
    """用户测试数据类"""
    
    # ===================== 用户登录数据 =====================
    @staticmethod
    def get_login_success_data() -> Dict[str, Any]:
        """登录成功数据"""
        return {
            "username": "admin",
            "password": "admin123"
        }
    
    @staticmethod
    def get_login_fail_data() -> List[Dict[str, Any]]:
        """登录失败数据集合"""
        return [
            {"username": "", "password": "admin123", "expected_msg": "用户名不能为空"},
            {"username": "admin", "password": "", "expected_msg": "密码不能为空"},
            {"username": "admin", "password": "wrong", "expected_msg": "用户名或密码错误"},
            {"username": "notexist", "password": "admin123", "expected_msg": "用户不存在"},
        ]
    
    # ===================== 用户创建数据 =====================
    @staticmethod
    def get_create_user_success_data() -> Dict[str, Any]:
        """创建用户成功数据"""
        timestamp = int(time.time() * 1000)
        return {
            "username": f"test_user_{timestamp}",
            "password": "Test123456",
            "real_name": "测试用户",
            "phone": "13800138000",
            "email": f"test_{timestamp}@example.com",
            "status": 1,
            "role_ids": [2]  # 普通用户角色
        }
    
    @staticmethod
    def get_create_user_fail_data() -> List[Dict[str, Any]]:
        """创建用户失败数据集合"""
        return [
            {"username": "", "password": "Test123456", "expected_msg": "用户名不能为空"},
            {"username": "ab", "password": "Test123456", "expected_msg": "用户名长度不能少于3位"},
            {"username": "a" * 51, "password": "Test123456", "expected_msg": "用户名长度不能超过50位"},
            {"username": "test_user", "password": "", "expected_msg": "密码不能为空"},
            {"username": "test_user", "password": "123", "expected_msg": "密码长度不能少于6位"},
            {"username": "test_user", "password": "abcdef", "expected_msg": "密码必须包含数字和字母"},
            {"username": "admin", "password": "Test123456", "expected_msg": "用户名已存在"},
        ]
    
    # ===================== 用户更新数据 =====================
    @staticmethod
    def get_update_user_data() -> Dict[str, Any]:
        """更新用户数据"""
        return {
            "real_name": "更新后的用户名",
            "phone": "13900139000",
            "email": "updated@example.com",
            "status": 1
        }
    
    # ===================== 用户查询数据 =====================
    @staticmethod
    def get_user_list_query_data() -> Dict[str, Any]:
        """用户列表查询数据"""
        return {
            "page": 1,
            "page_size": 10,
            "username": "",
            "status": None,
            "start_time": "",
            "end_time": ""
        }
    
    # ===================== 用户权限数据 =====================
    @staticmethod
    def get_assign_role_data() -> Dict[str, Any]:
        """分配角色数据"""
        return {
            "user_id": 1,
            "role_ids": [1, 2, 3]
        }
    
    @staticmethod
    def get_reset_password_data() -> Dict[str, Any]:
        """重置密码数据"""
        return {
            "user_id": 1,
            "new_password": "NewPassword123"
        }
