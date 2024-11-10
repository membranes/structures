"""Module structuring.py"""
import logging

import pandas as pd


class Structuring:
    """
    Description
    -----------

    This class builds the expected data structure for ...
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Creates the expected structure.  Within <data> each distinct sentence
        is split across rows; a word per row, in order.  The Specimen class re-constructs the
        original sentences.

        :param data:
        """

        self.__data: pd.DataFrame = data

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

    @staticmethod
    def __reformatting(blob: pd.DataFrame) -> pd.DataFrame:
        """

        :param blob: The data, which has fields sentence_identifier, sentence, & tagstr
        :return:
        """

        frame = pd.DataFrame()
        frame['id'] = blob.copy()['sentence_identifier'].str.replace(pat='Sentence: ', repl='').str.strip()
        frame['sentence'] = blob.copy()['sentence'].str.strip().str.split().apply(
            lambda words: list([word.strip() for word in words]))
        frame['tagstr'] = blob.copy()['tagstr'].str.strip().str.split(',')

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
        self.__logger.info('\n\n%s\n\n', frame.head())
        frame.info()

        return frame
