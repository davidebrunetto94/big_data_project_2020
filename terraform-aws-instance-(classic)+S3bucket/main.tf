locals {
    #  Directories start with "C:..." on Windows; All other OSs use "/" for root.
    is_windows = substr(pathexpand("~"), 0, 1) == "/" ? false : true
}


provider "aws" {
    region  = var.region
    profile = var.profile
}


resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF

  tags = {
      tag-key = "tag-value"
  }
}


resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2_profile"
  role = "${aws_iam_role.ec2_role.name}"
}

resource "aws_iam_role_policy" "s3_policy" {
  name = "s3_policy"
  role = "${aws_iam_role.ec2_role.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
EOF
}




resource "aws_security_group" "Hadoop_cluster_sc" {
    name = "Hadoop_cluster_sc"

    # inbound internet access
    ingress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # outbound internet access
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


# namenode (master)
resource "aws_instance" "Namenode" {
    count = var.namenode_count
    ami = var.ami_image
    instance_type = var.instance_type
    key_name = var.aws_key_name
    tags = {
        Name = var.namenode_name
    }
    private_ip = var.namenode_ip
    vpc_security_group_ids = [aws_security_group.Hadoop_cluster_sc.id]
    subnet_id = var.subnet_id
    iam_instance_profile = "${aws_iam_instance_profile.ec2_profile.name}"

    provisioner "file" {
        source      = "install-all.sh"
        destination = "/tmp/install-all.sh"

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    provisioner "file" {
        source      = "app/"
        destination = "/home/ubuntu/"
    
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/authorized_keys'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa.pub'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name} | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa'"
    }

    # execute the configuration script
    provisioner "remote-exec" {
        inline = [
            "chmod +x /tmp/install-all.sh",
            "/bin/bash /tmp/install-all.sh",
            "/opt/hadoop-2.7.7/bin/hadoop namenode -format"
        ]
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }

    }
}


# datanode (slaves)
resource "aws_instance" "Datanode" {
    subnet_id = var.subnet_id
    count = var.datanode_count
    ami = var.ami_image
    instance_type = var.instance_type
    key_name = var.aws_key_name
    tags = {
        Name = lookup(var.hostnames, count.index)
    }
    private_ip = lookup(var.ips, count.index)
    vpc_security_group_ids = [aws_security_group.Hadoop_cluster_sc.id]
    iam_instance_profile = "${aws_iam_instance_profile.ec2_profile.name}"

    # copy the initialization script to the remote machines
    provisioner "file" {
        source      = "install-all.sh"
        destination = "/tmp/install-all.sh"

        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }
    }

    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/authorized_keys'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name}.pub | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa.pub'"
    }
    provisioner "local-exec" {
        interpreter = local.is_windows ? ["PowerShell"] : []
        command = "cat ${var.key_path}/${var.key_name} | ssh -o StrictHostKeyChecking=no -i ${var.amz_key_path}  ubuntu@${self.public_dns} 'cat >> .ssh/id_rsa'"
    }

    # execute the configuration script
    provisioner "remote-exec" {
        inline = [
            "chmod +x /tmp/install-all.sh",
            "/bin/bash /tmp/install-all.sh",
        ]
        connection {
            host     = self.public_dns
            type     = "ssh"
            user     = "ubuntu"
            private_key = file(var.amz_key_path)
        }

    }
}