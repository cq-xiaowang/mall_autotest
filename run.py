"""
测试执行入口
支持多种执行方式和任务编排
"""
import os
import sys
import argparse
import subprocess
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
    
    # Allure报告
    if args.allure:
        allure_dir = BASE_DIR / 'reports' / 'allure'
        allure_dir.mkdir(parents=True, exist_ok=True)
        pytest_cmd.extend(['--alluredir', str(allure_dir)])
    
    # HTML报告
    if args.html_report:
        report_dir = BASE_DIR / 'reports' / 'html'
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
        pytest_cmd.extend(['--html', str(report_file), '--self-contained-html'])
    
    # 打印执行命令
    print(f"执行命令: {' '.join(pytest_cmd)}")
    
    # 执行测试
    result = subprocess.run(pytest_cmd, cwd=str(BASE_DIR))
    
    return result.returncode


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


def upload_report_to_server(report_path: str):
    """
    上传测试报告到服务器
    
    Args:
        report_path: 报告文件路径
    """
    import paramiko
    from config.config import Config
    
    # 获取服务器配置（可以添加到配置文件）
    server_host = Config.get('report_server.host', 'your-server.com')
    server_port = Config.get('report_server.port', 22)
    server_user = Config.get('report_server.user', 'user')
    server_password = Config.get('report_server.password', 'password')
    server_path = Config.get('report_server.path', '/var/www/html/reports/')
    
    try:
        # 连接服务器
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_host, port=server_port, username=server_user, password=server_password)
        
        # 上传文件
        sftp = ssh.open_sftp()
        report_name = Path(report_path).name
        remote_path = f"{server_path}{report_name}"
        sftp.put(report_path, remote_path)
        
        print(f"报告已上传: {remote_path}")
        
        sftp.close()
        ssh.close()
        
    except Exception as e:
        print(f"上传报告失败: {e}")


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
    
    # 其他选项
    parser.add_argument('--upload', action='store_true',
                        help='上传报告到服务器')
    
    args = parser.parse_args()
    
    # 打开Allure报告
    if args.open_allure:
        run_allure_report()
        return
    
    # 执行测试
    exit_code = run_tests(args)
    
    # 上传报告
    if args.upload and args.html_report:
        # 找到最新的HTML报告
        report_dir = BASE_DIR / 'reports' / 'html'
        reports = sorted(report_dir.glob('report_*.html'), reverse=True)
        if reports:
            upload_report_to_server(str(reports[0]))
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
