"""
登录页面UI自动化测试
"""
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from page_objects.login_page import LoginPage
from config.config import Config
from common.logger import Logger


@allure.feature('登录模块')
@allure.story('登录页面UI测试')
class TestLoginUI:
    """登录页面UI测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """测试前置"""
        self.driver = driver
        self.login_page = LoginPage(self.driver)
        self.logger = Logger()
        self.logger.info("初始化登录UI测试")
        yield
        self.logger.info("清理登录UI测试环境")
    
    @allure.title('登录页面元素显示测试')
    @allure.severity('normal')
    @allure.testcase('TC-UI-001')
    def test_login_page_elements_display(self):
        """测试登录页面元素是否正确显示"""
        # 打开登录页面
        self.login_page.open_login_page()
        
        # 验证页面元素
        assert self.login_page.is_displayed(LoginPage.USERNAME_INPUT), "用户名输入框未显示"
        assert self.login_page.is_displayed(LoginPage.PASSWORD_INPUT), "密码输入框未显示"
        assert self.login_page.is_displayed(LoginPage.LOGIN_BUTTON), "登录按钮未显示"
        assert self.login_page.is_login_button_enabled(), "登录按钮不可用"
    
    @allure.title('用户登录成功测试')
    @allure.severity('blocker')
    @allure.testcase('TC-UI-002')
    def test_login_success(self):
        """测试用户登录成功"""
        # 打开登录页面
        self.login_page.open_login_page()
        
        # 执行登录
        account = Config.get_test_account('admin')
        self.login_page.login(account['username'], account['password'])
        
        # 验证登录成功
        assert self.login_page.is_login_success(), "登录失败"
        
        # 截图
        self.login_page.take_screenshot('login_success.png')
    
    @allure.title('用户登录失败测试-空用户名')
    @allure.severity('critical')
    @allure.testcase('TC-UI-003')
    def test_login_empty_username(self):
        """测试空用户名登录"""
        self.login_page.open_login_page()
        
        # 只输入密码
        self.login_page.input_password('admin123')
        self.login_page.click_login_button()
        
        # 验证错误提示
        error_msg = self.login_page.get_error_message()
        assert '用户名' in error_msg or 'username' in error_msg.lower()
    
    @allure.title('用户登录失败测试-空密码')
    @allure.severity('critical')
    @allure.testcase('TC-UI-004')
    def test_login_empty_password(self):
        """测试空密码登录"""
        self.login_page.open_login_page()
        
        # 只输入用户名
        self.login_page.input_username('admin')
        self.login_page.click_login_button()
        
        # 验证错误提示
        error_msg = self.login_page.get_error_message()
        assert '密码' in error_msg or 'password' in error_msg.lower()
    
    @allure.title('用户登录失败测试-错误密码')
    @allure.severity('critical')
    @allure.testcase('TC-UI-005')
    def test_login_wrong_password(self):
        """测试错误密码登录"""
        self.login_page.open_login_page()
        
        # 输入错误密码
        self.login_page.login('admin', 'wrongpassword')
        
        # 验证错误提示
        error_msg = self.login_page.get_error_message()
        assert '密码' in error_msg or '错误' in error_msg or 'error' in error_msg.lower()
        
        # 截图
        self.login_page.take_screenshot('login_wrong_password.png')
    
    @allure.title('记住密码功能测试')
    @allure.severity('normal')
    @allure.testcase('TC-UI-006')
    def test_remember_password(self):
        """测试记住密码功能"""
        self.login_page.open_login_page()
        
        # 勾选记住密码并登录
        account = Config.get_test_account('admin')
        self.login_page.input_username(account['username'])
        self.login_page.input_password(account['password'])
        self.login_page.check_remember()
        self.login_page.click_login_button()
        
        # 验证登录成功
        assert self.login_page.is_login_success()
        
        # TODO: 验证cookie或其他记住密码机制
    
    @allure.title('忘记密码链接测试')
    @allure.severity('minor')
    @allure.testcase('TC-UI-007')
    def test_forgot_password_link(self):
        """测试忘记密码链接"""
        self.login_page.open_login_page()
        
        # 点击忘记密码
        self.login_page.click(LoginPage.FORGOT_PASSWORD_LINK)
        
        # 验证跳转到忘记密码页面
        current_url = self.login_page.get_current_url()
        assert 'forgot' in current_url or 'reset' in current_url
