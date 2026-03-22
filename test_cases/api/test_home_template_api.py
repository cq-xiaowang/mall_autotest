"""
商城首页模板管理API测试
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.logger import Logger


@allure.feature('首页模板管理')
@allure.story('首页模板接口')
class TestHomePageTemplateAPI:
    """首页模板管理API测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.logger = Logger()
        yield
        self.request.close()
    
    @allure.title('获取首页模板列表')
    @allure.severity('blocker')
    @allure.testcase('TC-HOME-001')
    def test_get_template_list(self):
        """测试获取首页模板列表"""
        query_data = {
            'page': 1,
            'page_size': 10
        }
        
        response = self.request.get('/home-template/list', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('创建首页模板')
    @allure.severity('critical')
    @allure.testcase('TC-HOME-002')
    def test_create_template(self):
        """测试创建首页模板"""
        template_data = {
            'template_name': '春节活动模板',
            'template_type': 'activity',
            'start_time': '2024-01-01 00:00:00',
            'end_time': '2024-02-15 23:59:59',
            'status': 0,
            'config': {
                'banners': [
                    {'image': 'https://example.com/banner1.jpg', 'link': '/activity/1'}
                ],
                'sections': [
                    {'type': 'product_list', 'title': '热门推荐', 'product_ids': [1, 2, 3]}
                ]
            }
        }
        
        response = self.request.post('/home-template/create', json=template_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('更新首页模板')
    @allure.severity('normal')
    @allure.testcase('TC-HOME-003')
    def test_update_template(self):
        """测试更新首页模板"""
        template_id = 1
        update_data = {
            'template_name': '更新后的模板名称',
            'status': 1
        }
        
        response = self.request.put(f'/home-template/{template_id}', json=update_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('发布首页模板')
    @allure.severity('critical')
    @allure.testcase('TC-HOME-004')
    def test_publish_template(self):
        """测试发布首页模板"""
        template_id = 1
        publish_data = {
            'status': 1
        }
        
        response = self.request.put(f'/home-template/{template_id}/publish', json=publish_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('预览首页模板')
    @allure.severity('normal')
    @allure.testcase('TC-HOME-005')
    def test_preview_template(self):
        """测试预览首页模板"""
        template_id = 1
        
        response = self.request.get(f'/home-template/{template_id}/preview')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('删除首页模板')
    @allure.severity('normal')
    @allure.testcase('TC-HOME-006')
    def test_delete_template(self):
        """测试删除首页模板"""
        template_id = 999
        
        response = self.request.delete(f'/home-template/{template_id}')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
