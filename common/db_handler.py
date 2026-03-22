"""
数据库连接处理模块
支持MySQL数据库操作
"""
import pymysql
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager
from pymysql.cursors import DictCursor
from config.config import Config


class DBHandler:
    """数据库操作处理类"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化数据库连接
        
        Args:
            config: 数据库配置，不传则从配置文件读取
        """
        self.config = config or Config.get_database_config()
        self.connection = None
    
    def connect(self):
        """建立数据库连接"""
        if self.connection is None or not self.connection.open:
            self.connection = pymysql.connect(
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 3306),
                user=self.config.get('user', 'root'),
                password=self.config.get('password', ''),
                database=self.config.get('database', ''),
                charset=self.config.get('charset', 'utf8mb4'),
                cursorclass=DictCursor
            )
        return self.connection
    
    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()
            self.connection = None
    
    @contextmanager
    def get_cursor(self, cursor_class=DictCursor):
        """获取游标的上下文管理器"""
        conn = self.connect()
        cursor = conn.cursor(cursor_class)
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def execute(self, sql: str, params: Tuple = None) -> int:
        """
        执行单条SQL语句
        
        Args:
            sql: SQL语句
            params: 参数元组
            
        Returns:
            影响的行数
        """
        with self.get_cursor() as cursor:
            affected_rows = cursor.execute(sql, params)
            return affected_rows
    
    def execute_many(self, sql: str, params_list: List[Tuple]) -> int:
        """
        批量执行SQL语句
        
        Args:
            sql: SQL语句
            params_list: 参数列表
            
        Returns:
            影响的行数
        """
        with self.get_cursor() as cursor:
            affected_rows = cursor.executemany(sql, params_list)
            return affected_rows
    
    def query_one(self, sql: str, params: Tuple = None) -> Optional[Dict[str, Any]]:
        """
        查询单条记录
        
        Args:
            sql: SQL语句
            params: 参数元组
            
        Returns:
            单条记录字典
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def query_all(self, sql: str, params: Tuple = None) -> List[Dict[str, Any]]:
        """
        查询所有记录
        
        Args:
            sql: SQL语句
            params: 参数元组
            
        Returns:
            记录列表
        """
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def query_page(self, sql: str, page: int = 1, page_size: int = 10, 
                   params: Tuple = None) -> Dict[str, Any]:
        """
        分页查询
        
        Args:
            sql: SQL语句
            page: 页码
            page_size: 每页数量
            params: 参数元组
            
        Returns:
            分页结果字典
        """
        offset = (page - 1) * page_size
        
        # 查询总数
        count_sql = f"SELECT COUNT(*) as total FROM ({sql}) as t"
        total = self.query_one(count_sql, params)['total']
        
        # 查询数据
        page_sql = f"{sql} LIMIT {offset}, {page_size}"
        data = self.query_all(page_sql, params)
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
            "data": data
        }
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """
        插入数据
        
        Args:
            table: 表名
            data: 数据字典
            
        Returns:
            插入的主键ID
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        with self.get_cursor() as cursor:
            cursor.execute(sql, tuple(data.values()))
            return cursor.lastrowid
    
    def update(self, table: str, data: Dict[str, Any], where: str, 
               where_params: Tuple = None) -> int:
        """
        更新数据
        
        Args:
            table: 表名
            data: 更新数据字典
            where: WHERE条件
            where_params: WHERE参数
            
        Returns:
            影响的行数
        """
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        params = tuple(data.values()) + (where_params or ())
        return self.execute(sql, params)
    
    def delete(self, table: str, where: str, where_params: Tuple = None) -> int:
        """
        删除数据
        
        Args:
            table: 表名
            where: WHERE条件
            where_params: WHERE参数
            
        Returns:
            影响的行数
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        return self.execute(sql, where_params)
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在"""
        sql = "SELECT COUNT(*) as cnt FROM information_schema.tables WHERE table_schema = %s AND table_name = %s"
        result = self.query_one(sql, (self.config.get('database'), table_name))
        return result['cnt'] > 0


# 数据库连接池（简单实现）
class DBPool:
    """数据库连接池"""
    
    _pool: List[DBHandler] = []
    _max_size = 10
    
    @classmethod
    def get_connection(cls) -> DBHandler:
        """获取连接"""
        if cls._pool:
            return cls._pool.pop()
        return DBHandler()
    
    @classmethod
    def return_connection(cls, conn: DBHandler):
        """归还连接"""
        if len(cls._pool) < cls._max_size:
            cls._pool.append(conn)
        else:
            conn.close()
