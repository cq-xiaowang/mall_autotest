"""
商品相关API单接口测试
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.logger import Logger
from test_data.product_data import ProductData


@allure.feature('商品管理')
@allure.story('商品接口')
class TestProductAPI:
    """商品相关API测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.logger = Logger()
        yield
        self.request.close()
    
    @allure.title('创建商品-成功')
    @allure.severity('blocker')
    @allure.testcase('TC-PROD-001')
    def test_create_product_success(self):
        """测试创建商品成功"""
        product_data = ProductData.get_create_product_success_data()
        
        response = self.request.post('/product/create', json=product_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
        assert api_response.get_data().get('product_id') is not None
    
    @allure.title('创建商品-失败')
    @allure.severity('critical')
    @allure.testcase('TC-PROD-002')
    @pytest.mark.parametrize('case', ProductData.get_create_product_fail_data())
    def test_create_product_fail(self, case):
        """测试创建商品失败"""
        product_data = {k: v for k, v in case.items() if k != 'expected_msg'}
        expected_msg = case['expected_msg']
        
        response = self.request.post('/product/create', json=product_data)
        api_response = APIResponse(response)
        
        assert expected_msg in api_response.get_message()
    
    @allure.title('获取商品列表')
    @allure.severity('normal')
    @allure.testcase('TC-PROD-003')
    def test_get_product_list(self):
        """测试获取商品列表"""
        query_data = ProductData.get_product_list_query_data()
        
        response = self.request.get('/product/list', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
        assert 'list' in api_response.get_data()
    
    @allure.title('获取商品详情')
    @allure.severity('normal')
    @allure.testcase('TC-PROD-004')
    def test_get_product_detail(self):
        """测试获取商品详情"""
        product_id = 1
        
        response = self.request.get(f'/product/{product_id}')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('更新商品信息')
    @allure.severity('normal')
    @allure.testcase('TC-PROD-005')
    def test_update_product(self):
        """测试更新商品信息"""
        product_id = 1
        update_data = ProductData.get_update_product_data()
        
        response = self.request.put(f'/product/{product_id}', json=update_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('商品上架')
    @allure.severity('critical')
    @allure.testcase('TC-PROD-006')
    def test_product_online(self):
        """测试商品上架"""
        product_id = 1
        status_data = {'status': 1}
        
        response = self.request.put(f'/product/{product_id}/status', json=status_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('商品下架')
    @allure.severity('critical')
    @allure.testcase('TC-PROD-007')
    def test_product_offline(self):
        """测试商品下架"""
        product_id = 1
        status_data = {'status': 0}
        
        response = self.request.put(f'/product/{product_id}/status', json=status_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('删除商品')
    @allure.severity('normal')
    @allure.testcase('TC-PROD-008')
    def test_delete_product(self):
        """测试删除商品"""
        product_id = 999
        
        response = self.request.delete(f'/product/{product_id}')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
    
    @allure.title('批量更新商品状态')
    @allure.severity('normal')
    @allure.testcase('TC-PROD-009')
    def test_batch_update_status(self):
        """测试批量更新商品状态"""
        batch_data = ProductData.get_batch_update_status_data()
        
        response = self.request.put('/product/batch/status', json=batch_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
