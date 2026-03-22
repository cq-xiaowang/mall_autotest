"""
测试执行入口
支持多种执行方式和任务编排
"""
import os
import sys
import argparse
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))


def run_tests(args):
    """
    执行测试
    
    Args:
        args: 命令行参数
    """
    # 构建pytest命令
    pytest_cmd = ['pytest']
    
    # 测试路径
    if args.test_path:
        pytest_cmd.append(args.test_path)
    else:
        pytest_cmd.append('test_cases/')
    
    # 环境
    pytest_cmd.extend(['--env', args.env])
    
    # 浏览器（UI测试时使用）
    if args.browser:
        pytest_cmd.extend(['--browser', args.browser])
    
    # 无头模式
    if args.headless:
        pytest_cmd.append('--headless')
    
    # 标记
    if args.marker:
        pytest_cmd.extend(['-m', args.marker])
    
    # 并行执行
    if args.parallel:
        pytest_cmd.extend(['-n', str(args.parallel)])
    
    # 失败重试
    if args.retry:
        pytest_cmd.extend(['--reruns', str(args.retry)])
    
    # 详细输出
    if args.verbose:
        pytest_cmd.append('-v')
    
    # 调试模式
    if args.debug:
        pytest_cmd.extend(['-s', '--tb=long'])
    
    # 记录测试场景
    scenario = args.scenario or (args.marker if args.marker else 'full')
    
    # Allure报告
    if args.allure:
        allure_dir = BASE_DIR / 'reports' / 'allure'
        allure_dir.mkdir(parents=True, exist_ok=True)
        pytest_cmd.extend(['--alluredir', str(allure_dir)])
    
    # HTML报告
    if args.html_report:
        report_dir = BASE_DIR / 'reports' / 'html'
        report_dir.mkdir(parents=True, exist_ok=True)
        # 按命名规则生成报告文件名: 触发平台+场景+状态+时间
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = report_dir / f'{args.trigger}_{scenario}_{timestamp}.html'
        pytest_cmd.extend(['--html', str(report_file), '--self-contained-html'])
    
    # 打印执行命令
    print(f"执行命令: {' '.join(pytest_cmd)}")
    
    # 执行测试
    result = subprocess.run(pytest_cmd, cwd=str(BASE_DIR))
    
    return result.returncode, str(report_file) if args.html_report else None, scenario


def run_allure_report():
    """生成并打开Allure报告"""
    allure_dir = BASE_DIR / 'reports' / 'allure'
    
    if not allure_dir.exists():
        print("未找到Allure报告目录，请先运行测试")
        return
    
    # 生成报告
    subprocess.run(['allure', 'generate', str(allure_dir), '-o', str(allure_dir / 'report'), '--clean'])
    
    # 打开报告
    subprocess.run(['allure', 'open', str(allure_dir / 'report')])


def upload_report_async(report_path: str, trigger: str, scenario: str, exit_code: int):
    """
    异步上传报告到OSS和Nginx
    
    Args:
        report_path: 报告路径
        trigger: 触发平台
        scenario: 测试场景
        exit_code: 执行结果（0成功，非0失败）
    """
    # 延迟导入，避免启动时就检查OSS
    try:
        from common.oss_uploader import report_uploader
        from config.config import Config
        
        status = 'success' if exit_code == 0 else 'failure'
        
        # 上传到OSS
        if Config.get('oss.enabled', False):
            print(f"\n[上传] 开始上传报告到OSS...")
            url = report_uploader.upload_html_report(
                report_path, 
                trigger=trigger,
                scenario=scenario
            )
            if url:
                print(f"[上传] OSS访问地址: {url}")
        
        # 上传到Nginx服务器
        if Config.get('nginx.enabled', False):
            print(f"\n[上传] 开始上传报告到Nginx服务器...")
            upload_to_nginx(report_path, trigger, scenario, status)
            
    except Exception as e:
        print(f"[上传] 上传失败: {e}")


def upload_to_nginx(report_path: str, trigger: str, scenario: str, status: str):
    """
    上传报告到Nginx服务器（SSH方式）
    
    Args:
        report_path: 报告路径
        trigger: 触发平台
        scenario: 测试场景
        status: 执行状态
    """
    import paramiko
    from config.config import Config
    
    server_host = Config.get('nginx.host', '')
    server_port = Config.get('nginx.port', 22)
    server_user = Config.get('nginx.user', '')
    server_password = Config.get('nginx.password', '')
    server_path = Config.get('nginx.upload_path', '/var/www/html/reports')
    
    if not server_host or not server_user:
        print("[上传] Nginx服务器配置不完整，跳过上传")
        return
    
    try:
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_name = f"{trigger}_{scenario}_{status}_{timestamp}.html"
        
        # 连接服务器
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_host, port=server_port, username=server_user, password=server_password)
        
        # 上传文件
        sftp = ssh.open_sftp()
        remote_path = f"{server_path}/{report_name}"
        sftp.put(report_path, remote_path)
        
        print(f"[上传] Nginx访问地址: http://{server_host}/reports/{report_name}")
        
        sftp.close()
        ssh.close()
        
    except Exception as e:
        print(f"[上传] Nginx上传失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='商城后台管理系统自动化测试框架')
    
    # 基本参数
    parser.add_argument('--env', default='dev', choices=['dev', 'test', 'prod'],
                        help='测试环境 (default: dev)')
    parser.add_argument('--test-path', default=None,
                        help='测试路径或文件')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox', 'edge'],
                        help='浏览器类型 (default: chrome)')
    parser.add_argument('--headless', action='store_true',
                        help='无头模式运行')
    
    # 测试选项
    parser.add_argument('-m', '--marker', default=None,
                        help='执行指定标记的测试')
    parser.add_argument('-n', '--parallel', type=int, default=None,
                        help='并行执行数量')
    parser.add_argument('--reruns', dest='retry', type=int, default=0,
                        help='失败重试次数')
    
    # 输出选项
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='详细输出')
    parser.add_argument('--debug', action='store_true',
                        help='调试模式')
    
    # 报告选项
    parser.add_argument('--allure', action='store_true',
                        help='生成Allure报告')
    parser.add_argument('--html-report', action='store_true',
                        help='生成HTML报告')
    parser.add_argument('--open-allure', action='store_true',
                        help='打开Allure报告')
    
    # 上传选项
    parser.add_argument('--upload', action='store_true',
                        help='上传报告到OSS和Nginx')
    parser.add_argument('--trigger', default='manual',
                        choices=['manual', 'github', 'jenkins', 'api', 'schedule'],
                        help='触发平台 (default: manual)')
    parser.add_argument('--scenario', default=None,
                        help='测试场景名称，用于报告命名')
    
    args = parser.parse_args()
    
    # 打开Allure报告
    if args.open_allure:
        run_allure_report()
        return
    
    # 执行测试
    exit_code, report_path, scenario = run_tests(args)
    
    # 上传报告（异步，不阻塞测试结果）
    if args.upload and report_path:
        # 根据触发平台确定场景名
        trigger = args.trigger
        scenario = scenario or args.marker or 'full'
        
        # 异步上传
        upload_thread = threading.Thread(
            target=upload_report_async,
            args=(report_path, trigger, scenario, exit_code)
        )
        upload_thread.start()
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
