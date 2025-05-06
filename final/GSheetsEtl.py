# GSheetsEtl.py

from SpatialEtl import SpatialEtl

class GSheetsEtl(SpatialEtl):
    """
    ETL subclass that (eventually) pulls data from a Google Sheet
    and writes it into spatial formats.
    """

    def __init__(self, config_dict):
        """
        Initialize the Google Sheets ETL with the same config dict.

        Parameters:
            config_dict (dict): Keys include 'remote_url' and 'proj_dir'.
        """
        try:
            super().__init__(config_dict)
        except Exception as e:
            print(f"[GSheetsEtl.__init__] Error: {e}")
            raise

    def process(self):
        """
        Run the three‐step workflow: extract, transform, load.
        """
        try:
            self.extract()
            self.transform()
            self.load()
        except Exception as e:
            print(f"[GSheetsEtl.process] Error: {e}")
            raise
