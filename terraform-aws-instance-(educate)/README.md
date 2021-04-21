# AWS - Terraform support

Introduction: this guide is based on the script we created and tested on an AWSfree-tier account.
With some minor modifications, the script can also be used on an AWS educate account.


1. [Package contents](#Package-contents)
2. [AWS CLI Installation](#AWS-CLI-Installation)
3. [Terraform Installation](#Terraform-Installation)
4. [Script Preparation](#Script-Preparation)
5. [Script Executing](#Script-Executing)
6. [Environment destruction](#Environment-destruction)


## Package contents
It is important to download the entire GitHub project and maintain the directory structure. The terraform script will automatically load the application contained in the ```proj``` folder inside the master node in the ```/home/ubuntu``` directory.
* main.tf: terraform script that creates the environment on your AWS account
* variables.tf: contains the configuration parameters for the script
* install-all.sh: script that installs and configures your nodes with necessary software
* other files...


## AWS CLI Installation
Installing the AWS CLI is a prerequisite for using Terraform with AWS.
Download and install AWS CLI v2 for your computer (https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).

If you are using AWS Educate, you need to modify ```access_key```, ```secret_key``` and ```token``` parameters in ```terraform.tfvars``` file.
You can find these data clicking "Account Details" button on the Workbench (or Vocareum) page then clicking on "Show" button.

## Terraform Installation
In our case, Terraform was installed on a Macintosh computer through the terminal and Homebrew.
Following the official guide you can find the procedure for you operating system (https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started).
For MacOs it was a fundamental prerequisite to install the following software:


* Homebrew:
```
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

* XCode:
```
$ xcode-select --install
```

* Gcc:
```
$ brew install --build-from-source gcc
```

After that, following the guide, you need to execute the following commands:
```
$ brew tap hashicorp/tap

$ brew install hashicorp/tap/terraform

$ brew upgrade hashicorp/tap/terraform
```

Check the installation with:
```
terraform -help
```


## Script Preparation
Through the shell, navigate to the folder “terraform-aws-instance(educate)” .

Edit the file ```variables.tf``` in order to change the parameters according to your needs, in particular:
* ```region:``` the region in which to instantiate the machines,
* ```instance_type:``` the type of machines to instantiate (t2.micro is the type offered by the aws free tier account),
* ```ami_image:``` specifies the desired OS image,
* ```datanode_count:``` the number of slave nodes,
* ```subnet_id:``` specifies the subnet id to be used for the private addresses of the nodes.
To find this information, you can access to the AWS VPC service, on the left menu open VIRTUAL PRIVATE CLOUD and select “Subnets”: all subnets will appear.
If there aren't any, create one.
Note the subnet id to be used in the terraform script variable.
In the IPv4 CIDR field we find the address of the subnet: the addresses of our nodes must be included within this subnet.
* ```namenode_ip:``` is the private ip address for the master instance.
* ```ips:``` is the list of private ip addresses belonging to your aws subnet for slave instances.
Warning: if these ip addresses are modified, they must also be modified on the install.sh file from line 22 to line 27.

We generate an SSH key with this command:
```ssh-keygen -f <terraform_directory>/localkey```

We generate a key pair from the AWS interface:
Go to the EC2 service.
On the left menu, look for the item "Network and security" where you can click on "Key pairs".

Click on the button at the top right "create a key pair", enter the name "chiave_aws", choose the .pem format and continue to create the file.

Save the file in the terraform folder.

Type the following command to set the right permissions on the file you just downloaded:
```chmod 400 chiave_aws.pem```


Now you can proceed with the execution of the script.


## Script Executing
Type the following command to initialize the directory:
```terraform init```

Then you can run the command to create and launch instances on AWS:
```terraform apply```

When prompted, type the answer ```yes```.

Wait for the actions to complete.

The EC2 instances will be created in which all the necessary software will be installed automatically (java, spark-3.0.2, hadoop-2.7.7, Python 3.8) thanks to the bash install.sh script that will be started on the instances.
Instances will be named as s01 (the master) and s02, s03, etc… (the slaves)

At the end, the DNS addresses of the master and the slaves will be displayed in green.

With these addresses it will be possible to access the instances through the command:
```ssh -i <terraform_directory>/chiave_aws.pem ubuntu@<Public_DNS>```


## Environment destruction
If we want to cancel the execution of the command ```apply``` you can execute:
```terraform destroy```

When prompted, type the answer ```yes```.

We can use the same command to delete instances when we no longer need them.

## This script is based on the following project:
 * [hadoop-spark-cluster-deployment](https://github.com/kostistsaprailis/hadoop-spark-cluster-deployment)
