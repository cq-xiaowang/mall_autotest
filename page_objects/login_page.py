"""
登录页面对象
"""
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from config.config import Config


class LoginPage(BasePage):
    """登录页面"""
    
    # 页面URL
    LOGIN_URL = '/login'
    
    # 页面元素定位器
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'btn-login')
    CAPTCHA_INPUT = (By.ID, 'captcha')
    CAPTCHA_IMAGE = (By.ID, 'captcha-img')
    ERROR_MESSAGE = (By.CLASS_NAME, 'error-message')
    REMEMBER_CHECKBOX = (By.ID, 'remember')
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, '忘记密码')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_login_page(self):
        """打开登录页面"""
        url = Config.get_full_url(self.LOGIN_URL)
        self.open(url)
        return self
    
    def input_username(self, username: str):
        """输入用户名"""
        self.send_keys(self.USERNAME_INPUT, username)
        return self
    
    def input_password(self, password: str):
        """输入密码"""
        self.send_keys(self.PASSWORD_INPUT, password)
        return self
    
    def input_captcha(self, captcha: str):
        """输入验证码"""
        self.send_keys(self.CAPTCHA_INPUT, captcha)
        return self
    
    def click_login_button(self):
        """点击登录按钮"""
        self.click(self.LOGIN_BUTTON)
        return self
    
    def check_remember(self):
        """勾选记住密码"""
        if not self.is_selected(self.REMEMBER_CHECKBOX):
            self.click(self.REMEMBER_CHECKBOX)
        return self
    
    def get_error_message(self) -> str:
        """获取错误提示信息"""
        if self.is_displayed(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return ''
    
    def is_login_button_enabled(self) -> bool:
        """登录按钮是否可用"""
        return self.is_enabled(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str, captcha: str = ''):
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
            captcha: 验证码（可选）
        """
        self.input_username(username)
        self.input_password(password)
        if captcha:
            self.input_captcha(captcha)
        self.click_login_button()
    
    def login_with_admin(self):
        """使用管理员账号登录"""
        account = Config.get_test_account('admin')
        self.login(account['username'], account['password'])
    
    def is_login_page(self) -> bool:
        """是否在登录页面"""
        return '/login' in self.get_current_url()
    
    def is_login_success(self) -> bool:
        """是否登录成功"""
        # 等待跳转到首页
        import time
        time.sleep(2)
        return '/login' not in self.get_current_url()
