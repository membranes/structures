"""Module setup.py"""
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.functions.directories
import src.s3.bucket
import src.s3.keys


class Setup:
    """
    Description
    -----------

    Sets up local & cloud environments
    """

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters, warehouse: str):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this project, e.g., region code
                              name, buckets, etc.
        :param warehouse: The temporary local directory where data sets are initially placed,
                          prior to transfer to Amazon S3 (Simple Storage Service)
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__warehouse = warehouse

    def __s3(self) -> bool:
        """
        Prepares an Amazon S3 (Simple Storage Service) bucket.

        :return:
        """

        # An instance for interacting with Amazon S3 buckets.
        bucket = src.s3.bucket.Bucket(service=self.__service, location_constraint=self.__s3_parameters.location_constraint,
                                      bucket_name=self.__s3_parameters.internal)

        if bucket.exists():

            temporary = src.s3.keys.Keys(
                service=self.__service, bucket_name=self.__s3_parameters.internal).all()

            return bucket.empty() if temporary else True

        return bucket.create()

    def __local(self) -> bool:
        """

        :return:
        """

        directories = src.functions.directories.Directories()
        directories.cleanup(path=self.__warehouse)

        return directories.create(path=self.__warehouse)

    def exc(self) -> bool:
        """

        :return:
        """

        return self.__s3() & self.__local()
