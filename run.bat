@echo off
REM ========================================
REM 商城自动化测试 - 快速执行脚本
REM ========================================

echo.
echo ========================================
echo   商城后台管理系统自动化测试
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo [1/3] 检查依赖包...
pip show pytest >nul 2>&1
if errorlevel 1 (
    echo [提示] 首次运行，正在安装依赖...
    pip install -r requirements.txt
)

REM 选择测试模式
echo.
echo 请选择测试模式:
echo   [1] 全量测试 (regression)
echo   [2] 冒烟测试 (smoke)
echo   [3] API接口测试 (api)
echo   [4] 场景测试 (scenario)
echo   [5] UI测试 (ui)
echo   [6] 自定义参数
echo.

set /p choice=请输入选项 (1-6): 

if "%choice%"=="1" goto full
if "%choice%"=="2" goto smoke
if "%choice%"=="3" goto api
if "%choice%"=="4" goto scenario
if "%choice%"=="5" goto ui
if "%choice%"=="6" goto custom
goto end

:full
echo [2/3] 运行全量测试...
python run.py --env test -m regression --allure --html-report -n 4
goto report

:smoke
echo [2/3] 运行冒烟测试...
python run.py --env test -m smoke --html-report
goto report

:api
echo [2/3] 运行API接口测试...
python run.py --env test -m api --allure -n 4
goto report

:scenario
echo [2/3] 运行场景测试...
python run.py --env test -m scenario --html-report
goto report

:ui
echo [2/3] 运行UI自动化测试...
python run.py --env test -m ui --browser chrome --headless
goto end

:custom
echo.
set /p custom_args=请输入自定义参数: 
python run.py %custom_args%
goto end

:report
echo [3/3] 生成测试报告...
echo.
echo 报告生成完成!
echo   - HTML报告: reports\html\
echo   - Allure报告: reports\allure\
echo.

set /p open_report=是否打开Allure报告? (Y/N): 
if /i "%open_report%"=="Y" (
    allure serve reports/allure
)

:end
echo.
echo ========================================
echo   测试执行完成
echo ========================================
echo.
pause
