variable "region" {
    type = string
    default = "us-east-1"
}

variable "profile"{
    type = string
    default = "default"
}

variable "instance_type" {
    type = string
    default = "t2.micro"
}

variable "ami_image" {
    type = string
    default = "ami-0996d3051b72b5b2c"
}

variable "key_name" {
    type = string
    default = "localkey"
}

variable "subnet_id" {
    default = "subnet-915144eb"
}

variable "key_path" {
    type = string
    default = "."
}

variable "aws_key_name" {
    type = string
    default = "chiave_aws"
}

variable "amz_key_path" {
    type = string
    default = "chiave_aws.pem"
}

variable "namenode_count" {
    type = number
    default = 1 
}

variable "datanode_count" {
    type = number
    default = 6 
}

variable "ips" {
    default = {
        "0" = "172.31.16.102"
        "1" = "172.31.16.103"
        "2" = "172.31.16.104"
        "3" = "172.31.16.105"
        "4" = "172.31.16.106"
        "5" = "172.31.16.107"
        "6" = "172.31.16.108"
        "7" = "172.31.16.109"
    }
}

variable "namenode_name" {
    type = string
    default = "s01"
}

variable "hostnames" {
    default = {
        "0" = "s02"
        "1" = "s03"
        "2" = "s04"
        "3" = "s05"
        "4" = "s06"
        "5" = "s07"
        "6" = "s08"
        "7" = "s09"
    }
}