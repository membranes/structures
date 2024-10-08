"""Module source.py"""

import dask.dataframe as dfr
import pandas as pd

import src.elements.s3_parameters as s3p
import config


class Source:
    """
    Reads-in the raw data
    """

    def __init__(self, s3_parameters: s3p.S3Parameters) -> None:
        """
        Construction
        """

        self.__path = ('s3://' + s3_parameters.internal + '/' +
                       s3_parameters.path_internal_data + config.Config().node)

        # Naming convention
        self.__names: dict[str, str] = {'Word': 'word', 'POS': 'part', 'Tag': 'tag'}

    def __read(self) -> dfr.DataFrame:
        """
        Reads-in the data set.

        :return:
        """

        try:
            frame: dfr.DataFrame = dfr.read_csv(path=self.__path, header=0)
        except ImportError as err:
            raise err from err

        frame: dfr.DataFrame = frame.assign(sentence_identifier=frame['Sentence #'].ffill())
        frame: dfr.DataFrame = frame.drop(columns='Sentence #')

        return frame

    def __rename(self, blob: dfr.DataFrame) -> dfr.DataFrame:
        """
        Renames the fields

        :param blob: A dask data frame
        :return:
        """

        frame: dfr.DataFrame = blob.copy()
        frame: dfr.DataFrame = frame.rename(columns=self.__names)

        return frame

    @staticmethod
    def __tag_splits(blob: dfr.DataFrame) -> dfr.DataFrame:
        """
        Splits each tag into its annotation & category parts.

        :param blob:
        :return:
        """

        splits: dfr.DataFrame = blob['tag'].str.split(pat='-', n=2, expand=True)
        splits: dfr.DataFrame = splits.rename(columns={0: 'annotation', 1: 'category'})
        splits: dfr.DataFrame = splits.assign(category=splits['category'].fillna(value='O'))
        frame : dfr.DataFrame = blob.join(other=splits)

        return frame

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        frame: dfr.DataFrame = self.__read()
        frame: dfr.DataFrame = self.__rename(blob=frame)
        frame: dfr.DataFrame = frame.assign(word=frame['word'].astype(str))
        frame: dfr.DataFrame = self.__tag_splits(blob=frame)

        return frame.compute()
