"""
短信通知模板相关API单接口测试
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.logger import Logger


@allure.feature('短信管理')
@allure.story('短信接口')
class TestSMSAPI:
    """短信相关API测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.logger = Logger()
        yield
        self.request.close()
    
    @allure.title('获取短信模板列表')
    @allure.severity('blocker')
    @allure.testcase('TC-SMS-001')
    def test_get_sms_template_list(self):
        """测试获取短信模板列表"""
        query_data = {
            'page': 1,
            'page_size': 10
        }
        
        response = self.request.get('/sms/template/list', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('创建短信模板')
    @allure.severity('critical')
    @allure.testcase('TC-SMS-002')
    def test_create_sms_template(self):
        """测试创建短信模板"""
        template_data = {
            'template_name': '订单发货通知',
            'template_code': 'SMS_001',
            'template_content': '您的订单{order_no}已发货，请耐心等待。',
            'template_type': 1
        }
        
        response = self.request.post('/sms/template/create', json=template_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('发送短信验证码')
    @allure.severity('critical')
    @allure.testcase('TC-SMS-003')
    def test_send_verify_code(self):
        """测试发送短信验证码"""
        sms_data = {
            'phone': '13800138000',
            'template_code': 'SMS_VERIFY',
            'params': {}
        }
        
        response = self.request.post('/sms/send', json=sms_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('验证短信验证码')
    @allure.severity('critical')
    @allure.testcase('TC-SMS-004')
    def test_verify_sms_code(self):
        """测试验证短信验证码"""
        verify_data = {
            'phone': '13800138000',
            'code': '123456'
        }
        
        response = self.request.post('/sms/verify', json=verify_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
    
    @allure.title('更新短信模板')
    @allure.severity('normal')
    @allure.testcase('TC-SMS-005')
    def test_update_sms_template(self):
        """测试更新短信模板"""
        template_id = 1
        update_data = {
            'template_name': '更新后的模板名称',
            'template_content': '更新后的模板内容'
        }
        
        response = self.request.put(f'/sms/template/{template_id}', json=update_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('删除短信模板')
    @allure.severity('normal')
    @allure.testcase('TC-SMS-006')
    def test_delete_sms_template(self):
        """测试删除短信模板"""
        template_id = 999
        
        response = self.request.delete(f'/sms/template/{template_id}')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
