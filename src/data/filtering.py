"""Module filtering.py"""
import logging

import pandas as pd


class Filtering:

    def __init__(self):
        """

        Constructor
        """

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    def __call__(self, data: pd.DataFrame, tags: pd.DataFrame) -> pd.DataFrame:
        """

        :param data:
        :param tags:
        :return:
        """

        # Determining the instances/words that have viable tag categories
        conditionals: pd.Series = data['category'].isin(values=tags['category'].unique())

        # Hence, the sentences that include one or more inviable categories
        invalid = data.copy().loc[~conditionals, 'sentence_identifier'].unique()

        # Hence, valid sentence identifiers
        markings = ~data['sentence_identifier'].isin(invalid)

        # Finally, the viable instances
        frame: pd.DataFrame = data.copy().loc[markings, :]

        self.__logger.info(frame.head())
        self.__logger.info(frame['category'].unique())
        frame.info()

        return frame
