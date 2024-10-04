"""Module source.py"""
import logging

import pandas as pd

import src.data.dictionary
import src.data.encodings
import src.data.filtering
import src.data.source
import src.data.structuring
import src.data.tags
import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.ingress

import config


class Interface:

    def __init__(self, service: sr.Service,  s3_parameters: s3p):
        """

        :param service: A suite of services for interacting with Amazon Web Services.
        :param s3_parameters: The overarching S3 parameters settings of this
                              project, e.g., region code name, buckets, etc.
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters
        self.__configurations = config.Config()

        # The raw data
        self.__raw = src.data.source.Source(s3_parameters=s3_parameters).exc()

        # Instances
        self.__dictionary = src.data.dictionary.Dictionary()

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __elements(self):
        """

        :return:
        """

        elements = src.data.tags.Tags(data=self.__raw).exc()
        enumerator, archetype = src.data.encodings.Encodings().exc(elements=elements)

        return elements, enumerator, archetype

    def __filtering(self, elements: pd.DataFrame) -> pd.DataFrame:
        """
        Filtering out instances of the raw data that are associated with elements/tags
        that have fewer than an expected number of occurrences.

        :param elements:
        :return:
        """

        filtering = src.data.filtering.Filtering()

        return filtering(data=self.__raw, elements=elements)

    @staticmethod
    def __structuring(filtered: pd.DataFrame):
        """

        :param filtered:
        :return:
        """

        return src.data.structuring.Structuring(data=filtered).exc()

    def exc(self):
        """

        :return:
        """

        elements, enumerator, archetype = self.__elements()
        filtered = self.__filtering(elements=elements)
        data = self.__structuring(filtered=filtered)

        # Save: Upcoming
        self.__logger.info(enumerator)
        self.__logger.info(archetype)
        self.__logger.info(data)

        # Inventory of data files
        # strings = self.__dictionary.exc(
        #     path=self.__configurations.prepared_, extension='*', prefix=self.__s3_parameters.path_internal_data)

        # Transfer
        # messages = src.s3.ingress.Ingress(
        #     service=self.__service, bucket_name=self.__s3_parameters.internal).exc(strings=strings)
        #
        # return messages