// Jenkinsfile - 商城自动化测试CI/CD流水线

pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'mall-autotest'
        DOCKER_REGISTRY = 'registry.example.com'
        TEST_ENV = 'test'
    }
    
    options {
        timeout(time: 1, unit: 'HOURS')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    
    stages {
        stage('环境准备') {
            steps {
                echo '=== 准备测试环境 ==='
                sh 'python --version'
                sh 'pip list | grep pytest'
            }
        }
        
        stage('代码检出') {
            steps {
                echo '=== 检出代码 ==='
                checkout scm
            }
        }
        
        stage('安装依赖') {
            steps {
                echo '=== 安装Python依赖 ==='
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('单元测试') {
            steps {
                echo '=== 运行单元测试 ==='
                sh 'pytest test_cases/ -m api -v --tb=short'
            }
        }
        
        stage('冒烟测试') {
            steps {
                echo '=== 运行冒烟测试 ==='
                sh 'python run.py --env ${TEST_ENV} -m smoke --html-report'
            }
        }
        
        stage('API接口测试') {
            steps {
                echo '=== 运行API接口测试 ==='
                sh 'python run.py --env ${TEST_ENV} -m api --allure -n 4'
            }
        }
        
        stage('场景测试') {
            steps {
                echo '=== 运行场景测试 ==='
                sh 'python run.py --env ${TEST_ENV} -m scenario --html-report --reruns 2'
            }
        }
        
        stage('生成报告') {
            steps {
                echo '=== 生成Allure报告 ==='
                sh 'allure generate reports/allure -o reports/allure/report --clean'
                
                script {
                    // 归档测试报告
                    archiveArtifacts artifacts: 'reports/**/*.html,reports/**/*.xml', fingerprint: true
                }
            }
        }
        
        stage('部署到测试环境') {
            when {
                branch 'master'
            }
            steps {
                echo '=== 部署Docker镜像 ==='
                sh """
                    docker build -t ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER} .
                    docker push ${DOCKER_REGISTRY}/${DOCKER_IMAGE}:${BUILD_NUMBER}
                """
            }
        }
    }
    
    post {
        always {
            echo '=== 清理环境 ==='
            sh 'docker system prune -f'
        }
        
        success {
            echo '=== 测试成功 ==='
            emailext (
                subject: "✅ 商城自动化测试通过 - Build #${BUILD_NUMBER}",
                body: """
                    测试环境: ${TEST_ENV}
                    构建编号: ${BUILD_NUMBER}
                    测试结果: SUCCESS
                    报告地址: http://jenkins.example.com/job/mall-autotest/${BUILD_NUMBER}/allure/
                """,
                to: 'qa-team@example.com'
            )
        }
        
        failure {
            echo '=== 测试失败 ==='
            emailext (
                subject: "❌ 商城自动化测试失败 - Build #${BUILD_NUMBER}",
                body: """
                    测试环境: ${TEST_ENV}
                    构建编号: ${BUILD_NUMBER}
                    测试结果: FAILURE
                    报告地址: http://jenkins.example.com/job/mall-autotest/${BUILD_NUMBER}/allure/
                """,
                to: 'qa-team@example.com,dev-team@example.com'
            )
        }
    }
}
