"""Module prefix.py"""
import boto3

import src.elements.service as sr


class Prefix():

    def __init__(self, service: sr.Service, bucket_name: str):
        """

        :param service:
        :param bucket_name:
        """

        self.__s3_resource: boto3.session.Session.resource = service.s3_resource
        self.__bucket_name = bucket_name

        # A bucket instance
        self.__bucket = self.__s3_resource.Bucket(name=self.__bucket_name)

    def delete(self, key: str):
        """

        :param key: An Amazon S3 (Simple Storage Service) prefix
        :return:
        """

        return self.__bucket.delete_objects({'Key': key})
