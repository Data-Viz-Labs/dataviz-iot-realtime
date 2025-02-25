provider "aws" {
  region = var.aws_region
}

# Obtener la AMI de Amazon Linux 2 más reciente
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Crear un par de claves SSH
resource "aws_key_pair" "lab_key" {
  key_name   = "lab-key"
  public_key = tls_private_key.lab_key.public_key_openssh
}

# Generar una clave privada
resource "tls_private_key" "lab_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Guardar la clave privada localmente
resource "local_file" "private_key" {
  content         = tls_private_key.lab_key.private_key_pem
  filename        = "${path.module}/lab-key.pem"
  file_permission = "0400"
}

# Crear una VPC
resource "aws_vpc" "lab_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "lab-vpc"
  }
}

# Crear una subred pública
resource "aws_subnet" "lab_subnet" {
  vpc_id                  = aws_vpc.lab_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "${var.aws_region}a"

  tags = {
    Name = "lab-subnet"
  }
}

# Crear un Internet Gateway
resource "aws_internet_gateway" "lab_igw" {
  vpc_id = aws_vpc.lab_vpc.id

  tags = {
    Name = "lab-igw"
  }
}

# Crear una tabla de rutas
resource "aws_route_table" "lab_route_table" {
  vpc_id = aws_vpc.lab_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab_igw.id
  }

  tags = {
    Name = "lab-route-table"
  }
}

# Asociar la tabla de rutas con la subred
resource "aws_route_table_association" "lab_route_assoc" {
  subnet_id      = aws_subnet.lab_subnet.id
  route_table_id = aws_route_table.lab_route_table.id
}

# Crear un grupo de seguridad
resource "aws_security_group" "lab_sg" {
  name        = "lab-security-group"
  description = "Allow SSH access from specific IP"
  vpc_id      = aws_vpc.lab_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ip]
    description = "SSH access from allowed IP"
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.allowed_ip]
    description = "All traffic from allowed IP"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "lab-security-group"
  }
}

# Crear instancias EC2
resource "aws_instance" "lab_instances" {
  count         = var.instance_count
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "m5.medium"
  key_name      = aws_key_pair.lab_key.key_name
  subnet_id     = aws_subnet.lab_subnet.id

  vpc_security_group_ids = [aws_security_group.lab_sg.id]

  tags = {
    Name = "lab-instance-${count.index + 1}"
  }
}

# Variables
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "instance_count" {
  description = "Number of EC2 instances to create (max 20)"
  type        = number
  default     = 1

  validation {
    condition     = var.instance_count > 0 && var.instance_count <= 20
    error_message = "Instance count must be between 1 and 20."
  }
}

variable "allowed_ip" {
  description = "IP address allowed to connect to instances"
  type        = string
  default     = "83.32.191.143/32"
}

# Outputs
output "instance_ips" {
  description = "Public IPs of the created instances"
  value       = aws_instance.lab_instances[*].public_ip
}

output "ssh_key_path" {
  description = "Path to the SSH private key"
  value       = local_file.private_key.filename
}

output "ssh_commands" {
  description = "SSH commands to connect to instances"
  value = [
    for i in range(length(aws_instance.lab_instances)) :
    "ssh -i ${local_file.private_key.filename} ec2-user@${aws_instance.lab_instances[i].public_ip}"
  ]
}
