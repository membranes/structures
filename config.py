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

        self.datapath = os.path.join(os.getcwd(), 'data')
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.prepared_ = os.path.join(self.warehouse, 'prepared')

        # Addressing category imbalance ...
        self.minimum_category_frequency = 1000

        # A template of Amazon S3 (Simple Storage Service) parameters
        self.s3_parameters_template = 'https://raw.githubusercontent.com/membranes/.github/refs/heads/master/profile/s3_parameters.yaml'
