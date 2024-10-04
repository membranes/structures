"""Module prefix.py"""
import logging
import boto3
import botocore.exceptions

import src.elements.service as sr

import src.s3.keys


class Prefix():

    def __init__(self, service: sr.Service, bucket_name: str):
        """

        :param service:
        :param bucket_name:
        """

        self.__service: sr.Service = service
        self.__s3_client = self.__service.s3_client
        self.__bucket_name = bucket_name



        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def delete(self, objects: list[dict]):
        """

        :param objects: An Amazon S3 (Simple Storage Service) ...
        :return:
        """

        try:
            response = self.__s3_client.delete_objects(
                Bucket=self.__bucket_name, Delete={'Objects': objects, 'Quiet': False})
        except botocore.exceptions.ClientError as err:
            raise err from err

        self.__logger.info(response)

        return response

    def objects(self, prefix: str) -> list[str]:
        """

        :param prefix:
        :return:
        """

        instance = src.s3.keys.Keys(service=self.__service, bucket_name=self.__bucket_name)

        return instance.excerpt(prefix=prefix)