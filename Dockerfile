# 商城后台管理系统自动化测试 - Dockerfile

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置时区
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装Allure命令行工具
RUN wget -q https://github.com/allure-framework/allure2/releases/download/2.13.6/allure-2.13.6.tgz && \
    tar -xzf allure-2.13.6.tgz -C /opt/ && \
    ln -s /opt/allure-2.13.6/bin/allure /usr/local/bin/allure && \
    rm allure-2.13.6.tgz

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建必要的目录
RUN mkdir -p logs reports/html reports/allure reports/screenshots test_data

# 默认命令
CMD ["python", "run.py", "--env", "test", "-m", "regression", "--allure"]
