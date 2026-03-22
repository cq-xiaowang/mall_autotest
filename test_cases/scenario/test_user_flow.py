"""
用户相关场景自动化测试
测试用户管理的完整业务流程
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.db_handler import DBHandler
from common.logger import Logger
from test_data.user_data import UserData


@allure.feature('用户管理')
@allure.story('用户场景测试')
class TestUserFlow:
    """用户场景测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.db = DBHandler()
        self.logger = Logger()
        self.user_ids = []
        self.auth_token = None
        yield
        self._cleanup_test_data()
        self.request.close()
        self.db.close()
    
    def _cleanup_test_data(self):
        """清理测试数据"""
        if self.user_ids:
            for user_id in self.user_ids:
                try:
                    self.request.delete(f'/user/{user_id}')
                except Exception:
                    pass
    
    @allure.title('用户登录到权限验证完整流程')
    @allure.severity('blocker')
    @allure.testcase('TC-SCENE-004')
    def test_user_login_and_permission_flow(self):
        """
        测试用户登录和权限验证流程：
        1. 用户登录获取token
        2. 使用token访问受保护资源
        3. 验证用户权限
        4. 修改用户角色
        5. 验证权限变化
        """
        # Step 1: 用户登录
        self.logger.info("Step 1: 用户登录")
        login_data = UserData.get_login_success_data()
        login_response = self.request.post('/user/login', json=login_data)
        login_api_response = APIResponse(login_response)
        
        assert login_api_response.is_success(), "登录失败"
        self.auth_token = login_api_response.get_data().get('token')
        assert self.auth_token is not None, "未获取到token"
        
        # 设置token到请求头
        self.request.set_auth_token(self.auth_token)
        
        # Step 2: 访问受保护资源
        self.logger.info("Step 2: 访问受保护资源")
        profile_response = self.request.get('/user/profile')
        profile_api_response = APIResponse(profile_response)
        
        assert profile_api_response.is_success(), "访问用户信息失败"
        
        # Step 3: 验证用户权限
        self.logger.info("Step 3: 验证用户权限")
        permissions_response = self.request.get('/user/permissions')
        permissions_api_response = APIResponse(permissions_response)
        
        assert permissions_api_response.is_success(), "获取权限列表失败"
        permissions = permissions_api_response.get_data().get('permissions', [])
        assert len(permissions) > 0, "用户无任何权限"
    
    @allure.title('用户注册到激活完整流程')
    @allure.severity('critical')
    @allure.testcase('TC-SCENE-005')
    def test_user_register_flow(self):
        """
        测试用户注册到激活流程：
        1. 创建新用户
        2. 验证用户状态
        3. 激活用户
        4. 使用新用户登录
        5. 修改密码
        """
        # Step 1: 创建新用户
        self.logger.info("Step 1: 创建新用户")
        user_data = UserData.get_create_user_success_data()
        user_data['status'] = 0  # 初始状态为未激活
        
        create_response = self.request.post('/user/create', json=user_data)
        create_api_response = APIResponse(create_response)
        
        assert create_api_response.is_success(), "创建用户失败"
        user_id = create_api_response.get_data().get('user_id')
        self.user_ids.append(user_id)
        
        # Step 2: 验证用户状态
        self.logger.info("Step 2: 验证用户状态")
        db_user = self.db.query_one("SELECT * FROM user WHERE id = %s", (user_id,))
        assert db_user['status'] == 0, "用户初始状态错误"
        
        # Step 3: 激活用户
        self.logger.info("Step 3: 激活用户")
        activate_response = self.request.put(f'/user/{user_id}/status', json={'status': 1})
        assert APIResponse(activate_response).is_success(), "激活用户失败"
        
        # 验证数据库
        db_user = self.db.query_one("SELECT * FROM user WHERE id = %s", (user_id,))
        assert db_user['status'] == 1, "用户状态未更新"
        
        # Step 4: 使用新用户登录
        self.logger.info("Step 4: 使用新用户登录")
        login_response = self.request.post('/user/login', json={
            'username': user_data['username'],
            'password': user_data['password']
        })
        assert APIResponse(login_response).is_success(), "新用户登录失败"
        
        # Step 5: 修改密码
        self.logger.info("Step 5: 修改密码")
        new_password_data = {
            'old_password': user_data['password'],
            'new_password': 'NewPassword123'
        }
        change_pwd_response = self.request.put('/user/password', json=new_password_data)
        assert APIResponse(change_pwd_response).is_success(), "修改密码失败"
    
    @allure.title('用户角色分配流程测试')
    @allure.severity('normal')
    @allure.testcase('TC-SCENE-006')
    def test_user_role_assignment_flow(self):
        """
        测试用户角色分配流程：
        1. 创建用户
        2. 获取可用角色列表
        3. 分配角色
        4. 验证角色分配结果
        5. 移除角色
        """
        # Step 1: 创建用户
        user_data = UserData.get_create_user_success_data()
        create_response = self.request.post('/user/create', json=user_data)
        create_api_response = APIResponse(create_response)
        
        assert create_api_response.is_success()
        user_id = create_api_response.get_data().get('user_id')
        self.user_ids.append(user_id)
        
        # Step 2: 获取角色列表
        roles_response = self.request.get('/role/list')
        roles_api_response = APIResponse(roles_response)
        
        assert roles_api_response.is_success()
        roles = roles_api_response.get_data().get('list', [])
        assert len(roles) > 0, "无可用角色"
        
        # Step 3: 分配角色
        role_ids = [roles[0]['id']]
        assign_data = UserData.get_assign_role_data()
        assign_data['user_id'] = user_id
        assign_data['role_ids'] = role_ids
        
        assign_response = self.request.post('/user/assign-role', json=assign_data)
        assert APIResponse(assign_response).is_success(), "分配角色失败"
        
        # Step 4: 验证角色分配
        user_roles_response = self.request.get(f'/user/{user_id}/roles')
        user_roles = APIResponse(user_roles_response).get_data().get('roles', [])
        assert len(user_roles) > 0, "用户角色分配失败"
        
        # Step 5: 移除角色
        remove_data = {'user_id': user_id, 'role_ids': []}
        remove_response = self.request.post('/user/assign-role', json=remove_data)
        assert APIResponse(remove_response).is_success(), "移除角色失败"
