# 🚀 AWS部署指南 - AI数据分析师演示应用

## 📋 部署方案概述

基于当前应用的特点，我推荐以下几种AWS部署方案，按复杂度和成本排序：

## 🎯 推荐方案

### 方案1: Amazon ECS + Fargate (推荐) ⭐⭐⭐⭐⭐

**适用场景**: 生产环境，需要高可用性和自动扩缩容

**架构组件**:
- **ECS Fargate**: 无服务器容器运行
- **Application Load Balancer**: 负载均衡和SSL终止
- **CloudFront**: CDN加速
- **Route 53**: 域名解析
- **ECR**: 容器镜像仓库
- **CloudWatch**: 监控和日志

**优势**:
- ✅ 无需管理服务器
- ✅ 自动扩缩容
- ✅ 高可用性
- ✅ 成本可控
- ✅ 易于维护

**预估成本**: $30-100/月

### 方案2: AWS App Runner (最简单) ⭐⭐⭐⭐

**适用场景**: 快速部署，简单应用

**架构组件**:
- **App Runner**: 全托管容器服务
- **CloudFront**: CDN加速(可选)

**优势**:
- ✅ 部署最简单
- ✅ 自动CI/CD
- ✅ 自动扩缩容
- ✅ 内置负载均衡

**预估成本**: $25-80/月

### 方案3: Amazon EC2 + Docker (传统) ⭐⭐⭐

**适用场景**: 需要更多控制权，成本敏感

**架构组件**:
- **EC2实例**: t3.medium或t3.large
- **Application Load Balancer**: 负载均衡
- **Auto Scaling Group**: 自动扩缩容
- **CloudWatch**: 监控

**优势**:
- ✅ 完全控制
- ✅ 成本可预测
- ✅ 灵活配置

**预估成本**: $50-150/月

## 🏗️ 详细部署方案 (推荐ECS Fargate)

### 1. 容器化准备

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 启动命令
CMD ["streamlit", "run", "demo_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

#### docker-compose.yml (本地测试)
```yaml
version: '3.8'
services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - AWS_DEFAULT_REGION=us-east-1
    volumes:
      - ./google.campaign_daily_geo_stats.csv:/app/google.campaign_daily_geo_stats.csv
```

### 2. AWS基础设施 (Terraform)

#### main.tf
```hcl
# VPC和网络
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "ai-analyst-vpc"
  }
}

# 公有子网
resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  map_public_ip_on_launch = true

  tags = {
    Name = "ai-analyst-public-${count.index + 1}"
  }
}

# ECS集群
resource "aws_ecs_cluster" "main" {
  name = "ai-analyst-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ECS任务定义
resource "aws_ecs_task_definition" "app" {
  family                   = "ai-analyst-app"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 1024
  memory                   = 2048
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn           = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name  = "ai-analyst"
      image = "${aws_ecr_repository.app.repository_url}:latest"
      
      portMappings = [
        {
          containerPort = 8501
          protocol      = "tcp"
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.app.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }

      environment = [
        {
          name  = "AWS_DEFAULT_REGION"
          value = var.aws_region
        }
      ]
    }
  ])
}

# ECS服务
resource "aws_ecs_service" "main" {
  name            = "ai-analyst-service"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    security_groups  = [aws_security_group.ecs_tasks.id]
    subnets          = aws_subnet.public[*].id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "ai-analyst"
    container_port   = 8501
  }

  depends_on = [aws_lb_listener.app]
}

# Application Load Balancer
resource "aws_lb" "main" {
  name               = "ai-analyst-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.lb.id]
  subnets            = aws_subnet.public[*].id

  enable_deletion_protection = false
}

# CloudFront分发
resource "aws_cloudfront_distribution" "main" {
  origin {
    domain_name = aws_lb.main.dns_name
    origin_id   = "ALB-${aws_lb.main.name}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  enabled = true
  comment = "AI Data Analyst Demo Distribution"

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "ALB-${aws_lb.main.name}"
    compress               = true
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = true
      headers      = ["*"]
      cookies {
        forward = "all"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}
```

### 3. CI/CD管道 (GitHub Actions)

#### .github/workflows/deploy.yml
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: ai-analyst-demo

jobs:
  deploy:
    name: Deploy
    runs-on: ubuntu-latest

    steps:
    - name: Checkout
      uses: actions/checkout@v3

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1

    - name: Build, tag, and push image to Amazon ECR
      id: build-image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        cd ads_data_analyst_agent
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

    - name: Deploy to Amazon ECS
      uses: aws-actions/amazon-ecs-deploy-task-definition@v1
      with:
        task-definition: task-definition.json
        service: ai-analyst-service
        cluster: ai-analyst-cluster
        wait-for-service-stability: true
```

## 🔧 部署步骤

### 第一阶段: 本地准备
1. **创建Dockerfile和相关配置文件**
2. **本地测试容器化应用**
3. **准备Terraform配置**

### 第二阶段: AWS基础设施
1. **创建ECR仓库**
2. **部署VPC和网络组件**
3. **创建ECS集群和服务**
4. **配置负载均衡器**

### 第三阶段: CI/CD设置
1. **配置GitHub Actions**
2. **设置AWS凭证**
3. **测试自动部署**

### 第四阶段: 优化和监控
1. **配置CloudWatch监控**
2. **设置告警**
3. **性能优化**

## 💰 成本估算

### ECS Fargate方案 (推荐)
- **Fargate计算**: ~$35/月 (2个任务，1vCPU/2GB)
- **Application Load Balancer**: ~$22/月
- **CloudFront**: ~$1-5/月 (取决于流量)
- **ECR存储**: ~$1/月
- **CloudWatch日志**: ~$5/月
- **数据传输**: ~$5-15/月

**总计**: ~$70-85/月

### 成本优化建议
- 使用Spot实例 (EC2方案)
- 配置自动扩缩容
- 优化镜像大小
- 使用CloudFront缓存

## 🔒 安全考虑

### 网络安全
- VPC隔离
- 安全组配置
- WAF保护 (可选)

### 应用安全
- 容器镜像扫描
- 最小权限原则
- 敏感数据加密

### 访问控制
- IAM角色和策略
- API密钥管理
- 日志审计

## 📊 监控和运维

### 监控指标
- CPU/内存使用率
- 请求响应时间
- 错误率
- 用户访问量

### 日志管理
- 应用日志
- 访问日志
- 错误日志
- 性能日志

### 告警设置
- 高CPU使用率
- 内存不足
- 服务不可用
- 异常错误率

## 🚀 快速开始

想要立即开始部署吗？我可以帮你：

1. **创建所有必要的配置文件**
2. **设置Terraform基础设施代码**
3. **配置CI/CD管道**
4. **提供详细的部署脚本**