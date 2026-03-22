"""
商品相关测试数据
"""
from typing import Dict, List, Any
import time


class ProductData:
    """商品测试数据类"""
    
    # ===================== 商品创建数据 =====================
    @staticmethod
    def get_create_product_success_data() -> Dict[str, Any]:
        """创建商品成功数据"""
        timestamp = int(time.time() * 1000)
        return {
            "product_name": f"测试商品_{timestamp}",
            "product_code": f"PROD{timestamp}",
            "category_id": 1,
            "brand_id": 1,
            "price": 99.99,
            "original_price": 199.99,
            "stock": 1000,
            "low_stock": 10,
            "unit": "件",
            "weight": 0.5,
            "brief": "这是一个测试商品",
            "description": "<p>商品详细描述</p>",
            "main_image": "https://example.com/image.jpg",
            "sub_images": [
                "https://example.com/image1.jpg",
                "https://example.com/image2.jpg"
            ],
            "status": 1,  # 上架状态
            "sort_order": 0
        }
    
    @staticmethod
    def get_create_product_fail_data() -> List[Dict[str, Any]]:
        """创建商品失败数据集合"""
        return [
            {"product_name": "", "expected_msg": "商品名称不能为空"},
            {"product_name": "a" * 201, "expected_msg": "商品名称不能超过200个字符"},
            {"product_name": "测试商品", "price": -1, "expected_msg": "价格不能为负数"},
            {"product_name": "测试商品", "price": "abc", "expected_msg": "价格格式不正确"},
            {"product_name": "测试商品", "stock": -1, "expected_msg": "库存不能为负数"},
            {"product_name": "测试商品", "category_id": None, "expected_msg": "商品类目不能为空"},
        ]
    
    # ===================== 商品更新数据 =====================
    @staticmethod
    def get_update_product_data() -> Dict[str, Any]:
        """更新商品数据"""
        return {
            "product_name": "更新后的商品名称",
            "price": 88.88,
            "stock": 500,
            "status": 1
        }
    
    @staticmethod
    def get_update_stock_data() -> Dict[str, Any]:
        """更新商品库存数据"""
        return {
            "product_id": 1,
            "stock_change": -10,  # 负数表示减少库存
            "remark": "订单扣减库存"
        }
    
    # ===================== 商品查询数据 =====================
    @staticmethod
    def get_product_list_query_data() -> Dict[str, Any]:
        """商品列表查询数据"""
        return {
            "page": 1,
            "page_size": 10,
            "product_name": "",
            "product_code": "",
            "category_id": None,
            "brand_id": None,
            "status": None,
            "min_price": None,
            "max_price": None,
            "sort_field": "create_time",
            "sort_order": "desc"
        }
    
    @staticmethod
    def get_product_detail_query_data() -> Dict[str, Any]:
        """商品详情查询数据"""
        return {
            "product_id": 1
        }
    
    # ===================== 商品上下架数据 =====================
    @staticmethod
    def get_product_status_data() -> Dict[str, Any]:
        """商品上下架数据"""
        return [
            {"product_id": 1, "status": 1, "expected_msg": "上架成功"},
            {"product_id": 1, "status": 0, "expected_msg": "下架成功"},
        ]
    
    # ===================== 商品批量操作数据 =====================
    @staticmethod
    def get_batch_update_status_data() -> Dict[str, Any]:
        """批量更新状态数据"""
        return {
            "product_ids": [1, 2, 3],
            "status": 1
        }
    
    @staticmethod
    def get_batch_delete_data() -> Dict[str, Any]:
        """批量删除数据"""
        return {
            "product_ids": [1, 2, 3]
        }
