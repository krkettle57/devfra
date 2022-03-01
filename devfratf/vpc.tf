resource "aws_vpc" "vpc" {
  cidr_block = var.network.vpc_cidr
}

#------------------------------
# Subnet
#------------------------------
resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = var.network.public_subnet_cidr
  depends_on = [aws_internet_gateway.igw]
}

resource "aws_subnet" "private" {
  vpc_id     = aws_vpc.vpc.id
  cidr_block = var.network.private_subnet_cidr
  depends_on = [aws_internet_gateway.igw]
}

#------------------------------
# RouteTable
#------------------------------
resource "aws_route_table" "public_sbn_rt" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_sbn_rt.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.natgw.id
  }
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

#------------------------------
# Gateway
#------------------------------
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_nat_gateway" "natgw" {
  allocation_id = aws_eip.natgw_ip.id
  subnet_id     = aws_subnet.public.id
  depends_on    = [aws_internet_gateway.igw]
}

resource "aws_eip" "natgw_ip" {
  vpc        = true
  depends_on = [aws_internet_gateway.igw]
}
