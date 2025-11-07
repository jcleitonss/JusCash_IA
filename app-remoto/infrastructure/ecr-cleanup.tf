# Remover ECR (temporário - será deletado após apply)
resource "aws_ecr_repository" "agent_core" {
  name                 = "${var.project_name}-agent-core"
  image_tag_mutability = "MUTABLE"
  force_delete         = true
  
  image_scanning_configuration {
    scan_on_push = true
  }
  
  lifecycle {
    ignore_changes = all
  }
}
