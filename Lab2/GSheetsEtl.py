from SpatialEtl import SpatialEtl

class GSheetsEtl(SpatialEtl):

    config_dict = None

    def __init__(self, config_dict):
        super().__init__(config_dict)

    def process(self):
        # call the inherited methods
        self.extract()
        self.transform()
        self.load()