"""
多线程处理模块
支持并发执行测试任务
"""
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, List, Any, Dict
from queue import Queue


class ThreadHandler:
    """多线程处理类"""
    
    def __init__(self, max_workers: int = 4):
        """
        初始化线程处理器
        
        Args:
            max_workers: 最大线程数
        """
        self.max_workers = max_workers
        self._results: List[Any] = []
        self._errors: List[Exception] = []
        self._lock = threading.Lock()
    
    def run_task(self, func: Callable, *args, **kwargs) -> Any:
        """
        单线程执行任务
        
        Args:
            func: 任务函数
            args: 位置参数
            kwargs: 关键字参数
            
        Returns:
            任务结果
        """
        return func(*args, **kwargs)
    
    def run_tasks(self, tasks: List[Dict[str, Any]]) -> List[Any]:
        """
        并发执行多个任务
        
        Args:
            tasks: 任务列表，每个任务是一个字典，包含:
                   - func: 任务函数
                   - args: 位置参数（可选）
                   - kwargs: 关键字参数（可选）
                   
        Returns:
            结果列表
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for task in tasks:
                func = task.get('func')
                args = task.get('args', ())
                kwargs = task.get('kwargs', {})
                future = executor.submit(func, *args, **kwargs)
                futures.append(future)
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    with self._lock:
                        self._errors.append(e)
        
        return results
    
    def run_parallel(self, func: Callable, params_list: List[tuple]) -> List[Any]:
        """
        并发执行同一函数的多个参数组合
        
        Args:
            func: 任务函数
            params_list: 参数列表，每个元素是一个参数元组
            
        Returns:
            结果列表
        """
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(func, *params) for params in params_list]
            
            for future in as_completed(futures):
                try:
                    results.append(future.result())
                except Exception as e:
                    with self._lock:
                        self._errors.append(e)
        
        return results
    
    def get_errors(self) -> List[Exception]:
        """获取执行过程中的错误"""
        return self._errors
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self._errors) > 0


class AsyncTaskQueue:
    """异步任务队列"""
    
    def __init__(self, worker_count: int = 4):
        """
        初始化异步任务队列
        
        Args:
            worker_count: 工作线程数
        """
        self.queue = Queue()
        self.worker_count = worker_count
        self.workers = []
        self._stop_event = threading.Event()
    
    def add_task(self, func: Callable, *args, **kwargs):
        """
        添加任务到队列
        
        Args:
            func: 任务函数
            args: 位置参数
            kwargs: 关键字参数
        """
        self.queue.put((func, args, kwargs))
    
    def _worker(self):
        """工作线程"""
        while not self._stop_event.is_set():
            try:
                func, args, kwargs = self.queue.get(timeout=1)
                try:
                    func(*args, **kwargs)
                except Exception as e:
                    print(f"Task execution error: {e}")
                finally:
                    self.queue.task_done()
            except:
                continue
    
    def start(self):
        """启动任务队列"""
        for _ in range(self.worker_count):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def stop(self):
        """停止任务队列"""
        self._stop_event.set()
        for worker in self.workers:
            worker.join(timeout=5)
        self.workers = []
    
    def wait_completion(self):
        """等待所有任务完成"""
        self.queue.join()


class RateLimiter:
    """速率限制器"""
    
    def __init__(self, max_calls: int, period: float = 1.0):
        """
        初始化速率限制器
        
        Args:
            max_calls: 时间段内最大调用次数
            period: 时间段（秒）
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self._lock = threading.Lock()
    
    def __call__(self, func: Callable) -> Callable:
        """装饰器模式"""
        def wrapper(*args, **kwargs):
            with self._lock:
                self._wait_if_needed()
                self.calls.append(threading.current_thread().ident)
            return func(*args, **kwargs)
        return wrapper
    
    def _wait_if_needed(self):
        """如果需要则等待"""
        import time
        now = time.time()
        
        # 清理过期的调用记录
        self.calls = [c for c in self.calls if now - c < self.period]
        
        if len(self.calls) >= self.max_calls:
            time.sleep(self.period)
