variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "juscrash"
}

variable "langsmith_api_key" {
  description = "LangSmith API Key para observabilidade"
  type        = string
  default     = ""
  sensitive   = true
}

variable "langsmith_project" {
  description = "LangSmith Project Name"
  type        = string
  default     = "juscrash-prod"
}

variable "langchain_tracing_enabled" {
  description = "Habilitar tracing LangSmith"
  type        = string
  default     = "true"
}
