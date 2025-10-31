output "frontend_url" {
  description = "CloudFront URL do frontend"
  value       = "https://${aws_cloudfront_distribution.frontend.domain_name}"
}

output "api_url" {
  description = "API Gateway URL"
  value       = aws_apigatewayv2_stage.prod.invoke_url
}

output "lambda_function_name" {
  description = "Lambda Function Name"
  value       = aws_lambda_function.agent_core.function_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront Distribution ID"
  value       = aws_cloudfront_distribution.frontend.id
}
