"""
类目相关API单接口测试
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.logger import Logger
from test_data.category_data import CategoryData


@allure.feature('类目管理')
@allure.story('类目接口')
class TestCategoryAPI:
    """类目相关API测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.logger = Logger()
        yield
        self.request.close()
    
    @allure.title('创建类目-成功')
    @allure.severity('blocker')
    @allure.testcase('TC-CAT-001')
    def test_create_category_success(self):
        """测试创建类目成功"""
        category_data = CategoryData.get_create_category_success_data()
        
        response = self.request.post('/category/create', json=category_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('创建类目-失败')
    @allure.severity('critical')
    @allure.testcase('TC-CAT-002')
    @pytest.mark.parametrize('case', CategoryData.get_create_category_fail_data())
    def test_create_category_fail(self, case):
        """测试创建类目失败"""
        category_data = {k: v for k, v in case.items() if k != 'expected_msg'}
        expected_msg = case['expected_msg']
        
        response = self.request.post('/category/create', json=category_data)
        api_response = APIResponse(response)
        
        assert expected_msg in api_response.get_message()
    
    @allure.title('获取类目列表')
    @allure.severity('normal')
    @allure.testcase('TC-CAT-003')
    def test_get_category_list(self):
        """测试获取类目列表"""
        query_data = CategoryData.get_category_list_query_data()
        
        response = self.request.get('/category/list', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('获取类目树')
    @allure.severity('normal')
    @allure.testcase('TC-CAT-004')
    def test_get_category_tree(self):
        """测试获取类目树"""
        query_data = CategoryData.get_category_tree_query_data()
        
        response = self.request.get('/category/tree', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('更新类目')
    @allure.severity('normal')
    @allure.testcase('TC-CAT-005')
    def test_update_category(self):
        """测试更新类目"""
        category_id = 1
        update_data = CategoryData.get_update_category_data()
        
        response = self.request.put(f'/category/{category_id}', json=update_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('删除类目')
    @allure.severity('normal')
    @allure.testcase('TC-CAT-006')
    def test_delete_category(self):
        """测试删除类目"""
        category_id = 999
        
        response = self.request.delete(f'/category/{category_id}')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
