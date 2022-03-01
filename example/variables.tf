variable "prefix" {
  description = "The prefix of resource."
  type        = string
}

variable "network" {
  description = ""
  type        = map(string)
}

variable "source_cidr_list" {
  description = ""
  type        = list(string)
}

variable "bastion" {
  description = ""
  type        = map(string)
}

variable "instances" {
  description = ""
  type        = map(map(string))
}
