provider "aws" {
    region  = var.region
    profile = var.profile
}


resource "aws_s3_bucket" "bigdatabucket" {
  bucket = var.bucketName
  acl    = "private"
  tags = {
    Name        = var.bucketName
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_object" "dataset-obj" {
    for_each = fileset("tweet_data/", "*")
    bucket = aws_s3_bucket.bigdatabucket.id
    key = "tweet_data/${each.value}"
    source = "tweet_data/${each.value}"
    etag = filemd5("tweet_data/${each.value}")
}