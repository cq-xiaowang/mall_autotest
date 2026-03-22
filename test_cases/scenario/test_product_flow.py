"""
商品相关场景自动化测试
测试商品管理的完整业务流程
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.db_handler import DBHandler
from common.logger import Logger
from test_data.product_data import ProductData
from test_data.category_data import CategoryData


@allure.feature('商品管理')
@allure.story('商品场景测试')
class TestProductFlow:
    """商品场景测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.db = DBHandler()
        self.logger = Logger()
        self.product_ids = []  # 记录创建的商品ID，用于清理
        yield
        # 清理测试数据
        self._cleanup_test_data()
        self.request.close()
        self.db.close()
    
    def _cleanup_test_data(self):
        """清理测试数据"""
        if self.product_ids:
            for product_id in self.product_ids:
                try:
                    self.request.delete(f'/product/{product_id}')
                except Exception:
                    pass
            self.logger.info(f"清理测试数据: {self.product_ids}")
    
    @allure.title('商品完整生命周期测试')
    @allure.severity('blocker')
    @allure.testcase('TC-SCENE-001')
    def test_product_lifecycle(self):
        """
        测试商品完整生命周期：
        1. 创建类目
        2. 创建商品
        3. 查询商品
        4. 更新商品
        5. 上架商品
        6. 下架商品
        7. 删除商品
        """
        # Step 1: 创建类目
        self.logger.info("Step 1: 创建类目")
        category_data = CategoryData.get_create_category_success_data()
        category_response = self.request.post('/category/create', json=category_data)
        category_api_response = APIResponse(category_response)
        
        assert category_api_response.is_success(), "创建类目失败"
        category_id = category_api_response.get_data().get('category_id')
        
        # Step 2: 创建商品
        self.logger.info("Step 2: 创建商品")
        product_data = ProductData.get_create_product_success_data()
        product_data['category_id'] = category_id
        create_response = self.request.post('/product/create', json=product_data)
        create_api_response = APIResponse(create_response)
        
        assert create_api_response.is_success(), "创建商品失败"
        product_id = create_api_response.get_data().get('product_id')
        self.product_ids.append(product_id)
        
        # Step 3: 查询商品
        self.logger.info("Step 3: 查询商品")
        get_response = self.request.get(f'/product/{product_id}')
        get_api_response = APIResponse(get_response)
        
        assert get_api_response.is_success(), "查询商品失败"
        assert get_api_response.get_data().get('product_name') == product_data['product_name']
        
        # Step 4: 更新商品
        self.logger.info("Step 4: 更新商品")
        update_data = ProductData.get_update_product_data()
        update_response = self.request.put(f'/product/{product_id}', json=update_data)
        update_api_response = APIResponse(update_response)
        
        assert update_api_response.is_success(), "更新商品失败"
        
        # Step 5: 上架商品
        self.logger.info("Step 5: 上架商品")
        online_response = self.request.put(f'/product/{product_id}/status', json={'status': 1})
        online_api_response = APIResponse(online_response)
        
        assert online_api_response.is_success(), "上架商品失败"
        
        # 验证数据库状态
        db_product = self.db.query_one(
            "SELECT * FROM product WHERE id = %s", (product_id,)
        )
        assert db_product['status'] == 1, "数据库商品状态未更新"
        
        # Step 6: 下架商品
        self.logger.info("Step 6: 下架商品")
        offline_response = self.request.put(f'/product/{product_id}/status', json={'status': 0})
        offline_api_response = APIResponse(offline_response)
        
        assert offline_api_response.is_success(), "下架商品失败"
        
        # Step 7: 删除商品
        self.logger.info("Step 7: 删除商品")
        delete_response = self.request.delete(f'/product/{product_id}')
        delete_api_response = APIResponse(delete_response)
        
        assert delete_api_response.is_success(), "删除商品失败"
        self.product_ids.remove(product_id)  # 已删除，无需清理
    
    @allure.title('商品库存管理流程测试')
    @allure.severity('critical')
    @allure.testcase('TC-SCENE-002')
    def test_product_stock_flow(self):
        """
        测试商品库存管理流程：
        1. 创建商品
        2. 验证初始库存
        3. 减少库存（模拟下单）
        4. 验证库存变化
        5. 增加库存（模拟退货）
        6. 验证库存变化
        """
        # 创建商品
        product_data = ProductData.get_create_product_success_data()
        product_data['stock'] = 100
        
        create_response = self.request.post('/product/create', json=product_data)
        create_api_response = APIResponse(create_response)
        
        assert create_api_response.is_success()
        product_id = create_api_response.get_data().get('product_id')
        self.product_ids.append(product_id)
        
        # 验证初始库存
        initial_stock = self._get_product_stock(product_id)
        assert initial_stock == 100, f"初始库存错误，期望100，实际{initial_stock}"
        
        # 减少库存
        update_stock_data = ProductData.get_update_stock_data()
        update_stock_data['product_id'] = product_id
        update_stock_data['stock_change'] = -10
        
        self.request.put('/product/stock', json=update_stock_data)
        
        # 验证库存变化
        updated_stock = self._get_product_stock(product_id)
        assert updated_stock == 90, f"扣减后库存错误，期望90，实际{updated_stock}"
        
        # 增加库存
        update_stock_data['stock_change'] = 5
        self.request.put('/product/stock', json=update_stock_data)
        
        # 验证库存变化
        final_stock = self._get_product_stock(product_id)
        assert final_stock == 95, f"增加后库存错误，期望95，实际{final_stock}"
    
    def _get_product_stock(self, product_id: int) -> int:
        """获取商品库存"""
        response = self.request.get(f'/product/{product_id}')
        api_response = APIResponse(response)
        return api_response.get_data().get('stock', 0)
    
    @allure.title('商品批量操作测试')
    @allure.severity('normal')
    @allure.testcase('TC-SCENE-003')
    def test_batch_product_operations(self):
        """
        测试商品批量操作：
        1. 批量创建商品
        2. 批量上架
        3. 批量下架
        4. 批量删除
        """
        # 批量创建商品
        created_ids = []
        for i in range(3):
            product_data = ProductData.get_create_product_success_data()
            response = self.request.post('/product/create', json=product_data)
            api_response = APIResponse(response)
            assert api_response.is_success()
            created_ids.append(api_response.get_data().get('product_id'))
        
        self.product_ids.extend(created_ids)
        
        # 批量上架
        batch_data = {'product_ids': created_ids, 'status': 1}
        batch_response = self.request.put('/product/batch/status', json=batch_data)
        assert APIResponse(batch_response).is_success()
        
        # 验证所有商品状态
        for product_id in created_ids:
            stock = self._get_product_stock(product_id)
            assert stock >= 0
        
        # 批量下架
        batch_data['status'] = 0
        batch_response = self.request.put('/product/batch/status', json=batch_data)
        assert APIResponse(batch_response).is_success()
        
        # 批量删除
        delete_data = {'product_ids': created_ids}
        delete_response = self.request.delete('/product/batch', json=delete_data)
        assert APIResponse(delete_response).is_success()
        
        # 清理ID列表
        for pid in created_ids:
            if pid in self.product_ids:
                self.product_ids.remove(pid)
