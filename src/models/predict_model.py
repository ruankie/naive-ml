# -*- coding: utf-8 -*-
import click
import traceback
import logging.config
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def pipeline(y):
    logger.info('Start scoring data.')
    try:
        x = 10/y
    except ZeroDivisionError as err:
        logger.error('Cannot divide by zero: %s', err, exc_info=True)
    except:
        logger.error('Uncaught exception: %s', traceback.format_exc())


@click.command()
@click.argument('input_filepath', default='data/processed', type=click.Path(exists=True))
@click.argument('output_filepath', default='models', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs predict model scripts to score the training data from (../processed) into
        predict data (saved in ../models).
    """
    logger.info(f'Read from {input_filepath}, write to {output_filepath}.')

if __name__ == '__main__':

    load_dotenv(find_dotenv())

    #pylint: disable = no-value-for-paramete
    main()
