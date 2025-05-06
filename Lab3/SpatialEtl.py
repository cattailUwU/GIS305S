class SpatialEtl:
    def __init__(self, config_dict):
        self.config_dict = config_dict

    def extract(self):
        print(f"extracting data from {self.config_dict.get('remote_url')}"
              f" to {self.config_dict.get('proj_dir')}")

    def transform(self):
        # default: do nothing (or raise NotImplementedError if you prefer)
        print("No transform step defined; skipping.")

    def load(self):
        # default: do nothing
        print("No load step defined; skipping.")