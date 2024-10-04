"""Module setup.py"""
import os

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.directories
import src.s3.bucket
import src.s3.keys
import src.s3.prefix

import config


class Setup:
    """
    Description
    -----------

    Sets up local & cloud environments
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__configurations = config.Config()

        # The prefix in focus within the Amazon S3 () bucket in focus.
        parts = self.__configurations.prepared_.split(sep=(self.__configurations.warehouse + os.sep))
        self.__prefix = self.__s3_parameters.path_internal_data + parts[-1] + '/'

    def __s3(self) -> bool:
        """
        Prepares an Amazon S3 (Simple Storage Service) bucket.

        :return:
        """

        # An instance for interacting with Amazon S3 buckets.
        bucket = src.s3.bucket.Bucket(service=self.__service, location_constraint=self.__s3_parameters.location_constraint,
                                      bucket_name=self.__s3_parameters.internal)

        if bucket.exists():

            instance = src.s3.prefix.Prefix(
                service=self.__service, bucket_name=self.__s3_parameters.internal)

            keys = instance.objects(prefix=self.__prefix)
            objects = [{'Key' : key} for key in keys]

            state = instance.delete(objects=objects)
            print(state)

            return True if state else False

        return bucket.create()

    def __local(self) -> bool:
        """

        :return:
        """

        directories = src.functions.directories.Directories()
        directories.cleanup(path=self.__configurations.warehouse)

        return directories.create(path=self.__configurations.prepared_)

    def exc(self) -> bool:
        """

        :return:
        """

        return self.__s3() & self.__local()
