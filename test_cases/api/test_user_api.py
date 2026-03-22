"""
用户相关API单接口测试
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.logger import Logger
from test_data.user_data import UserData


@allure.feature('用户管理')
@allure.story('用户接口')
class TestUserAPI:
    """用户相关API测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.logger = Logger()
        self.logger.info("初始化用户API测试")
        yield
        self.request.close()
        self.logger.info("清理用户API测试环境")
    
    @allure.title('用户登录-成功')
    @allure.severity('blocker')
    @allure.testcase('TC-USER-001')
    def test_login_success(self):
        """测试用户登录成功"""
        # 准备数据
        login_data = UserData.get_login_success_data()
        
        # 发送请求
        self.logger.log_api_request('POST', '/user/login', data=login_data)
        response = self.request.post('/user/login', json=login_data)
        api_response = APIResponse(response)
        
        # 验证响应
        self.logger.log_api_response(response.status_code, api_response.json)
        
        assert response.status_code == 200
        assert api_response.is_success()
        assert api_response.get_code() == 200
        assert api_response.get_data().get('token') is not None
    
    @allure.title('用户登录-失败')
    @allure.severity('critical')
    @allure.testcase('TC-USER-002')
    @pytest.mark.parametrize('case', UserData.get_login_fail_data())
    def test_login_fail(self, case):
        """测试用户登录失败"""
        login_data = {
            'username': case['username'],
            'password': case['password']
        }
        expected_msg = case['expected_msg']
        
        response = self.request.post('/user/login', json=login_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert expected_msg in api_response.get_message()
    
    @allure.title('创建用户-成功')
    @allure.severity('critical')
    @allure.testcase('TC-USER-003')
    def test_create_user_success(self):
        """测试创建用户成功"""
        user_data = UserData.get_create_user_success_data()
        
        response = self.request.post('/user/create', json=user_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
        assert api_response.get_data().get('user_id') is not None
    
    @allure.title('创建用户-失败')
    @allure.severity('normal')
    @allure.testcase('TC-USER-004')
    @pytest.mark.parametrize('case', UserData.get_create_user_fail_data())
    def test_create_user_fail(self, case):
        """测试创建用户失败"""
        user_data = {k: v for k, v in case.items() if k != 'expected_msg'}
        expected_msg = case['expected_msg']
        
        response = self.request.post('/user/create', json=user_data)
        api_response = APIResponse(response)
        
        assert expected_msg in api_response.get_message()
    
    @allure.title('获取用户列表')
    @allure.severity('normal')
    @allure.testcase('TC-USER-005')
    def test_get_user_list(self):
        """测试获取用户列表"""
        query_data = UserData.get_user_list_query_data()
        
        response = self.request.get('/user/list', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
        assert 'list' in api_response.get_data()
    
    @allure.title('更新用户信息')
    @allure.severity('normal')
    @allure.testcase('TC-USER-006')
    def test_update_user(self):
        """测试更新用户信息"""
        user_id = 1
        update_data = UserData.get_update_user_data()
        
        response = self.request.put(f'/user/{user_id}', json=update_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('删除用户')
    @allure.severity('normal')
    @allure.testcase('TC-USER-007')
    def test_delete_user(self):
        """测试删除用户"""
        user_id = 999
        
        response = self.request.delete(f'/user/{user_id}')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
