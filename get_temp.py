""" get_temp.py - get the temperatures from the mocreo hub for the refridgerator
"""
import json
import requests
from bs4 import BeautifulSoup


def main():
    """ main code for getting temps from a mocreo hub
    """
    # Get the config file information
    with open('config.json', 'r', encoding='utf8') as j:
        config = json.load(j)

    # Process lables
    labels = {}
    if 'labels' in config:
        lbl = config['labels']
        for l in lbl:
            labels[l['sn']] = l['name']

    # Set up a session
    s = requests.Session()

    # Build the login url and request data
    url = f"http://{config['mocreo_hub']}/login"
    rdata = { "path": "/", "passwd": f"{config['password']}" }

    # loging to start the session
    req = s.post(url, rdata)
    if req.status_code != 200:
        print(f"ERROR authorizing: {req.status_code}")

    # now request the sensor page
    url = f"http://{config['mocreo_hub']}/sensors"
    req = s.get(url)
    if req.status_code != 200:
        print(f"ERROR in getting sensors: {req.status_code}")

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
            if labels:
                ret.append({'sn': sn, 'name': labels[sn], 'temp': temp})
            else:
                ret.append({'sn': sn, 'temp': temp})

        print(json.dumps(ret))

if __name__ == "__main__":
    main()
