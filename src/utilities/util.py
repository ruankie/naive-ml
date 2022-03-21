#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

logging.config.fileConfig('logging.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def get_today_date():
    today = datetime.now().date()
    return today
