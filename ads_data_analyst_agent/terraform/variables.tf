# 基本配置
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "ai-analyst-demo"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

# ECR配置
variable "ecr_repository_name" {
  description = "Name of the ECR repository"
  type        = string
  default     = "ai-analyst-demo"
}

# ECS配置
variable "fargate_cpu" {
  description = "Fargate instance CPU units to provision (1 vCPU = 1024 CPU units)"
  type        = number
  default     = 1024
}

variable "fargate_memory" {
  description = "Fargate instance memory to provision (in MiB)"
  type        = number
  default     = 2048
}

variable "app_count" {
  description = "Number of docker containers to run"
  type        = number
  default     = 2
}

variable "container_name" {
  description = "Name of the container"
  type        = string
  default     = "ai-analyst"
}

# 域名配置 (可选)
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = ""
}

variable "certificate_arn" {
  description = "ARN of the SSL certificate"
  type        = string
  default     = ""
}

# 标签
variable "tags" {
  description = "A map of tags to assign to the resource"
  type        = map(string)
  default = {
    Project     = "AI Data Analyst Demo"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}