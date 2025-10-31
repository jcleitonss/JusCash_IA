# Upload ZIP para S3
resource "aws_s3_object" "lambda_zip" {
  bucket = aws_s3_bucket.flows.id
  key    = "lambda/juscrash-agent-core.zip"
  source = "${path.module}/../agent-core/lambda-package.zip"
  etag   = filemd5("${path.module}/../agent-core/lambda-package.zip")
}

# Lambda Function (ZIP via S3)
resource "aws_lambda_function" "agent_core" {
  function_name = "${var.project_name}-agent-core"
  role          = aws_iam_role.lambda.arn
  
  s3_bucket        = aws_s3_bucket.flows.id
  s3_key           = aws_s3_object.lambda_zip.key
  source_code_hash = filebase64sha256("${path.module}/../agent-core/lambda-package.zip")
  
  runtime = "python3.11"
  handler = "src.handler.handler"
  
  timeout     = 60
  memory_size = 1024
  
  environment {
    variables = {
      FLOWS_BUCKET            = aws_s3_bucket.flows.id
      AWS_BEDROCK_REGION      = var.aws_region
      BEDROCK_AGENT_ID        = try(aws_bedrockagent_agent.juscrash_agent.agent_id, "")
      BEDROCK_AGENT_ALIAS_ID  = try(aws_bedrockagent_agent_alias.production.agent_alias_id, "TSTALIASID")
      LANGSMITH_API_KEY       = var.langsmith_api_key
      LANGSMITH_PROJECT       = var.langsmith_project
      LANGSMITH_ENDPOINT      = "https://api.smith.langchain.com"
      LANGCHAIN_TRACING_V2    = var.langchain_tracing_enabled
    }
  }
}

# IAM Role para Lambda
resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach basic execution role
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Custom policy para S3, Bedrock e Bedrock Agent
resource "aws_iam_role_policy" "lambda_custom" {
  name = "${var.project_name}-lambda-policy"
  role = aws_iam_role.lambda.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.flows.arn,
          "${aws_s3_bucket.flows.arn}/*"
        ]
      },
      {
        Effect   = "Allow"
        Action   = "bedrock:InvokeModel"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeAgent",
          "bedrock:GetAgent",
          "bedrock:ListAgents"
        ]
        Resource = "*"
      }
    ]
  })
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.project_name}-agent-core"
  retention_in_days = 7
}
