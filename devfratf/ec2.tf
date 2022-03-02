#------------------------------
# Key Pair
#------------------------------
resource "aws_key_pair" "bastion" {
  key_name   = "${var.prefix}-bastion"
  public_key = file(var.bastion.public_keypath)
}

resource "aws_key_pair" "devserver" {
  for_each   = var.instances
  key_name   = "${var.prefix}-${each.key}"
  public_key = file(each.value.public_keypath)
}

#------------------------------
# EC2 Instance
#------------------------------
resource "aws_instance" "bastion" {
  ami           = var.bastion.ami_id
  subnet_id     = aws_subnet.public.id
  key_name      = aws_key_pair.bastion.key_name
  instance_type = var.bastion.instance_type
  user_data     = var.bastion.user_data
  vpc_security_group_ids = [
    aws_security_group.bastion.id
  ]
  associate_public_ip_address = true

  tags = {
    Name = "${var.prefix}-bastion"
  }
}

resource "null_resource" "bastion_cmd" {
  for_each = var.instances
  triggers = {
    instance = aws_instance.bastion.id
  }
  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = "ec2-user"
      host        = aws_eip.bastion.public_ip
      private_key = file(var.bastion.private_keypath)
    }
    inline = [
      "sudo adduser ${each.key}",
      "sudo mkdir -p /home/${each.key}/.ssh",
      "sudo chown -R ${each.key}:${each.key} /home/${each.key}/.ssh",
      "sudo bash -c 'echo ${file(each.value.public_keypath)} >> /home/${each.key}/.ssh/authorized_keys'"
    ]
  }
}

resource "aws_instance" "devserver" {
  for_each      = var.instances
  ami           = each.value.ami_id
  subnet_id     = aws_subnet.private.id
  key_name      = aws_key_pair.devserver[each.key].key_name
  instance_type = each.value.instance_type
  vpc_security_group_ids = [
    aws_security_group.devserver.id
  ]
  private_ip = each.value.private_ip
  user_data  = each.value.user_data

  tags = {
    Name = "${var.prefix}-${each.key}"
  }
}

#------------------------------
# Security Group
#------------------------------
resource "aws_security_group" "bastion" {
  name        = "${var.prefix}-bastion"
  description = "ssh for bastion"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = var.source_cidr_list
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "devserver" {
  name        = "${var.prefix}-devserver"
  description = "ssh for devserver"
  vpc_id      = aws_vpc.vpc.id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    security_groups = [
      aws_security_group.bastion.id
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

#------------------------------
# EIP
#------------------------------
resource "aws_eip" "bastion" {
  vpc      = true
  instance = aws_instance.bastion.id
  depends_on = [
    aws_instance.bastion
  ]
}
