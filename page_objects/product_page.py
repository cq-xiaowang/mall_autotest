"""
商品管理页面对象
"""
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from config.config import Config


class ProductPage(BasePage):
    """商品管理页面"""
    
    # 页面URL
    PRODUCT_LIST_URL = '/product/list'
    PRODUCT_ADD_URL = '/product/add'
    
    # 商品列表页元素
    PRODUCT_NAME_INPUT = (By.ID, 'product-name')
    PRODUCT_CODE_INPUT = (By.ID, 'product-code')
    SEARCH_BUTTON = (By.ID, 'btn-search')
    RESET_BUTTON = (By.ID, 'btn-reset')
    ADD_PRODUCT_BUTTON = (By.ID, 'btn-add-product')
    PRODUCT_TABLE = (By.ID, 'product-table')
    PRODUCT_ROW = (By.CLASS_NAME, 'product-row')
    
    # 商品表单元素
    PRODUCT_FORM = (By.ID, 'product-form')
    FORM_NAME_INPUT = (By.ID, 'form-name')
    FORM_CODE_INPUT = (By.ID, 'form-code')
    FORM_CATEGORY_SELECT = (By.ID, 'form-category')
    FORM_BRAND_SELECT = (By.ID, 'form-brand')
    FORM_PRICE_INPUT = (By.ID, 'form-price')
    FORM_ORIGINAL_PRICE_INPUT = (By.ID, 'form-original-price')
    FORM_STOCK_INPUT = (By.ID, 'form-stock')
    FORM_STATUS_SELECT = (By.ID, 'form-status')
    FORM_BRIEF_INPUT = (By.ID, 'form-brief')
    FORM_DESCRIPTION_INPUT = (By.ID, 'form-description')
    SUBMIT_BUTTON = (By.ID, 'btn-submit')
    CANCEL_BUTTON = (By.ID, 'btn-cancel')
    
    # 操作按钮
    EDIT_BUTTON = (By.CLASS_NAME, 'btn-edit')
    DELETE_BUTTON = (By.CLASS_NAME, 'btn-delete')
    STATUS_BUTTON = (By.CLASS_NAME, 'btn-status')
    VIEW_BUTTON = (By.CLASS_NAME, 'btn-view')
    
    # 确认弹窗
    CONFIRM_DIALOG = (By.CLASS_NAME, 'confirm-dialog')
    CONFIRM_YES_BUTTON = (By.CLASS_NAME, 'btn-confirm-yes')
    CONFIRM_NO_BUTTON = (By.CLASS_NAME, 'btn-confirm-no')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_product_list(self):
        """打开商品列表页面"""
        url = Config.get_full_url(self.PRODUCT_LIST_URL)
        self.open(url)
        return self
    
    def open_add_product_page(self):
        """打开添加商品页面"""
        url = Config.get_full_url(self.PRODUCT_ADD_URL)
        self.open(url)
        return self
    
    def search_by_name(self, product_name: str):
        """按商品名称搜索"""
        self.send_keys(self.PRODUCT_NAME_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)
        return self
    
    def search_by_code(self, product_code: str):
        """按商品编码搜索"""
        self.send_keys(self.PRODUCT_CODE_INPUT, product_code)
        self.click(self.SEARCH_BUTTON)
        return self
    
    def reset_search(self):
        """重置搜索条件"""
        self.click(self.RESET_BUTTON)
        return self
    
    def click_add_product(self):
        """点击添加商品按钮"""
        self.click(self.ADD_PRODUCT_BUTTON)
        return self
    
    def fill_product_form(self, product_data: dict):
        """
        填写商品表单
        
        Args:
            product_data: 商品数据字典
        """
        if 'product_name' in product_data:
            self.send_keys(self.FORM_NAME_INPUT, product_data['product_name'])
        if 'product_code' in product_data:
            self.send_keys(self.FORM_CODE_INPUT, product_data['product_code'])
        if 'category_id' in product_data:
            self.select_by_value(self.FORM_CATEGORY_SELECT, str(product_data['category_id']))
        if 'brand_id' in product_data:
            self.select_by_value(self.FORM_BRAND_SELECT, str(product_data['brand_id']))
        if 'price' in product_data:
            self.send_keys(self.FORM_PRICE_INPUT, str(product_data['price']))
        if 'original_price' in product_data:
            self.send_keys(self.FORM_ORIGINAL_PRICE_INPUT, str(product_data['original_price']))
        if 'stock' in product_data:
            self.send_keys(self.FORM_STOCK_INPUT, str(product_data['stock']))
        if 'status' in product_data:
            self.select_by_value(self.FORM_STATUS_SELECT, str(product_data['status']))
        if 'brief' in product_data:
            self.send_keys(self.FORM_BRIEF_INPUT, product_data['brief'])
        if 'description' in product_data:
            self.send_keys(self.FORM_DESCRIPTION_INPUT, product_data['description'])
        
        return self
    
    def submit_product_form(self):
        """提交商品表单"""
        self.click(self.SUBMIT_BUTTON)
        return self
    
    def cancel_product_form(self):
        """取消商品表单"""
        self.click(self.CANCEL_BUTTON)
        return self
    
    def get_product_count(self) -> int:
        """获取商品列表数量"""
        rows = self.find_elements(self.PRODUCT_ROW)
        return len(rows)
    
    def edit_product(self, product_id: int):
        """编辑商品"""
        # 根据product_id定位编辑按钮并点击
        edit_btn = (By.XPATH, f"//tr[@data-id='{product_id}']//button[contains(@class, 'btn-edit')]")
        self.click(edit_btn)
        return self
    
    def delete_product(self, product_id: int, confirm: bool = True):
        """
        删除商品
        
        Args:
            product_id: 商品ID
            confirm: 是否确认删除
        """
        # 点击删除按钮
        delete_btn = (By.XPATH, f"//tr[@data-id='{product_id}']//button[contains(@class, 'btn-delete')]")
        self.click(delete_btn)
        
        # 处理确认弹窗
        if confirm:
            self.click(self.CONFIRM_YES_BUTTON)
        else:
            self.click(self.CONFIRM_NO_BUTTON)
        
        return self
    
    def toggle_product_status(self, product_id: int):
        """切换商品上下架状态"""
        status_btn = (By.XPATH, f"//tr[@data-id='{product_id}']//button[contains(@class, 'btn-status')]")
        self.click(status_btn)
        return self
    
    def is_product_exists(self, product_name: str) -> bool:
        """检查商品是否存在"""
        self.search_by_name(product_name)
        return self.get_product_count() > 0
    
    def get_product_info(self, product_id: int) -> dict:
        """获取商品信息"""
        row = (By.XPATH, f"//tr[@data-id='{product_id}']")
        # 这里简化处理，实际需要根据页面结构解析
        return {
            'name': self.get_text((By.XPATH, f"//tr[@data-id='{product_id}']/td[1]")),
            'price': self.get_text((By.XPATH, f"//tr[@data-id='{product_id}']/td[2]")),
            'stock': self.get_text((By.XPATH, f"//tr[@data-id='{product_id}']/td[3]")),
        }
