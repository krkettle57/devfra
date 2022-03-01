output "vpc_id" {
  value = aws_vpc.vpc.id
}

output "pub_sbn_id" {
  value = aws_subnet.public.id
}

output "pri_sbn_id" {
  value = aws_subnet.private.id
}

output "bastion_eip" {
  value = aws_eip.bastion.public_ip
}
