"""
页面对象模块（UI自动化）
"""
from page_objects.base_page import BasePage
from page_objects.login_page import LoginPage
from page_objects.product_page import ProductPage
from page_objects.user_page import UserPage

__all__ = ['BasePage', 'LoginPage', 'ProductPage', 'UserPage']
