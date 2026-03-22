"""
类目相关测试数据
"""
from typing import Dict, List, Any
import time


class CategoryData:
    """类目测试数据类"""
    
    # ===================== 类目创建数据 =====================
    @staticmethod
    def get_create_category_success_data() -> Dict[str, Any]:
        """创建类目成功数据"""
        timestamp = int(time.time() * 1000)
        return {
            "category_name": f"测试类目_{timestamp}",
            "parent_id": 0,  # 一级类目
            "level": 1,
            "icon": "https://example.com/icon.jpg",
            "sort_order": 0,
            "status": 1,
            "description": "测试类目描述"
        }
    
    @staticmethod
    def get_create_sub_category_data() -> Dict[str, Any]:
        """创建子类目数据"""
        timestamp = int(time.time() * 1000)
        return {
            "category_name": f"子类目_{timestamp}",
            "parent_id": 1,  # 父类目ID
            "level": 2,
            "sort_order": 0,
            "status": 1
        }
    
    @staticmethod
    def get_create_category_fail_data() -> List[Dict[str, Any]]:
        """创建类目失败数据集合"""
        return [
            {"category_name": "", "expected_msg": "类目名称不能为空"},
            {"category_name": "a" * 51, "expected_msg": "类目名称不能超过50个字符"},
            {"parent_id": -1, "expected_msg": "父类目不存在"},
            {"level": 4, "expected_msg": "类目层级不能超过3级"},
        ]
    
    # ===================== 类目更新数据 =====================
    @staticmethod
    def get_update_category_data() -> Dict[str, Any]:
        """更新类目数据"""
        return {
            "category_name": "更新后的类目名称",
            "icon": "https://example.com/new_icon.jpg",
            "sort_order": 10,
            "status": 1
        }
    
    # ===================== 类目查询数据 =====================
    @staticmethod
    def get_category_list_query_data() -> Dict[str, Any]:
        """类目列表查询数据"""
        return {
            "parent_id": None,  # 不传则查询所有
            "status": None,
            "level": None
        }
    
    @staticmethod
    def get_category_tree_query_data() -> Dict[str, Any]:
        """类目树查询数据"""
        return {
            "max_level": 3
        }
    
    # ===================== 类目状态数据 =====================
    @staticmethod
    def get_category_status_data() -> Dict[str, Any]:
        """类目状态数据"""
        return [
            {"category_id": 1, "status": 1, "expected_msg": "启用成功"},
            {"category_id": 1, "status": 0, "expected_msg": "禁用成功"},
        ]
