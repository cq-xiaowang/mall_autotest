"""
商品管理页面UI自动化测试
"""
import pytest
import allure
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from config.config import Config
from test_data.product_data import ProductData
from common.logger import Logger


@allure.feature('商品管理')
@allure.story('商品页面UI测试')
class TestProductUI:
    """商品管理页面UI测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """测试前置"""
        self.driver = driver
        self.login_page = LoginPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.logger = Logger()
        
        # 登录
        self._login()
        yield
        
        self.logger.info("清理商品UI测试环境")
    
    def _login(self):
        """登录"""
        self.login_page.open_login_page()
        account = Config.get_test_account('admin')
        self.login_page.login(account['username'], account['password'])
    
    @allure.title('商品列表页面显示测试')
    @allure.severity('normal')
    @allure.testcase('TC-UI-010')
    def test_product_list_page_display(self):
        """测试商品列表页面元素显示"""
        # 打开商品列表页面
        self.product_page.open_product_list()
        
        # 验证页面元素
        assert self.product_page.is_displayed(ProductPage.SEARCH_BUTTON), "搜索按钮未显示"
        assert self.product_page.is_displayed(ProductPage.ADD_PRODUCT_BUTTON), "添加商品按钮未显示"
        assert self.product_page.is_displayed(ProductPage.PRODUCT_TABLE), "商品表格未显示"
    
    @allure.title('商品搜索功能测试')
    @allure.severity('critical')
    @allure.testcase('TC-UI-011')
    def test_product_search(self):
        """测试商品搜索功能"""
        self.product_page.open_product_list()
        
        # 执行搜索
        self.product_page.search_by_name('测试')
        
        # 等待搜索结果
        import time
        time.sleep(1)
        
        # 截图
        self.product_page.take_screenshot('product_search.png')
    
    @allure.title('添加商品页面显示测试')
    @allure.severity('normal')
    @allure.testcase('TC-UI-012')
    def test_add_product_page_display(self):
        """测试添加商品页面元素显示"""
        self.product_page.open_add_product_page()
        
        # 验证表单元素
        assert self.product_page.is_displayed(ProductPage.FORM_NAME_INPUT), "商品名称输入框未显示"
        assert self.product_page.is_displayed(ProductPage.FORM_PRICE_INPUT), "价格输入框未显示"
        assert self.product_page.is_displayed(ProductPage.SUBMIT_BUTTON), "提交按钮未显示"
    
    @allure.title('添加商品完整流程测试')
    @allure.severity('blocker')
    @allure.testcase('TC-UI-013')
    def test_add_product_flow(self):
        """测试添加商品完整流程"""
        self.product_page.open_add_product_page()
        
        # 填写商品信息
        product_data = ProductData.get_create_product_success_data()
        self.product_page.fill_product_form(product_data)
        
        # 截图
        self.product_page.take_screenshot('add_product_form.png')
        
        # 提交
        self.product_page.submit_product_form()
        
        # 等待跳转
        import time
        time.sleep(2)
        
        # 验证是否跳转到列表页
        current_url = self.product_page.get_current_url()
        assert 'list' in current_url or 'product' in current_url
    
    @allure.title('重置搜索条件测试')
    @allure.severity('minor')
    @allure.testcase('TC-UI-014')
    def test_reset_search(self):
        """测试重置搜索条件"""
        self.product_page.open_product_list()
        
        # 输入搜索条件
        self.product_page.send_keys(ProductPage.PRODUCT_NAME_INPUT, '测试')
        
        # 点击重置
        self.product_page.reset_search()
        
        # 验证输入框已清空
        value = self.product_page.get_attribute(ProductPage.PRODUCT_NAME_INPUT, 'value')
        assert value == '', f"重置后输入框未清空: {value}"
    
    @allure.title('商品列表分页测试')
    @allure.severity('normal')
    @allure.testcase('TC-UI-015')
    def test_product_list_pagination(self):
        """测试商品列表分页功能"""
        self.product_page.open_product_list()
        
        # 等待加载
        import time
        time.sleep(1)
        
        # 获取初始数量
        initial_count = self.product_page.get_product_count()
        
        # TODO: 点击下一页并验证
        
        self.product_page.take_screenshot('product_list_pagination.png')
