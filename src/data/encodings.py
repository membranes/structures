"""Module encodings.py"""
import logging
import typing

import pandas as pd


class Encodings:
    """

    This class enumerates the viable tags, and provides the inverse mappings.
    """

    def __init__(self):
        """
        Constructor
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __coding(self, series: pd.Series) -> typing.Tuple[dict, dict]:
        """
        Tags enumeration, and their inverse mappings.

        :param series:
        :return:
        """

        enumerator: dict = {k: v for v, k in enumerate(iterable=series)}
        self.__logger.info(enumerator)

        archetype: dict = {v: k for k, v in enumerator.items()}
        self.__logger.info(archetype)

        return enumerator, archetype

    def exc(self, tags: pd.DataFrame) -> typing.Tuple[dict, dict]:
        """

        :param tags: pd.DataFrame: tag | annotation | category
        :return:
        """

        enumerator, archetype = self.__coding(series=tags['tag'])

        return enumerator, archetype
