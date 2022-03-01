module "devfra" {
  source           = "../devfratf"
  prefix           = var.prefix
  bastion          = var.bastion
  source_cidr_list = var.source_cidr_list
  network          = var.network
  instances        = var.instances
}
