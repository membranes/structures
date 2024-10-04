"""Module main.py"""
import logging
import os
import sys


def main() -> None:
    """
    Entry point

    :return:
        None
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Set up
    setup: bool = src.setup.Setup(service=service, s3_parameters=s3_parameters).exc()
    logger.info('Set: %s', setup)

    # Get
    if setup:
        messages = src.data.interface.Interface(service=service, s3_parameters=s3_parameters).exc()
        logger.info(messages)

    # Delete Cache Points
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Modules
    import config
    import src.data.source
    import src.elements.s3_parameters as s3p
    import src.elements.service as sr

    import src.functions.cache
    import src.functions.service
    import src.s3.s3_parameters
    import src.setup
    import src.data.interface

    # Configurations
    configurations = config.Config()

    # S3 S3Parameters, Service Instance
    s3_parameters: s3p.S3Parameters = src.s3.s3_parameters.S3Parameters().exc()
    service: sr.Service = src.functions.service.Service(region_name=s3_parameters.region_name).exc()

    main()
