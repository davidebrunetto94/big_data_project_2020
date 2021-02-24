terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.28"
    }
  }
}

provider "aws" {
    region  = var.region
    profile = var.profile
}

resource "aws_security_group" "webnode" {
    name = "webnode"
    description = "Web Security Group"
        ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    lifecycle {
        create_before_destroy = true
    }
}


resource "aws_instance" "master1" {
    ami             = var.ami_image
    instance_type   = var.instance_type
    key_name        = var.nomeChiaveAws
    tags = {
        Name = "master_1"
    }
    
    subnet_id = "subnet-915144eb"

    vpc_security_group_ids = [aws_security_group.webnode.id]

    private_ip      = var.mgmt_jump_private_ips_master

    provisioner "file" {
        source      = "install.sh"
        destination = "/tmp/install.sh"

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.pathChiaveAws)
        }
    }

    provisioner "local-exec" {
        command = "cat ./${var.nomeChiaveLocale}.pub | ssh -o StrictHostKeyChecking=no -i ${var.pathChiaveAws}  ubuntu@${self.public_dns} 'cat >> .ssh/authorized_keys'"
    }
    provisioner "local-exec" {
        command = "cat ./${var.nomeChiaveLocale}.pub | ssh -o StrictHostKeyChecking=no -i ${var.pathChiaveAws}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa.pub'"
    }
    provisioner "local-exec" {
        command = "cat ./${var.nomeChiaveLocale} | ssh -o StrictHostKeyChecking=no -i ${var.pathChiaveAws}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa'"
    }

    # execute the configuration script
    provisioner "remote-exec" {
        inline = [
            "chmod +x /tmp/install.sh",
            "/bin/bash /tmp/install.sh",
            "/opt/hadoop-2.7.7/bin/hadoop namenode -format"
        ]
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.pathChiaveAws)
        }

    }
}


resource "aws_instance" "slave1" {
    count           = var.numOfSlaves
    ami             = var.ami_image
    instance_type   = var.instance_type
    key_name        = var.nomeChiaveAws
    tags = {
        Name = lookup(var.mgmt_jump_hostnames, count.index)
    }

    subnet_id = "subnet-915144eb"
    
    vpc_security_group_ids = [aws_security_group.webnode.id]

    private_ip = lookup(var.mgmt_jump_private_ips, count.index)

    provisioner "file" {
        source      = "install.sh"
        destination = "/tmp/install.sh"

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.pathChiaveAws)
        }
    }

    provisioner "local-exec" {
        command = "cat ./${var.nomeChiaveLocale}.pub | ssh -o StrictHostKeyChecking=no -i ${var.pathChiaveAws}  ubuntu@${self.public_dns} 'cat >> .ssh/authorized_keys'"
    }
    provisioner "local-exec" {
        command = "cat ./${var.nomeChiaveLocale}.pub | ssh -o StrictHostKeyChecking=no -i ${var.pathChiaveAws}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa.pub'"
    }
    provisioner "local-exec" {
        command = "cat ./${var.nomeChiaveLocale} | ssh -o StrictHostKeyChecking=no -i ${var.pathChiaveAws}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa'"
    }

    provisioner "remote-exec" {
        inline = [
            "chmod +x /tmp/install.sh",
            "/bin/bash /tmp/install.sh",
        ]
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.pathChiaveAws)
        }

    }
}



output "Master_dns_address" {
    value = aws_instance.master1.*.public_dns
}

output "Slave_dns_address" {
    value = aws_instance.slave1.*.public_dns
}