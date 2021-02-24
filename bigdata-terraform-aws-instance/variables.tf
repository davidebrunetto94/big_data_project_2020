variable "region" {
    type = string
    default = "us-east-2" # Stati Uniti Orientali (Ohio)
}

variable "instance_type" {
    type = string
    default = "t2.micro" # free tier
}

variable "ami_image" {
    type = string
    default = "ami-0996d3051b72b5b2c" # ubuntu 20.04
}

variable "profile"{
    type = string
    default = "default"
}

variable "key_name" {
    type = string
    default = "localkey"
}

variable "nomeChiaveAws" {
    type = string
    default = "chiave_aws"
}

variable "nomeChiaveLocale" {
    type = string
    default = "localkey"
}

variable "pathChiaveAws" {
    type = string
    default = "chiave_aws.pem"
}

variable "numOfMasters" {
    type = number
    default = 1
}

variable "numOfSlaves" {
    type = number
    default = 1
}

variable "mgmt_jump_private_ips_master" {
    default = "172.31.16.101"
}

variable "subnetId" {
    default = "subnet-915144eb"
}

variable "mgmt_jump_private_ips" {
    default = {
        "0" = "172.31.16.102"
        "1" = "172.31.16.103"
        "2" = "172.31.16.104"
        "3" = "172.31.16.105"
        "4" = "172.31.16.106"
        "5" = "172.31.16.107"
    }
}

variable "mgmt_jump_hostnames" {
    default = {
        "0" = "slave_1"
        "1" = "slave_2"
        "2" = "slave_3"
        "3" = "slave_4"
        "4" = "slave_5"
        "5" = "slave_6"
    }
}