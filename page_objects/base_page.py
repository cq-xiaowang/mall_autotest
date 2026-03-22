"""
基础页面对象类
封装Selenium WebDriver基本操作
"""
from typing import Any, List, Tuple
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from config.settings import Settings
from common.logger import Logger


class BasePage:
    """页面基类"""
    
    def __init__(self, driver: webdriver.Remote = None):
        """
        初始化页面对象
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.logger = Logger()
        self.timeout = Settings.get('UI_TIMEOUT', 10)
    
    def open(self, url: str):
        """打开页面"""
        self.driver.get(url)
        self.logger.info(f"打开页面: {url}")
    
    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """获取页面标题"""
        return self.driver.title
    
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        查找单个元素
        
        Args:
            locator: 定位器，格式为(By.ID, 'value')
            timeout: 超时时间
            
        Returns:
            WebElement
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        return element
    
    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """
        查找多个元素
        
        Args:
            locator: 定位器
            timeout: 超时时间
            
        Returns:
            WebElement列表
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        elements = wait.until(EC.presence_of_all_elements_located(locator))
        return elements
    
    def find_visible_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """查找可见元素"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def find_clickable_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """查找可点击元素"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def click(self, locator: Tuple[str, str]):
        """点击元素"""
        element = self.find_clickable_element(locator)
        element.click()
        self.logger.debug(f"点击元素: {locator}")
    
    def send_keys(self, locator: Tuple[str, str], text: str, clear: bool = True):
        """
        输入文本
        
        Args:
            locator: 定位器
            text: 输入文本
            clear: 是否先清空
        """
        element = self.find_visible_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)
        self.logger.debug(f"输入文本: {locator} = {text}")
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """获取元素文本"""
        element = self.find_visible_element(locator)
        return element.text
    
    def get_attribute(self, locator: Tuple[str, str], name: str) -> str:
        """获取元素属性"""
        element = self.find_element(locator)
        return element.get_attribute(name)
    
    def is_displayed(self, locator: Tuple[str, str]) -> bool:
        """元素是否可见"""
        try:
            element = self.find_visible_element(locator, timeout=5)
            return element.is_displayed()
        except Exception:
            return False
    
    def is_enabled(self, locator: Tuple[str, str]) -> bool:
        """元素是否可用"""
        try:
            element = self.find_element(locator)
            return element.is_enabled()
        except Exception:
            return False
    
    def is_selected(self, locator: Tuple[str, str]) -> bool:
        """元素是否选中"""
        try:
            element = self.find_element(locator)
            return element.is_selected()
        except Exception:
            return False
    
    def select_by_value(self, locator: Tuple[str, str], value: str):
        """
        下拉框选择（通过value）
        
        Args:
            locator: select元素定位器
            value: 选项value
        """
        from selenium.webdriver.support.select import Select
        element = self.find_element(locator)
        Select(element).select_by_value(value)
    
    def select_by_text(self, locator: Tuple[str, str], text: str):
        """
        下拉框选择（通过可见文本）
        
        Args:
            locator: select元素定位器
            text: 选项文本
        """
        from selenium.webdriver.support.select import Select
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text)
    
    def hover(self, locator: Tuple[str, str]):
        """鼠标悬停"""
        element = self.find_visible_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()
    
    def double_click(self, locator: Tuple[str, str]):
        """双击"""
        element = self.find_visible_element(locator)
        ActionChains(self.driver).double_click(element).perform()
    
    def right_click(self, locator: Tuple[str, str]):
        """右键点击"""
        element = self.find_visible_element(locator)
        ActionChains(self.driver).context_click(element).perform()
    
    def drag_and_drop(self, source: Tuple[str, str], target: Tuple[str, str]):
        """拖拽"""
        source_element = self.find_visible_element(source)
        target_element = self.find_visible_element(target)
        ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()
    
    def switch_to_frame(self, locator: Tuple[str, str] = None, index: int = None):
        """切换到iframe"""
        if locator:
            frame = self.find_element(locator)
            self.driver.switch_to.frame(frame)
        elif index is not None:
            self.driver.switch_to.frame(index)
        else:
            self.driver.switch_to.frame(0)
    
    def switch_to_default_content(self):
        """切换回主文档"""
        self.driver.switch_to.default_content()
    
    def switch_to_window(self, window_index: int = -1):
        """
        切换窗口
        
        Args:
            window_index: 窗口索引，-1表示最新打开的窗口
        """
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[window_index])
    
    def close_current_window(self):
        """关闭当前窗口"""
        self.driver.close()
    
    def accept_alert(self):
        """确认弹窗"""
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        alert.accept()
    
    def dismiss_alert(self):
        """取消弹窗"""
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        alert.dismiss()
    
    def get_alert_text(self) -> str:
        """获取弹窗文本"""
        alert = WebDriverWait(self.driver, self.timeout).until(EC.alert_is_present())
        return alert.text
    
    def execute_script(self, script: str, *args):
        """执行JavaScript"""
        return self.driver.execute_script(script, *args)
    
    def scroll_to_element(self, locator: Tuple[str, str]):
        """滚动到元素位置"""
        element = self.find_element(locator)
        self.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def scroll_to_top(self):
        """滚动到页面顶部"""
        self.execute_script("window.scrollTo(0, 0);")
    
    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    def take_screenshot(self, filename: str) -> str:
        """
        截图
        
        Args:
            filename: 文件名
            
        Returns:
            截图文件路径
        """
        screenshot_dir = Settings.SCREENSHOT_DIR
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        filepath = screenshot_dir / filename
        self.driver.save_screenshot(str(filepath))
        self.logger.info(f"截图保存: {filepath}")
        return str(filepath)
    
    def wait_for_page_load(self, timeout: int = None):
        """等待页面加载完成"""
        timeout = timeout or self.timeout
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    
    def refresh(self):
        """刷新页面"""
        self.driver.refresh()
    
    def back(self):
        """后退"""
        self.driver.back()
    
    def forward(self):
        """前进"""
        self.driver.forward()
