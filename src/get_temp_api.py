""" get_temp.py - get the temperatures from the mocreo hub for the refridgerator
"""
import json
from flask import Flask
import rh_mocreo.mocreo_query as rhm

app = Flask(__name__)

@app.route("/", methods=['GET'])
def get_temps():
    """ main code for getting temps from a mocreo hub
    """
    # Get the config file information
    with open('config.json', 'r', encoding='utf8') as j:
        config = json.load(j)

    return rhm.mocreo_query(config) # type: ignore
