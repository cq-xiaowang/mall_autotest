"""
pytest配置文件
定义全局fixtures和钩子函数
"""
import pytest
import os
import allure
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config.config import Config
from config.settings import Settings
from common.logger import Logger
from common.request_handler import RequestHandler


# ===================== 命令行参数 =====================
def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption(
        '--env', 
        action='store', 
        default='dev',
        help='测试环境: dev, test, prod'
    )
    parser.addoption(
        '--browser',
        action='store',
        default='chrome',
        help='浏览器类型: chrome, firefox, edge'
    )
    parser.addoption(
        '--headless',
        action='store_true',
        help='是否无头模式运行'
    )
    parser.addoption(
        '--report',
        action='store',
        default='html',
        help='报告类型: html, allure'
    )


# ===================== 环境配置 =====================
@pytest.fixture(scope='session', autouse=True)
def set_environment(request):
    """设置测试环境"""
    env = request.config.getoption('--env')
    os.environ['TEST_ENV'] = env
    
    # 重新加载配置
    Config.reload_config(env)
    
    logger = Logger()
    logger.info(f"{'='*60}")
    logger.info(f"测试环境: {env}")
    logger.info(f"测试开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*60}")
    
    yield
    
    logger.info(f"测试结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


# ===================== WebDriver Fixture =====================
@pytest.fixture(scope='function')
def driver(request):
    """
    WebDriver fixture
    每个测试函数一个driver实例
    """
    browser = request.config.getoption('--browser')
    headless = request.config.getoption('--headless')
    
    driver_instance = None
    
    if browser.lower() == 'chrome':
        options = Options()
        
        if headless:
            options.add_argument('--headless')
        
        # 常用配置
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        
        # 禁用自动化检测
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver_instance = webdriver.Chrome(options=options)
        
    elif browser.lower() == 'firefox':
        from selenium.webdriver.firefox.options import Options as FirefoxOptions
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        driver_instance = webdriver.Firefox(options=options)
        
    elif browser.lower() == 'edge':
        from selenium.webdriver.edge.options import Options as EdgeOptions
        options = EdgeOptions()
        if headless:
            options.add_argument('--headless')
        driver_instance = webdriver.Edge(options=options)
    
    else:
        raise ValueError(f"不支持的浏览器类型: {browser}")
    
    # 设置隐式等待
    driver_instance.implicitly_wait(10)
    
    # 最大化窗口
    driver_instance.maximize_window()
    
    yield driver_instance
    
    # 清理
    try:
        driver_instance.quit()
    except Exception:
        pass


# ===================== 登录Token Fixture =====================
@pytest.fixture(scope='session')
def admin_token():
    """获取管理员登录token"""
    with RequestHandler() as request:
        account = Config.get_test_account('admin')
        response = request.post('/user/login', json=account)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            return data.get('token')
    return None


# ===================== 数据库Fixture =====================
@pytest.fixture(scope='function')
def db():
    """数据库连接fixture"""
    from common.db_handler import DBHandler
    
    db_handler = DBHandler()
    yield db_handler
    db_handler.close()


# ===================== 测试数据清理Fixture =====================
@pytest.fixture(scope='function')
def cleanup_products():
    """商品数据清理fixture"""
    product_ids = []
    
    yield product_ids
    
    # 清理数据
    if product_ids:
        logger = Logger()
        logger.info(f"清理测试商品数据: {product_ids}")
        with RequestHandler() as request:
            for product_id in product_ids:
                try:
                    request.delete(f'/product/{product_id}')
                except Exception:
                    pass


@pytest.fixture(scope='function')
def cleanup_users():
    """用户数据清理fixture"""
    user_ids = []
    
    yield user_ids
    
    if user_ids:
        logger = Logger()
        logger.info(f"清理测试用户数据: {user_ids}")
        with RequestHandler() as request:
            for user_id in user_ids:
                try:
                    request.delete(f'/user/{user_id}')
                except Exception:
                    pass


# ===================== 测试报告相关 =====================
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    生成测试报告的钩子
    用于在测试失败时截图
    """
    outcome = yield
    report = outcome.get_result()
    
    # 只在测试失败时处理
    if report.when == 'call' and report.failed:
        # 尝试截图
        if 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            try:
                screenshot_name = f"failed_{item.name}_{datetime.now().strftime('%H%M%S')}.png"
                screenshot_path = Settings.SCREENSHOT_DIR / screenshot_name
                driver.save_screenshot(str(screenshot_path))
                
                # 添加到allure报告
                allure.attach.file(
                    str(screenshot_path),
                    name='失败截图',
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                Logger().error(f"截图失败: {e}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """测试结束后的统计"""
    logger = Logger()
    
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    error = len(terminalreporter.stats.get('error', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    
    logger.info(f"测试统计: 通过={passed}, 失败={failed}, 错误={error}, 跳过={skipped}")
