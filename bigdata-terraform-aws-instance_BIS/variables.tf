variable "region" {
    type = string
    default = "us-east-2"
}

variable "profile"{
    type = string
    default = "default"
}

variable "instance_type" {
    type = string
    default = "t2.micro"               # change instance type if needed
}

variable "ami_image" {
    type = string
    default = "ami-0996d3051b72b5b2c"   # ubuntu image
}

variable "key_name" {
    type = string
    default = "localkey"                # key name, see readme
}

variable "subnetId" {
    default = "subnet-915144eb"
}

variable "key_path" {
    type = string
    default = "."                       # change directory to local .ssh directory e.g. ~/.ssh/
}

variable "aws_key_name" {
    type = string
    default = "chiave_aws"                  # key name, see readme
}

variable "amz_key_path" {
    type = string
    default = "chiave_aws.pem"
}

variable "namenode_count" {
    type = number
    default = 1                         # count = 1 = 1 aws EC2
}

variable "datanode_count" {
    type = number
    default = 6                         # count = 3 = 3 aws EC2
}

variable "ips" {
    default = {
        "0" = "172.31.16.102"
        "1" = "172.31.16.103"
        "2" = "172.31.16.104"
        "3" = "172.31.16.105"
        "4" = "172.31.16.106"
        "5" = "172.31.16.107"
    }
}

variable "hostnames" {
    default = {
        "0" = "s02"
        "1" = "s03"
        "2" = "s04"
        "3" = "s05"
        "4" = "s06"
        "5" = "s07"
    }
}