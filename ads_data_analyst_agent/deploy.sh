#!/bin/bash

# AI数据分析师演示应用 - AWS部署脚本
# 使用方法: ./deploy.sh [环境名称]

set -e

# 配置变量
PROJECT_NAME="ai-analyst-demo"
AWS_REGION="us-east-1"
ENVIRONMENT=${1:-production}

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查必要工具
check_prerequisites() {
    log_info "检查必要工具..."
    
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI 未安装，请先安装 AWS CLI"
        exit 1
    fi
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v terraform &> /dev/null; then
        log_error "Terraform 未安装，请先安装 Terraform"
        exit 1
    fi
    
    log_success "所有必要工具已安装"
}

# 检查AWS凭证
check_aws_credentials() {
    log_info "检查AWS凭证..."
    
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS凭证未配置，请运行 'aws configure'"
        exit 1
    fi
    
    log_success "AWS凭证验证成功"
}

# 构建和推送Docker镜像
build_and_push_image() {
    log_info "构建和推送Docker镜像..."
    
    # 获取ECR登录令牌
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com
    
    # 构建镜像
    log_info "构建Docker镜像..."
    docker build -t $PROJECT_NAME .
    
    # 获取ECR仓库URL
    ECR_REPOSITORY=$(aws ecr describe-repositories --repository-names $PROJECT_NAME --region $AWS_REGION --query 'repositories[0].repositoryUri' --output text 2>/dev/null || echo "")
    
    if [ -z "$ECR_REPOSITORY" ]; then
        log_info "创建ECR仓库..."
        aws ecr create-repository --repository-name $PROJECT_NAME --region $AWS_REGION
        ECR_REPOSITORY=$(aws ecr describe-repositories --repository-names $PROJECT_NAME --region $AWS_REGION --query 'repositories[0].repositoryUri' --output text)
    fi
    
    # 标记和推送镜像
    docker tag $PROJECT_NAME:latest $ECR_REPOSITORY:latest
    docker push $ECR_REPOSITORY:latest
    
    log_success "Docker镜像推送成功: $ECR_REPOSITORY:latest"
}

# 部署基础设施
deploy_infrastructure() {
    log_info "部署AWS基础设施..."
    
    cd terraform
    
    # 初始化Terraform
    terraform init
    
    # 规划部署
    terraform plan -var="environment=$ENVIRONMENT"
    
    # 确认部署
    read -p "是否继续部署基础设施? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        terraform apply -var="environment=$ENVIRONMENT" -auto-approve
        log_success "基础设施部署成功"
    else
        log_warning "部署已取消"
        exit 0
    fi
    
    cd ..
}

# 更新ECS服务
update_ecs_service() {
    log_info "更新ECS服务..."
    
    # 强制更新服务以使用新镜像
    aws ecs update-service \
        --cluster "${PROJECT_NAME}-cluster" \
        --service "${PROJECT_NAME}-service" \
        --force-new-deployment \
        --region $AWS_REGION
    
    log_success "ECS服务更新成功"
}

# 等待部署完成
wait_for_deployment() {
    log_info "等待部署完成..."
    
    aws ecs wait services-stable \
        --cluster "${PROJECT_NAME}-cluster" \
        --services "${PROJECT_NAME}-service" \
        --region $AWS_REGION
    
    log_success "部署完成"
}

# 获取应用URL
get_application_url() {
    log_info "获取应用访问URL..."
    
    ALB_DNS=$(aws elbv2 describe-load-balancers \
        --names "${PROJECT_NAME}-alb" \
        --region $AWS_REGION \
        --query 'LoadBalancers[0].DNSName' \
        --output text 2>/dev/null || echo "")
    
    if [ -n "$ALB_DNS" ]; then
        log_success "应用访问URL: http://$ALB_DNS"
        echo
        echo "🎉 部署成功！"
        echo "📱 应用URL: http://$ALB_DNS"
        echo "📊 CloudWatch日志: https://console.aws.amazon.com/cloudwatch/home?region=$AWS_REGION#logsV2:log-groups/log-group/%2Fecs%2F$PROJECT_NAME"
        echo "🔧 ECS服务: https://console.aws.amazon.com/ecs/home?region=$AWS_REGION#/clusters/${PROJECT_NAME}-cluster/services"
    else
        log_warning "无法获取应用URL，请检查AWS控制台"
    fi
}

# 清理资源 (可选)
cleanup() {
    log_warning "清理AWS资源..."
    
    read -p "确定要删除所有AWS资源吗? 这个操作不可逆! (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd terraform
        terraform destroy -var="environment=$ENVIRONMENT" -auto-approve
        cd ..
        
        # 删除ECR镜像
        aws ecr batch-delete-image \
            --repository-name $PROJECT_NAME \
            --image-ids imageTag=latest \
            --region $AWS_REGION 2>/dev/null || true
        
        log_success "资源清理完成"
    else
        log_info "清理已取消"
    fi
}

# 显示帮助信息
show_help() {
    echo "AI数据分析师演示应用 - AWS部署脚本"
    echo
    echo "使用方法:"
    echo "  $0 [选项] [环境名称]"
    echo
    echo "选项:"
    echo "  -h, --help     显示帮助信息"
    echo "  -c, --cleanup  清理AWS资源"
    echo "  -b, --build    仅构建和推送镜像"
    echo "  -d, --deploy   仅部署基础设施"
    echo
    echo "示例:"
    echo "  $0 production              # 完整部署到生产环境"
    echo "  $0 --build                 # 仅构建和推送镜像"
    echo "  $0 --cleanup               # 清理所有资源"
}

# 主函数
main() {
    echo "🚀 AI数据分析师演示应用 - AWS部署"
    echo "=================================="
    echo
    
    case "${1:-}" in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--cleanup)
            check_prerequisites
            check_aws_credentials
            cleanup
            exit 0
            ;;
        -b|--build)
            check_prerequisites
            check_aws_credentials
            build_and_push_image
            exit 0
            ;;
        -d|--deploy)
            check_prerequisites
            check_aws_credentials
            deploy_infrastructure
            exit 0
            ;;
        *)
            # 完整部署流程
            check_prerequisites
            check_aws_credentials
            build_and_push_image
            deploy_infrastructure
            update_ecs_service
            wait_for_deployment
            get_application_url
            ;;
    esac
}

# 执行主函数
main "$@"