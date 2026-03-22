"""
阿里云OSS报告上传模块
"""
import os
import json
import asyncio
import aiohttp
import oss2
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from config.config import Config
from common.logger import Logger


class OSSUploader:
    """阿里云OSS上传工具类"""
    
    def __init__(self):
        self.logger = Logger()
        self._init_config()
    
    def _init_config(self):
        """初始化OSS配置"""
        self.enabled = Config.get('oss.enabled', False)
        self.access_key_id = Config.get('oss.access_key_id', '')
        self.access_key_secret = Config.get('oss.access_key_secret', '')
        self.bucket_name = Config.get('oss.bucket_name', '')
        self.endpoint = Config.get('oss.endpoint', '')
        self.region = Config.get('oss.region', 'oss-cn-hangzhou')
        self.base_path = Config.get('oss.base_path', 'test-reports')
        
        if self.enabled and self.access_key_id:
            # 初始化OSS客户端
            auth = oss2.Auth(self.access_key_id, self.access_key_secret)
            self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
    
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        """
        上传单个文件到OSS
        
        Args:
            local_path: 本地文件路径
            remote_path: OSS远程路径
            
        Returns:
            是否成功
        """
        if not self.enabled:
            self.logger.warning("OSS上传未启用，跳过")
            return False
        
        try:
            # 确保remote_path不以/开头
            remote_path = remote_path.lstrip('/')
            
            result = self.bucket.put_object_from_file(remote_path, local_path)
            
            if result.status == 200:
                self.logger.info(f"文件上传成功: {local_path} -> oss://{self.bucket_name}/{remote_path}")
                return True
            else:
                self.logger.error(f"文件上传失败: {result.status}")
                return False
                
        except Exception as e:
            self.logger.error(f"OSS上传异常: {e}")
            return False
    
    def upload_directory(self, local_dir: str, remote_dir: str = None) -> Dict[str, bool]:
        """
        递归上传目录
        
        Args:
            local_dir: 本地目录
            remote_dir: OSS远程目录
            
        Returns:
            上传结果字典
        """
        results = {}
        
        if not self.enabled:
            self.logger.warning("OSS上传未启用，跳过")
            return results
        
        local_path = Path(local_dir)
        if not local_path.exists():
            self.logger.error(f"目录不存在: {local_dir}")
            return results
        
        remote_base = remote_dir or self.base_path
        
        for file_path in local_path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(local_path)
                remote_path = f"{remote_base}/{relative_path}"
                
                results[str(file_path)] = self.upload_file(str(file_path), remote_path)
        
        return results
    
    def get_file_url(self, remote_path: str, expires: int = 3600) -> Optional[str]:
        """
        获取文件访问URL
        
        Args:
            remote_path: OSS远程路径
            expires: 过期时间(秒)
            
        Returns:
            访问URL
        """
        if not self.enabled:
            return None
        
        try:
            remote_path = remote_path.lstrip('/')
            url = self.bucket.sign_url('GET', remote_path, expires)
            return url
        except Exception as e:
            self.logger.error(f"获取URL失败: {e}")
            return None


class ReportUploader:
    """测试报告上传管理器"""
    
    def __init__(self):
        self.logger = Logger()
        self.oss = OSSUploader()
        self._init_config()
    
    def _init_config(self):
        """初始化配置"""
        self.report_base_dir = Path(__file__).parent.parent / 'reports'
    
    def generate_report_name(self, trigger: str = 'manual', 
                            scenario: str = 'full', 
                            status: str = 'success') -> str:
        """
        生成报告文件名
        
        命名规则: 触发平台+场景+状态+时间戳
        
        Args:
            trigger: 触发平台 (github/jenkins/manual/api)
            scenario: 测试场景 (smoke/api/scenario/regression/full)
            status: 执行状态 (success/failure)
            
        Returns:
            报告文件名
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{trigger}_{scenario}_{status}_{timestamp}"
    
    def upload_html_report(self, report_path: str, 
                          trigger: str = 'manual',
                          scenario: str = 'full') -> Optional[str]:
        """
        上传HTML报告
        
        Args:
            report_path: 报告文件路径
            trigger: 触发平台
            scenario: 测试场景
            
        Returns:
            OSS访问URL，失败返回None
        """
        report_file = Path(report_path)
        
        if not report_file.exists():
            self.logger.error(f"报告文件不存在: {report_path}")
            return None
        
        # 判断执行状态
        # 简单通过文件名判断，实际可以从测试结果获取
        status = 'success' if 'success' in report_file.name else 'failure'
        
        # 生成远程路径
        report_name = self.generate_report_name(trigger, scenario, status)
        remote_path = f"{self.oss.base_path}/{report_name}.html"
        
        # 上传到OSS
        success = self.oss.upload_file(str(report_path), remote_path)
        
        if success:
            url = self.oss.get_file_url(remote_path)
            self.logger.info(f"报告已上传，访问URL: {url}")
            return url
        
        return None
    
    def upload_allure_report(self, allure_dir: str,
                            trigger: str = 'manual',
                            scenario: str = 'full') -> Dict[str, Any]:
        """
        上传Allure报告目录
        
        Args:
            allure_dir: Allure报告目录
            trigger: 触发平台
            scenario: 测试场景
            
        Returns:
            上传结果
        """
        status = 'success'  # Allure报告不区分状态
        report_name = self.generate_report_name(trigger, scenario, status)
        remote_dir = f"{self.oss.base_path}/{report_name}"
        
        self.logger.info(f"开始上传Allure报告: {allure_dir} -> {remote_dir}")
        
        results = self.oss.upload_directory(allure_dir, remote_dir)
        
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        result = {
            'success': success_count > 0,
            'total_files': total_count,
            'success_files': success_count,
            'failed_files': total_count - success_count,
            'report_url': f"https://{self.oss.bucket_name}.{self.oss.endpoint}/{remote_dir}/index.html"
        }
        
        self.logger.info(f"Allure报告上传完成: {result}")
        return result


# 异步上传（用于非阻塞上传）
class AsyncReportUploader(ReportUploader):
    """异步报告上传器"""
    
    async def upload_html_async(self, report_path: str,
                                trigger: str = 'manual',
                                scenario: str = 'full') -> Optional[str]:
        """异步上传HTML报告"""
        return await asyncio.to_thread(
            self.upload_html_report, report_path, trigger, scenario
        )
    
    async def upload_allure_async(self, allure_dir: str,
                                   trigger: str = 'manual',
                                   scenario: str = 'full') -> Dict[str, Any]:
        """异步上传Allure报告"""
        return await asyncio.to_thread(
            self.upload_allure_report, allure_dir, trigger, scenario
        )


# 全局实例
report_uploader = ReportUploader()
async_uploader = AsyncReportUploader()
