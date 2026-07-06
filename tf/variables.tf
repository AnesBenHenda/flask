variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Used to prefix/tag all resources"
  type        = string
  default     = "inter"
}

variable "instance_type" {
  description = "t3.medium (2 vCPU / 4GB)."
  type        = string
  default     = "t3.medium"
}

variable "root_volume_size_gb" {
  description = "Docker images + kind nodes + monitoring stack add up fast"
  type        = number
  default     = 30
}

variable "ssh_public_key" {
  description = "public key contents, output of: cat ~/.ssh/id_rsa.pub"
  type        = string
}

variable "admin_cidr" {
  description = "IP in CIDR form, e.g. 203.0.113.5/32 — run `curl -s ifconfig.me` to find it."
  type        = string
}


variable "domain_name" {
  description = "Full subdomain for the app, e.g. myapp.example.com"
  type        = string
  default     = "myapp.example.com"
}

variable "hosted_zone_name" {
  description = "Apex domain of the Route 53 public hosted zone, e.g. example.com"
  type        = string
  default     = "example.com"
}
