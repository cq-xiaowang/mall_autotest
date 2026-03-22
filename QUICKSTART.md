# 快速开始指南

## 一、本地运行

### 方式1：Windows 一键运行
```bash
# 双击运行 run.bat，按提示选择
run.bat
```

### 方式2：命令行运行
```bash
# 安装依赖
pip install -r requirements.txt

# 全量测试
python run.py --env test -m regression --allure --html-report

# 只运行API测试
python run.py --env test -m api -n 4

# 只运行冒烟测试
python run.py --env test -m smoke
```

---

## 二、Docker 部署

### 方式1：Docker Compose（推荐）

```bash
# 启动所有服务（测试+数据库+Redis+Nginx）
docker-compose up -d

# 查看日志
docker-compose logs -f autotest

# 停止服务
docker-compose down
```

### 方式2：单独运行测试容器

```bash
# 构建镜像
docker build -t mall-autotest .

# 运行测试
docker run -it --rm \
  -e TEST_ENV=test \
  -v $(pwd)/reports:/app/reports \
  mall-autotest
```

---

## 三、CI/CD 集成

### Jenkins
直接使用项目中的 `Jenkinsfile`

### GitHub Actions
推送到GitHub后自动触发 `.github/workflows/autotest.yml`

---

## 四、常用命令汇总

| 场景 | 命令 |
|------|------|
| 全量回归测试 | `python run.py --env test -m regression --allure --html-report -n 4` |
| 冒烟测试 | `python run.py --env test -m smoke --html-report` |
| 仅API接口 | `python run.py --env test -m api --allure` |
| 仅UI测试 | `python run.py --env test -m ui --headless` |
| 场景测试 | `python run.py --env test -m scenario --html-report` |
| 排除UI测试 | `python run.py --env test -m "not ui"` |
| 失败重试 | `python run.py --env test -m api --reruns 2` |
| 生成Allure | `python run.py --env test --allure && allure open reports/allure` |

---

## 五、报告查看

### HTML报告
直接浏览器打开 `reports/html/report_*.html`

### Allure报告
```bash
# 生成报告
allure generate reports/allure -o reports/allure/report

# 打开报告
allure open reports/allure/report
```

### Docker + Nginx
启动后访问 `http://localhost:8080`
