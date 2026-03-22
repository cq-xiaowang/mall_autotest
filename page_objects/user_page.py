"""
用户管理页面对象
"""
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from config.config import Config


class UserPage(BasePage):
    """用户管理页面"""
    
    # 页面URL
    USER_LIST_URL = '/user/list'
    
    # 用户列表页元素
    USERNAME_INPUT = (By.ID, 'search-username')
    STATUS_SELECT = (By.ID, 'search-status')
    SEARCH_BUTTON = (By.ID, 'btn-search')
    RESET_BUTTON = (By.ID, 'btn-reset')
    ADD_USER_BUTTON = (By.ID, 'btn-add-user')
    USER_TABLE = (By.ID, 'user-table')
    USER_ROW = (By.CLASS_NAME, 'user-row')
    
    # 用户表单元素
    USER_FORM = (By.ID, 'user-form')
    FORM_USERNAME_INPUT = (By.ID, 'form-username')
    FORM_PASSWORD_INPUT = (By.ID, 'form-password')
    FORM_REALNAME_INPUT = (By.ID, 'form-realname')
    FORM_PHONE_INPUT = (By.ID, 'form-phone')
    FORM_EMAIL_INPUT = (By.ID, 'form-email')
    FORM_STATUS_SELECT = (By.ID, 'form-status')
    FORM_ROLE_CHECKBOXES = (By.NAME, 'role-ids')
    SUBMIT_BUTTON = (By.ID, 'btn-submit')
    CANCEL_BUTTON = (By.ID, 'btn-cancel')
    
    # 操作按钮
    EDIT_BUTTON = (By.CLASS_NAME, 'btn-edit')
    DELETE_BUTTON = (By.CLASS_NAME, 'btn-delete')
    RESET_PWD_BUTTON = (By.CLASS_NAME, 'btn-reset-pwd')
    ASSIGN_ROLE_BUTTON = (By.CLASS_NAME, 'btn-assign-role')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_user_list(self):
        """打开用户列表页面"""
        url = Config.get_full_url(self.USER_LIST_URL)
        self.open(url)
        return self
    
    def search_by_username(self, username: str):
        """按用户名搜索"""
        self.send_keys(self.USERNAME_INPUT, username)
        self.click(self.SEARCH_BUTTON)
        return self
    
    def search_by_status(self, status: int):
        """按状态搜索"""
        self.select_by_value(self.STATUS_SELECT, str(status))
        self.click(self.SEARCH_BUTTON)
        return self
    
    def reset_search(self):
        """重置搜索条件"""
        self.click(self.RESET_BUTTON)
        return self
    
    def click_add_user(self):
        """点击添加用户按钮"""
        self.click(self.ADD_USER_BUTTON)
        return self
    
    def fill_user_form(self, user_data: dict):
        """
        填写用户表单
        
        Args:
            user_data: 用户数据字典
        """
        if 'username' in user_data:
            self.send_keys(self.FORM_USERNAME_INPUT, user_data['username'])
        if 'password' in user_data:
            self.send_keys(self.FORM_PASSWORD_INPUT, user_data['password'])
        if 'real_name' in user_data:
            self.send_keys(self.FORM_REALNAME_INPUT, user_data['real_name'])
        if 'phone' in user_data:
            self.send_keys(self.FORM_PHONE_INPUT, user_data['phone'])
        if 'email' in user_data:
            self.send_keys(self.FORM_EMAIL_INPUT, user_data['email'])
        if 'status' in user_data:
            self.select_by_value(self.FORM_STATUS_SELECT, str(user_data['status']))
        
        return self
    
    def submit_user_form(self):
        """提交用户表单"""
        self.click(self.SUBMIT_BUTTON)
        return self
    
    def cancel_user_form(self):
        """取消用户表单"""
        self.click(self.CANCEL_BUTTON)
        return self
    
    def get_user_count(self) -> int:
        """获取用户列表数量"""
        rows = self.find_elements(self.USER_ROW)
        return len(rows)
    
    def edit_user(self, user_id: int):
        """编辑用户"""
        edit_btn = (By.XPATH, f"//tr[@data-id='{user_id}']//button[contains(@class, 'btn-edit')]")
        self.click(edit_btn)
        return self
    
    def delete_user(self, user_id: int):
        """删除用户"""
        delete_btn = (By.XPATH, f"//tr[@data-id='{user_id}']//button[contains(@class, 'btn-delete')]")
        self.click(delete_btn)
        # 确认删除
        self.click((By.CLASS_NAME, 'btn-confirm-yes'))
        return self
    
    def reset_password(self, user_id: int):
        """重置用户密码"""
        reset_btn = (By.XPATH, f"//tr[@data-id='{user_id}']//button[contains(@class, 'btn-reset-pwd')]")
        self.click(reset_btn)
        return self
    
    def assign_role(self, user_id: int, role_ids: list):
        """
        分配角色
        
        Args:
            user_id: 用户ID
            role_ids: 角色ID列表
        """
        assign_btn = (By.XPATH, f"//tr[@data-id='{user_id}']//button[contains(@class, 'btn-assign-role')]")
        self.click(assign_btn)
        
        # 选择角色
        for role_id in role_ids:
            checkbox = (By.XPATH, f"//input[@name='role-ids' and @value='{role_id}']")
            if not self.is_selected(checkbox):
                self.click(checkbox)
        
        # 确认
        self.click((By.ID, 'btn-confirm-assign'))
        return self
    
    def is_user_exists(self, username: str) -> bool:
        """检查用户是否存在"""
        self.search_by_username(username)
        return self.get_user_count() > 0
