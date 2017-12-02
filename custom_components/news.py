"""
"""
import asyncio
import logging
import time
import feedparser
from html.parser import HTMLParser
# pip install git+https://github.com/Danielhiversen/sports-tracker-liberator
from bs4 import BeautifulSoup
from xml.parsers.expat import ExpatError
import requests
import xmltodict
from datetime import timedelta

from homeassistant.const import ATTR_ENTITY_ID
from homeassistant.util import dt as dt_util
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import track_state_change, track_time_change
from homeassistant.helpers.event import track_point_in_utc_time
from homeassistant.components.sensor.rest import RestData


# The domain of your component. Should be equal to the name of your component.
DOMAIN = "news"

# List of component names (string) your component depends upon.
# We depend on group because group will be loaded after all the components that
# initialize devices have been setup.
DEPENDENCIES = ['group', ]

# Shortcut for the logger
_LOGGER = logging.getLogger(__name__)

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed = d
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def num2str(num):
  num = float(num)
  if (num - int(num)) == 0:
      num = int(num)
  return str(round(num, 1)).replace("."," komma ")


def setup(hass, config):
    """Setup component."""

    news_rss = []
    auth_token=config[DOMAIN].get("token")

    def _get_text(message_type=None):
        news = ""

        if message_type in [1, 2]:
            return news

        news = news + "Här kommer senaste nytt:  "
        if False:
            _news_rss = news_rss
        else:
            _news_rss = news_rss[:2]
        for case in _news_rss:
            news = news + case + " "
        return news

    @asyncio.coroutine
    def _read_news(service):
        _url = service.data.get("url")
        message_type = int(service.data.get("message_type", -1))
        news = _get_text(message_type)

        data = {}
        if service and service.data.get(ATTR_ENTITY_ID):
            data[ATTR_ENTITY_ID] = service.data.get(ATTR_ENTITY_ID)
        data['message'] = news
        data['cache'] = False

        autoradio = True if service.data.get("entity_id_radio") else False
        yield from hass.services.async_call('tts', 'google_say', data, blocking=autoradio)
        return
        if not autoradio:
            return
        # if vekking:

        data = {}
        data[ATTR_ENTITY_ID] = service.data.get("entity_id_radio")
        data[ATTR_ENTITY_ID] = service.data.get("entity_id_radio")
        if service.data.get("radio_option"):
            data['option'] = service.data.get("radio_option")
        else:
            data['option'] = "P3"
        hass.services.call('input_select', 'select_option', data)

    def _rss_news():
        nonlocal news_rss
        resource = _url
        method = 'GET'
        payload = auth = headers = None
        rest = RestData(method, resource, auth, headers, payload, verify_ssl=True)
        rest.update()
        news_rss = []
        if rest.data is None:
            return
        raw_data = BeautifulSoup(rest.data, 'html.parser')
        prew_text = ""
        for raw_text in raw_data.select("p"):
            text = strip_tags(str(raw_text))
            if text == prew_text:
                continue
            prew_text = text
            news_rss.append(text)
            if len(news_rss) > 2:
                break
        _feed = feedparser.parse("http://www.yr.no/sted/Norge/S%C3%B8r-Tr%C3%B8ndelag/Trondheim/Trondheim/varsel.xml")
        summary = _feed.feed.get("summary")
        if summary is None:
            return
        news_rss.append("Værvarsel " + strip_tags(summary).replace("<strong>","").replace("</strong>",""))


    _rss_news()

    hass.services.register(DOMAIN, "read_news", _read_news)
    print(_get_text())

    return True
