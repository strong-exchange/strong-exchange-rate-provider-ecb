import httpx
# from rss_parser import RSSParser
# import feedparser
from xml.etree import ElementTree as ET
from .data import rates
from .data import latest_daily_rate_for


timeout = httpx.Timeout(60.0, connect=10.0)
client = httpx.Client(timeout=timeout)


ns = {
    'euro_fx_ref': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'
}

def update_daily_rates_from_ecb():
    global latest_daily_rate_for

    response = client.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
    xml = ET.fromstring(response.text)
    fx_ref_for_date = xml.find('euro_fx_ref:Cube', ns).find('euro_fx_ref:Cube', ns)
    latest_daily_rate_for = fx_ref_for_date.attrib['time']
    for currency_rate in fx_ref_for_date:
        currency_name = currency_rate.attrib['currency']
        rate = currency_rate.attrib['rate']
        rates[currency_name] = rate
