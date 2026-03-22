"""
商品大盘统计相关API单接口测试
"""
import pytest
import allure
from common.request_handler import RequestHandler, APIResponse
from common.logger import Logger


@allure.feature('统计分析')
@allure.story('统计接口')
class TestStatisticsAPI:
    """统计分析相关API测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试前置"""
        self.request = RequestHandler()
        self.logger = Logger()
        yield
        self.request.close()
    
    @allure.title('获取商品销量统计')
    @allure.severity('blocker')
    @allure.testcase('TC-STAT-001')
    def test_get_product_sales_statistics(self):
        """测试获取商品销量统计"""
        query_data = {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'top_n': 10
        }
        
        response = self.request.get('/statistics/product/sales', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
        assert 'list' in api_response.get_data()
    
    @allure.title('获取商品浏览量统计')
    @allure.severity('normal')
    @allure.testcase('TC-STAT-002')
    def test_get_product_view_statistics(self):
        """测试获取商品浏览量统计"""
        query_data = {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31',
            'top_n': 10
        }
        
        response = self.request.get('/statistics/product/views', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('获取类目销量分布')
    @allure.severity('normal')
    @allure.testcase('TC-STAT-003')
    def test_get_category_sales_distribution(self):
        """测试获取类目销量分布"""
        query_data = {
            'start_date': '2024-01-01',
            'end_date': '2024-12-31'
        }
        
        response = self.request.get('/statistics/category/distribution', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('获取库存预警统计')
    @allure.severity('critical')
    @allure.testcase('TC-STAT-004')
    def test_get_stock_warning_statistics(self):
        """测试获取库存预警统计"""
        query_data = {
            'low_stock_threshold': 10
        }
        
        response = self.request.get('/statistics/stock/warning', params=query_data)
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
    
    @allure.title('获取大盘概览数据')
    @allure.severity('blocker')
    @allure.testcase('TC-STAT-005')
    def test_get_overview_statistics(self):
        """测试获取大盘概览数据"""
        response = self.request.get('/statistics/overview')
        api_response = APIResponse(response)
        
        assert response.status_code == 200
        assert api_response.is_success()
        # 验证返回的数据结构
        data = api_response.get_data()
        assert 'total_products' in data
        assert 'total_categories' in data
        assert 'total_orders' in data
