""" get_temp.py - get the temperatures from the mocreo hub for the refridgerator
"""
import json
import rh_mocreo.mocreo_query as rhm


def main():
    """ main code for getting temps from a mocreo hub
    """
    # Get the config file information
    with open('config.json', 'r', encoding='utf8') as j:
        config = json.load(j)

    print(rhm.mocreo_query(config)) # type: ignore


if __name__ == "__main__":
    main()
