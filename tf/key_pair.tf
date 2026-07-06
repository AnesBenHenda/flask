resource "aws_key_pair" "admin" {
  key_name   = "${var.project_name}-key"
  public_key = var.ssh_public_key
}
