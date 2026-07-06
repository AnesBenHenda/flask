output "instance_public_ip" {
  description = "Public IP of the EC2 instance (use for SSH; app traffic goes via ALB)"
  value       = aws_instance.kind_host.public_ip
}

output "cluster_name" {
  value = local.cluster_name
}

output "instance_id" {
  value = aws_instance.kind_host.id
}

output "alb_dns_name" {
  description = "Raw ALB DNS name (used internally by the Route 53 alias)"
  value       = aws_lb.main.dns_name
}

output "app_url" {
  description = "Public HTTPS URL for the application"
  value       = "https://${var.domain_name}"
}

output "acm_certificate_arn" {
  description = "ARN of the ACM TLS certificate"
  value       = aws_acm_certificate.main.arn
}
