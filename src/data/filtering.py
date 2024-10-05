"""Module filtering.py"""

import pandas as pd


class Filtering:
    """
    Class Filtering

    Filters out inviable sentences because they include one or more words
    associated with inviable categories.  A category is inviable if the
    number of words associated with the category is < config.Config().minimum_category_frequency
    """

    def __init__(self):
        """

        Constructor
        """

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

        return frame
