import json
from os import environ, mkdir, path, getcwd
from threading import Timer
import tarfile
from time import strftime, gmtime

import boto3 as boto
import traceback
import sys

s3 = boto.resource("s3")


def exit(error=None):
    if error is not None:
        print('Error occured, sending email...')
        print(error)
        email(error, environ.get('EMAIL_FROM'),
              environ.get('EMAIL_TO').split(';'))


def main():
    try:
        filename = "/tmp/backup-fileassets-{}.tgz".format(
            strftime("%Y-%m-%d_%H%M%S", gmtime()))

        print("Creating {}".format(filename))
        with tarfile.open("{}".format(filename), "w:gz") as tar:
            tar.add(environ.get('IN_FOLDER'),
                    arcname=path.basename(environ.get('IN_FOLDER')))

        bucket_name = environ.get('BUCKET_NAME')
        if bucket_name is not None:
            s3.Bucket(bucket_name).upload_file(
                filename, path.basename(filename))
        else:
            print(f"Backup is available at {filename}")
        print("Done")
        exit()
    except Exception as e:
        exit(e)


def email(error, from_address, addresses):
    try:
        ses = boto.client('ses', region_name=environ.get('SES_REGION'))
        bucket_name = environ.get('BUCKET_NAME')
        errString = ''.join(traceback.format_exception(
            etype=type(error), value=error, tb=error.__traceback__))
        response = ses.send_email(
            Source=from_address,
            Destination={
                'ToAddresses': addresses
            },
            Message={
                'Subject': {
                    'Data': 'Error: Backup Failed'
                },
                'Body': {
                    'Text': {
                        'Data': f'The database backup for {bucket_name} failed:\n{errString}'
                    }
                }
            }
        )
    except Exception as e:
        print('Error sending email...')
        print(e)


if __name__ == "__main__":
    main()


def lambda_handler(_, __):
    main()
