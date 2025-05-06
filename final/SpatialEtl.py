# SpatialEtl.py

class SpatialEtl:
    """
    Base class for spatial ETL operations.

    Provides the generic extract(), transform(), and load() methods that
    subclasses can override.
    """

    def __init__(self, config_dict):
        """
        Initialize with configuration.

        Parameters:
            config_dict (dict): Keys include 'remote_url' and 'proj_dir'.
        """
        try:
            self.config_dict = config_dict
        except Exception as e:
            print(f"[SpatialEtl.__init__] Initialization error: {e}")
            raise

    def extract(self):
        """
        Perform data extraction.

        Default implementation just logs the action.
        """
        try:
            print(f"extracting data from "
                  f"{self.config_dict.get('remote_url')} "
                  f"to {self.config_dict.get('proj_dir')}")
        except Exception as e:
            print(f"[SpatialEtl.extract] Error: {e}")
            raise

    def transform(self):
        """
        Perform data transformation.

        Default is a no‐op.
        """
        try:
            print("No transform step defined; skipping.")
        except Exception as e:
            print(f"[SpatialEtl.transform] Error: {e}")
            raise

    def load(self):
        """
        Perform data loading into the spatial database.

        Default is a no‐op.
        """
        try:
            print("No load step defined; skipping.")
        except Exception as e:
            print(f"[SpatialEtl.load] Error: {e}")
            raise
