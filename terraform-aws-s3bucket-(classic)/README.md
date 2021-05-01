# AWS - S3 support

Introduction: this guide is based on the script we created and tested on an AWSfree-tier account.
With some minor modifications, the script can also be used on an AWS educate account.

1. [Package contents](#Package-contents)
2. [How to use](#How-to-use)

## Package contents
It is important to download the entire GitHub project and maintain the directory structure.
* main.tf: terraform script that creates the S2 bucket on your AWS account
* variables.tf: contains the configuration parameters for the script

## How to use
Before starting, you need to create a ```tweetdata``` folder in the directory of the terraform application in question and put all the files we want in our bucket inside.
The only configuration in the code that may be necessary is to modify the ```bucketName``` variable in the ```variables.tf``` file by inserting the name we want to give to the bucket.

ATTENTION: you can only use lowercase letters, numbers, the characters '-' and '.' and which must have a letter or number at the ends. Additionally, the bucket name must be globally unique.

After that we can execute the usual commands.
First: 
```
terraform init
```
And then:
```
terraform apply
```
Wait for the upload to complete.
Depending on the volume of data and the speed of your connection, the time can vary from a few minutes to many hours.
To check it, you can log into the S3 service of your AWS account and view the created bucket.
Once finished we can use the bucket data in our master instance using the following command to do the dataset transfer:
```
aws s3 sync s3://<nome-del-bucket>/tweet_data tweet_data
```
