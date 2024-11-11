"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor
        """

        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.prepared_ = os.path.join(self.warehouse, 'prepared')

        # Addressing category imbalance ...
        self.minimum_category_frequency = 1000

        # A template of Amazon S3 (Simple Storage Service) parameters
        self.s3_parameters_template = 'https://raw.githubusercontent.com/membranes/configurations/refs/heads/master/data/s3_parameters.yaml'

        # Node: The raw data to be structured
        self.node = 'raw/dataset.csv'

        # The metadata of the prepared data
        text = 'fields: {"sentence_identifier": "The sentence identification code.", "sentence": "A news brief sentence.", "tagstr": "The tag of each word or punctuation in the sentence.", "code_per_tag": "The code of each tag in tagstr."}'
        tags = 'terms: {"Annotation": {"I": "inside", "B": "beginning"},  "Categories": {"ORG": "organisation names", "GPE": "geopolitical entity", "LOC": "geographical names", "TIM": "time representations", "PER": "names of people"}}'

        self.metadata = {'description': 'The prepared data collection for the token classification project.',
                         'details': 'The collection consists of (a) the data set of news briefs, i.e., data.csv, (b) the identity ' +
                                    'and label mapping enumerator.json, and (c) the inverse of enumerator.json, i.e., ' +
                                    'archetype.json.',
                         'file-data': text,
                         'file-enumerator': tags,
                         'file-archetype': tags}
