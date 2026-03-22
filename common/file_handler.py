"""
文件处理模块
支持多种格式文件的读取和写入
"""
import json
import yaml
import csv
import os
from pathlib import Path
from typing import Any, Dict, List, Union


class FileHandler:
    """文件操作处理类"""
    
    @staticmethod
    def read_file(file_path: str, encoding: str = 'utf-8') -> str:
        """
        读取文本文件
        
        Args:
            file_path: 文件路径
            encoding: 编码格式
            
        Returns:
            文件内容字符串
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    
    @staticmethod
    def write_file(file_path: str, content: str, encoding: str = 'utf-8'):
        """
        写入文本文件
        
        Args:
            file_path: 文件路径
            content: 文件内容
            encoding: 编码格式
        """
        # 确保目录存在
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
    
    @staticmethod
    def read_json(file_path: str, encoding: str = 'utf-8') -> Union[Dict, List]:
        """
        读取JSON文件
        
        Args:
            file_path: 文件路径
            encoding: 编码格式
            
        Returns:
            JSON数据
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return json.load(f)
    
    @staticmethod
    def write_json(file_path: str, data: Union[Dict, List], 
                   encoding: str = 'utf-8', indent: int = 2):
        """
        写入JSON文件
        
        Args:
            file_path: 文件路径
            data: JSON数据
            encoding: 编码格式
            indent: 缩进空格数
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
    
    @staticmethod
    def read_yaml(file_path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
        """
        读取YAML文件
        
        Args:
            file_path: 文件路径
            encoding: 编码格式
            
        Returns:
            YAML数据
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return yaml.safe_load(f) or {}
    
    @staticmethod
    def write_yaml(file_path: str, data: Dict[str, Any], encoding: str = 'utf-8'):
        """
        写入YAML文件
        
        Args:
            file_path: 文件路径
            data: YAML数据
            encoding: 编码格式
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding=encoding) as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
    
    @staticmethod
    def read_csv(file_path: str, encoding: str = 'utf-8', 
                 has_header: bool = True) -> List[Dict[str, Any]]:
        """
        读取CSV文件
        
        Args:
            file_path: 文件路径
            encoding: 编码格式
            has_header: 是否有表头
            
        Returns:
            CSV数据列表
        """
        result = []
        with open(file_path, 'r', encoding=encoding, newline='') as f:
            if has_header:
                reader = csv.DictReader(f)
                result = [row for row in reader]
            else:
                reader = csv.reader(f)
                result = [row for row in reader]
        return result
    
    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, Any]], 
                  fieldnames: List[str] = None, encoding: str = 'utf-8'):
        """
        写入CSV文件
        
        Args:
            file_path: 文件路径
            data: 数据列表
            fieldnames: 字段名列表
            encoding: 编码格式
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding=encoding, newline='') as f:
            if data:
                fieldnames = fieldnames or list(data[0].keys())
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
    
    @staticmethod
    def append_file(file_path: str, content: str, encoding: str = 'utf-8'):
        """
        追加写入文件
        
        Args:
            file_path: 文件路径
            content: 追加内容
            encoding: 编码格式
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'a', encoding=encoding) as f:
            f.write(content)
    
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """检查文件是否存在"""
        return Path(file_path).exists()
    
    @staticmethod
    def delete_file(file_path: str) -> bool:
        """删除文件"""
        try:
            Path(file_path).unlink()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """获取文件大小（字节）"""
        return Path(file_path).stat().st_size
    
    @staticmethod
    def list_files(directory: str, pattern: str = '*') -> List[str]:
        """
        列出目录下的文件
        
        Args:
            directory: 目录路径
            pattern: 文件匹配模式
            
        Returns:
            文件路径列表
        """
        path = Path(directory)
        return [str(f) for f in path.glob(pattern) if f.is_file()]
