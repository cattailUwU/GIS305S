# lab3.py

import arcpy
import yaml
import logging
from GSheetsEtl import GSheetsEtl
from SpatialEtl import SpatialEtl
import requests

def setup():
    logging.debug("ENTER setup()")
    # load config
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    # configure logging to write to <proj_dir>/wnv.log
    logging.basicConfig(
        filename=f"{config_dict.get('proj_dir')}wnv.log",
        filemode="w",
        level=logging.DEBUG
    )
    logging.debug("EXIT  setup()")
    return config_dict

def main():
    logging.debug("ENTER main()")
    config = setup()
    logging.info("Starting West Nile Virus Simulation")
    # run your ETL process
    etl = GSheetsEtl(config)
    etl.process()
    logging.debug("EXIT  main()")

if __name__ == '__main__':
    main()
