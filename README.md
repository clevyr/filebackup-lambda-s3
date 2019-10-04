# Python filebackup-lambda-s3

[![](https://images.microbadger.com/badges/image/clevyr/filebackup-lambda-s3.svg)](https://microbadger.com/images/clevyr/filebackup-lambda-s3 "Get your own image badge on microbadger.com")

This is a Docker-compatible Python script to make backup of any and pushes it to an S3 bucket.

This is intended to be ran under fargate or a lambda function.

Use lambda if the total size is less than 256 MB due to disk limitations, otherwise use fargate.

Make sure the lambda or fargate container has IAM access to `s3:PutObject and ses:SendEmail`

## Environment Variables

|  Variable   |                             Details                             |              Example               |
| ----------- | --------------------------------------------------------------- | ---------------------------------- |
| IN_FOLDER   | the folder to backup, usually a volume bind                     | `/data/in`                         |
| BUCKET_NAME | The S3 bucket to upload the backup to                           | `app-dev-backups`                  |
| SES_REGION  | The region that SES is working in                               | `us-east-1`                        |
| EMAIL_FROM  | The email address to send emails from                           | `backups@domain.com`               |
| EMAIL_TO    | The list of email addresses to send to, separated by semicolons | `user@domain.com;user1@domain.com` |
