"""
HTTP请求处理模块
封装requests库，支持会话管理和请求重试
"""
import requests
from typing import Dict, Any, Optional, Union, Tuple
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import Config


class RequestHandler:
    """HTTP请求处理类"""
    
    def __init__(self, base_url: str = None, timeout: int = None):
        """
        初始化请求处理器
        
        Args:
            base_url: 基础URL，不传则从配置读取
            timeout: 超时时间
        """
        self.base_url = base_url or Config.get_base_url()
        self.timeout = timeout or Config.get_timeout('request')
        self.session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 默认请求头
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def set_header(self, key: str, value: str):
        """设置请求头"""
        self.headers[key] = value
    
    def set_auth_token(self, token: str):
        """设置认证Token"""
        self.headers['Authorization'] = f'Bearer {token}'
    
    def set_content_type(self, content_type: str):
        """设置Content-Type"""
        self.headers['Content-Type'] = content_type
    
    def _build_url(self, endpoint: str) -> str:
        """构建完整URL"""
        if endpoint.startswith('http'):
            return endpoint
        return f"{self.base_url}{endpoint}"
    
    def request(self, method: str, endpoint: str, 
                params: Dict = None, data: Dict = None, 
                json: Dict = None, headers: Dict = None,
                files: Dict = None, **kwargs) -> requests.Response:
        """
        发送HTTP请求
        
        Args:
            method: 请求方法
            endpoint: 接口路径
            params: URL参数
            data: 表单数据
            json: JSON数据
            headers: 请求头
            files: 上传文件
            **kwargs: 其他参数
            
        Returns:
            响应对象
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}
        
        response = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            data=data,
            json=json,
            headers=request_headers,
            timeout=self.timeout,
            files=files,
            **kwargs
        )
        
        return response
    
    def get(self, endpoint: str, params: Dict = None, 
            headers: Dict = None, **kwargs) -> requests.Response:
        """GET请求"""
        return self.request('GET', endpoint, params=params, headers=headers, **kwargs)
    
    def post(self, endpoint: str, data: Dict = None, 
             json: Dict = None, headers: Dict = None, 
             **kwargs) -> requests.Response:
        """POST请求"""
        return self.request('POST', endpoint, data=data, json=json, headers=headers, **kwargs)
    
    def put(self, endpoint: str, data: Dict = None, 
            json: Dict = None, headers: Dict = None, 
            **kwargs) -> requests.Response:
        """PUT请求"""
        return self.request('PUT', endpoint, data=data, json=json, headers=headers, **kwargs)
    
    def patch(self, endpoint: str, data: Dict = None, 
              json: Dict = None, headers: Dict = None, 
              **kwargs) -> requests.Response:
        """PATCH请求"""
        return self.request('PATCH', endpoint, data=data, json=json, headers=headers, **kwargs)
    
    def delete(self, endpoint: str, params: Dict = None, 
               headers: Dict = None, **kwargs) -> requests.Response:
        """DELETE请求"""
        return self.request('DELETE', endpoint, params=params, headers=headers, **kwargs)
    
    def upload_file(self, endpoint: str, file_path: str, 
                    file_field: str = 'file', data: Dict = None,
                    headers: Dict = None) -> requests.Response:
        """
        上传文件
        
        Args:
            endpoint: 接口路径
            file_path: 文件路径
            file_field: 文件字段名
            data: 其他表单数据
            headers: 请求头
            
        Returns:
            响应对象
        """
        with open(file_path, 'rb') as f:
            files = {file_field: f}
            # 上传文件时不设置Content-Type，让requests自动处理
            upload_headers = {k: v for k, v in self.headers.items() 
                            if k.lower() != 'content-type'}
            upload_headers.update(headers or {})
            return self.request('POST', endpoint, data=data, files=files, headers=upload_headers)
    
    def download_file(self, endpoint: str, save_path: str, 
                      params: Dict = None, **kwargs) -> str:
        """
        下载文件
        
        Args:
            endpoint: 接口路径
            save_path: 保存路径
            params: URL参数
            **kwargs: 其他参数
            
        Returns:
            保存的文件路径
        """
        response = self.get(endpoint, params=params, stream=True, **kwargs)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return save_path
    
    def close(self):
        """关闭会话"""
        self.session.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class APIResponse:
    """API响应封装类"""
    
    def __init__(self, response: requests.Response):
        self.response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self._json_data = None
    
    @property
    def json(self) -> Any:
        """获取JSON数据"""
        if self._json_data is None:
            try:
                self._json_data = self.response.json()
            except Exception:
                self._json_data = {}
        return self._json_data
    
    @property
    def text(self) -> str:
        """获取文本数据"""
        return self.response.text
    
    @property
    def content(self) -> bytes:
        """获取二进制数据"""
        return self.response.content
    
    def is_success(self) -> bool:
        """是否成功（2xx状态码）"""
        return 200 <= self.status_code < 300
    
    def get_code(self) -> int:
        """获取业务状态码"""
        return self.json.get('code', -1)
    
    def get_message(self) -> str:
        """获取业务消息"""
        return self.json.get('message', '')
    
    def get_data(self) -> Any:
        """获取业务数据"""
        return self.json.get('data')
