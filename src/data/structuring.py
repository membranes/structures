"""Module structuring.py"""
import logging

import pandas as pd


class Structuring:
    """
    Description
    -----------

    This class builds the expected data structure for ...
    """

    def __init__(self, data: pd.DataFrame, enumerator: dict) -> None:
        """
        Creates the expected structure.  Within <data> each distinct sentence
        is split across rows; a word per row, in order.  The Specimen class re-constructs the
        original sentences.

        :param data:
        :param enumerator:
        """

        self.__data: pd.DataFrame = data
        self.__enumerator: dict = enumerator

        # Logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.__logger = logging.getLogger(__name__)

    @staticmethod
    def __sentences(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        sentences: pd.DataFrame = blob.copy().drop(columns='tag').groupby(
            by=['sentence_identifier'])['word'].apply(' '.join).to_frame()

        return sentences

    @staticmethod
    def __labels(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob:
        :return:
        """

        labels: pd.DataFrame = blob.copy().drop(columns='word').groupby(
            by=['sentence_identifier'])['tag'].apply(','.join).to_frame()

        return labels

    def __reformatting(self, blob: pd.DataFrame) -> pd.DataFrame:
        """
        frame['words'] = frame['sentence'].str.split()
        frame['codes'] = frame['tagstr'].str.split(',').apply(lambda x: list(map(self.__enumerator.get, x)))

        :param blob: The data, which has fields sentence_identifier, sentence, & tagstr
        :return:
        """

        frame = blob.copy()
        frame['sentence_identifier'] = frame['sentence_identifier'].str.replace(pat='Sentence: ', repl='').str.strip()
        frame['code_per_tag'] = frame['tagstr'].str.split(',').apply(lambda x: ','.join(map( str, map(self.__enumerator.get, x))))

        return frame

    def exc(self) -> pd.DataFrame:
        """

        :return:
        """

        blob = self.__data[['sentence_identifier', 'word', 'tag']].copy()

        # Re-build the sentences, and a string of the corresponding labels per sentence word.
        sentences = self.__sentences(blob=blob)
        labels = self.__labels(blob=blob)

        # The frames <sentences> & <labels> each have a _sentence identifiers_ index field.
        frame: pd.DataFrame = sentences.join(labels).drop_duplicates()
        frame.reset_index(inplace=True)
        frame.rename(columns={'word': 'sentence', 'tag': 'tagstr'}, inplace=True)

        # Formatting
        frame = self.__reformatting(blob=frame)

        # Preview
        self.__logger.info('\n\n%s\n\n', frame.head())
        frame.info()

        return frame
