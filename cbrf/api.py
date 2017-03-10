# -*- coding: utf-8 -*-

"""
cbrf.api
~~~~~~~~

This module implements the cbrf wrapper API.

:copyright: (c) 2012 by Kenneth Reitz.
:license: MIT
"""

import datetime
from xml.etree.ElementTree import XML, Element

import requests

from . import const
from . import utils


def get_currencies_info() -> Element:
    """Get META information about currencies

    url: http://www.cbr.ru/scripts/XML_val.asp

    :return: :class: `Element <Element 'Valuta'>` object
    :rtype: ElementTree.Element
    """
    response = requests.get(const.CBRF_API_URLS['info'])
    response.encoding = 'windows-1251'

    return XML(response.text)


def get_daily_rate(date_req: datetime.datetime = None, lang: str = 'rus') -> Element:
    """ Getting currency for current day.

    see example: http://www.cbr.ru/scripts/Root.asp?PrtId=SXML

    :param date_req:
    :type date_req: datetime.datetime
    :param lang: language of API response ('eng' || 'rus')
    :type lang: str

    :return: :class: `Element <Element 'ValCurs'>` object
    :rtype: ElementTree.Element
    """
    if lang not in ['rus', 'eng']:
        raise ValueError('"lang" must be string. "rus" or "eng"')

    base_url = const.CBRF_API_URLS['daily_rus'] if lang == 'rus' \
        else const.CBRF_API_URLS['daily_eng']

    url = base_url + 'date_req=' + utils.date_to_str(date_req) if date_req else base_url

    response = requests.get(url=url)
    response.encoding = 'windows-1251'

    return XML(response.text)


def get_dynamic_rates(date_req1: datetime.datetime,
                      date_req2: datetime.datetime,
                      currency_id: str) -> Element:
    """

    :param date_req1: begin date
    :type date_req1: datetime.datetime
    :param date_req2: end date
    :type date_req2: datetime.datetime
    :param currency_id: currency code (http://www.cbr.ru/scripts/XML_val.asp?d=0)
    :type currency_id: str

    :return: :class: `Element <Element 'ValCurs'>` object
    :rtype: ElementTree.Element
    """
    url = const.CBRF_API_URLS['dynamic'] + \
          f'date_req1={utils.date_to_str(date_req1)}&' \
          f'date_req2={utils.date_to_str(date_req2)}&' \
          f'VAL_NM_RQ={currency_id}'

    response = requests.get(url=url)
    response.encoding = 'windows-1251'

    return XML(response.text)
