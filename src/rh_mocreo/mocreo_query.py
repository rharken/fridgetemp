""" mocreo_query.py - get the temperatures from the mocreo hub for the refrigerator
"""
from datetime import datetime
import json
import requests
from bs4 import BeautifulSoup

def process_labels(cfg: dict[str, object]) -> dict[str, str]:
    """ Process Labels from a config dictionary (json)

    Args:
        cfg (dict[str, object]): Configuration dictionary

    Returns:
        dict[str, str]: A dictionary containing the labels to use
    """
    labels = {}
    if 'labels' in cfg:
        lbl = cfg['labels']
        for l in lbl: # pyright: ignore[reportUnknownVariableType, reportGeneralTypeIssues]
            labels[l['sn']] = l['name']

    return labels # pyright: ignore[reportUnknownVariableType]


def mocreo_query(config: dict[str, object]) -> str:
    """ main code for getting temps from a mocreo hub
    """
    # Process lables
    labels = process_labels(config)

    # Set up a session
    s = requests.Session()

    # Build the login url and request data
    url = f"http://{config['mocreo_hub']}/login"
    rdata = {"path": "/", "passwd": f"{config['password']}"}

    # login to start the session
    req = s.post(url, rdata)
    if req.status_code != 200:
        print(f"ERROR authorizing: {req.status_code}")
        return ""

    # now request the sensor page
    curr_time = datetime.now()
    url = f"http://{config['mocreo_hub']}/sensors"
    req = s.get(url)
    if req.status_code != 200:
        print(f"ERROR in getting sensors: {req.status_code}")
        return ""

    # parse the sensor page for the temperatures
    if req.text:
        soup = BeautifulSoup(req.text, 'html.parser')

        ret = []
        cards = soup.select('.card')
        for c in cards:
            output = {}
            serial = ""
            serial_and_updated = c.select('.text-muted')
            temperature = c.select('.digits')
            if len(serial_and_updated) > 0:
                serial            = serial_and_updated[0].get_text().split()[-1]
                output['sn']      = serial
            if len(serial_and_updated) > 1:
                output['updated'] = serial_and_updated[1].get_text()
            if len(temperature) > 0:
                output['temp']    = temperature[0].get_text()
            if labels and serial in labels:
                output['name']    = labels[serial]
            output['current_time'] = curr_time.strftime("%Y-%m-%d %H:%M:%S")

            ret.append(output) # pyright: ignore[reportUnknownMemberType]

        return json.dumps(ret)
    return ""
