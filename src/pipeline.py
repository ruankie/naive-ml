# -*- coding: utf-8 -*-
import click
import traceback
import logging.config
from pythonjsonlogger import jsonlogger
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

import data.make_dataset as md
import features.build_features as fe
import models.train_model as tm
import models.predict_model as pm
import visualization.visualize as viz
from utilities.util import get_today_date

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger()

def pipeline():
    logger.info('Start running pipeline.')

@click.command()
@click.argument('input_filepath', default='data/raw', type=click.Path(exists=True))
@click.argument('output_filepath', default='data/processed', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs the entire pipeline from data to models/visualisation.
    """

    logger.info('Start running pipeline for: %s.', get_today_date())

    md.pipeline()
    fe.pipeline()
    tm.pipeline()
    pm.pipeline(0) # example of providing traceback in error handling
    pm.pipeline('0') # example of providing traceback with uncaught exceptions


if __name__ == '__main__':

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
