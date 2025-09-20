""" mocreo_query.py - get the temperatures from the mocreo hub for the refridgerator
"""
import json
import requests
from bs4 import BeautifulSoup

def process_labels(cfg: dict[str, object]) -> dict[str, str]:
    """ Process Labels from a config dictionary

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
            serial_number = c.select('.text-muted')
            temperature = c.select('.digits')
            sn = serial_number[0].get_text().split()[-1]
            temp = temperature[0].get_text()
            if labels and sn in labels:
                ret.append({'sn': sn,  # pyright: ignore[reportUnknownMemberType]
                            'name': labels[sn],
                            'temp': temp})
            else:
                ret.append({'sn': sn,  # pyright: ignore[reportUnknownMemberType]
                            'temp': temp})

        return json.dumps(ret)
    return ""
