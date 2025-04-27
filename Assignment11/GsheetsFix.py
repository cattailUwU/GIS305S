# GSheetsEtls.py

from SpatialEtl import SpatialEtl

class GSheetsEtls(SpatialEtl):
    def __init__(self, remote, local_dir, data_format, destination):
        super().__init__(remote, local_dir, data_format, destination)

    def process(self):
        # call the inherited methods
        self.extract()
        self.transform()
        self.load()
