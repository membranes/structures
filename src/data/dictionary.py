"""Module dictionary.py"""
import glob
import logging
import os

import numpy as np
import pandas as pd


class Dictionary:
    """
    Class KeyStrings
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

    def __local(self, path: str, extension: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :return:
        """

        splitter = os.path.basename(path) + os.path.sep
        self.__logger.info(splitter)

        # The list of files within the path directory, including its child directories.
        files: list[str] = glob.glob(pathname=os.path.join(path, '**',  f'*.{extension}'),
                                     recursive=True)

        details: list[dict] = [
            {'file': file,
             'vertex': file.rsplit(splitter, maxsplit=1)[1]}
            for file in files]

        return pd.DataFrame.from_records(details)

    @staticmethod
    def __metadata() -> dict:
        """

        :return:
        """

        return {'description': 'The prepared data collection for the token classification project.',
                'details': 'The collection consists of (a) the data, i.e., data.csv, (b) the identity and label mapping enumerator.json, and (c) the inverse of enumerator.json, i.e., archetype.json.'}

    def exc(self, path: str, extension: str, prefix: str) -> pd.DataFrame:
        """

        :param path: The path wherein the files of interest lie
        :param extension: The extension type of the files of interest
        :param prefix: The Amazon S3 (Simple Storage Service) where the files of path are heading
        :return:
        """

        local: pd.DataFrame = self.__local(path=path, extension=extension)

        # Building the Amazon S3 strings
        frame = local.assign(key=prefix + local["vertex"])

        # The metadata dict strings
        frame['metadata'] = np.array(self.__metadata()).repeat(frame.shape[0])

        return frame[['file', 'key', 'metadata']]
