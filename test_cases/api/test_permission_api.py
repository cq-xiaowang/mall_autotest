"""
权限相关API单接口测试
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.logger import Logger


@allure.feature('权限管理')
@allure.story('权限接口')
class TestPermissionAPI:
    """权限相关API测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.logger = Logger()
        yield
        self.request.close()
    
    @allure.title('获取角色列表')
    @allure.severity('blocker')
    @allure.testcase('TC-PERM-001')
    def test_get_role_list(self):
        """测试获取角色列表"""
        response = self.request.get('/role/list')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
        assert 'list' in api_response.get_data()
    
    @allure.title('创建角色')
    @allure.severity('critical')
    @allure.testcase('TC-PERM-002')
    def test_create_role(self):
        """测试创建角色"""
        role_data = {
            'role_name': '测试角色',
            'role_code': 'test_role',
            'description': '测试角色描述',
            'permission_ids': [1, 2, 3]
        }
        
        response = self.request.post('/role/create', json=role_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('更新角色权限')
    @allure.severity('critical')
    @allure.testcase('TC-PERM-003')
    def test_update_role_permissions(self):
        """测试更新角色权限"""
        role_id = 1
        permission_data = {
            'permission_ids': [1, 2, 3, 4, 5]
        }
        
        response = self.request.put(f'/role/{role_id}/permissions', json=permission_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('获取权限列表')
    @allure.severity('normal')
    @allure.testcase('TC-PERM-004')
    def test_get_permission_list(self):
        """测试获取权限列表"""
        response = self.request.get('/permission/list')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('删除角色')
    @allure.severity('normal')
    @allure.testcase('TC-PERM-005')
    def test_delete_role(self):
        """测试删除角色"""
        role_id = 999
        
        response = self.request.delete(f'/role/{role_id}')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
