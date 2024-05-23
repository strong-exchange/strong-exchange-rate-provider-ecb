import httpx
from pathlib import Path
from xml.etree import ElementTree as ET
from .data import rates, history_data


timeout = httpx.Timeout(60.0, connect=10.0)
client = httpx.Client(timeout=timeout)


ns = {
    "euro_fx_ref": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref",
    "ecb_stats": "http://www.ecb.europa.eu/vocabulary/stats/exr/1",
}


async def update_daily_rates_from_ecb():
    # ToDo: add test for this variable
    global latest_daily_rate_for

    response = client.get(
        "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    )
    xml = ET.fromstring(response.text)
    fx_ref_for_date = xml.find("euro_fx_ref:Cube", ns).find("euro_fx_ref:Cube", ns)
    latest_daily_rate_for = fx_ref_for_date.attrib["time"]
    for currency_rate in fx_ref_for_date:
        currency_name = currency_rate.attrib["currency"]
        rate = currency_rate.attrib["rate"]
        rates[currency_name] = rate


def load_history_from_ecb_file():
    BASE_DIR = Path(__file__).parent.parent
    path_to_xml_with_history = BASE_DIR / "ecb_rates_history" / "eurofxref-sdmx.xml"
    xml = ET.parse(path_to_xml_with_history)

    xml_dataset = xml.getroot().find("ecb_stats:DataSet", ns)
    xml_groups = xml_dataset.findall("ecb_stats:Group", ns)
    xml_series_all = xml_dataset.findall("ecb_stats:Series", ns)

    for xml_group, xml_series in zip(xml_groups, xml_series_all):
        symbol = xml_group.attrib["CURRENCY"]
        xml_rates_by_date = xml_series.findall("ecb_stats:Obs", ns)
        for xml_rate_for_date in xml_rates_by_date:
            history_day = history_data[xml_rate_for_date.attrib["TIME_PERIOD"]]
            history_day[symbol] = xml_rate_for_date.attrib["OBS_VALUE"]
