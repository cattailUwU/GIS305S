import arcpy
import yaml
from GSheetsEtl import GSheetsEtl       # flat import, not etl.GSheetsEtl
from SpatialEtl import SpatialEtl       # bring in base class
import requests

def setup():
    with open('config/wnvoutbreak.yaml') as f:
        config_dict = yaml.load(f, Loader=yaml.FullLoader)
    return config_dict

def etl():
    print("etling...")
    # ✂️ CHANGE HERE: only pass the config dict, not four separate strings
    etl_instance = GSheetsEtl(config_dict)
    etl_instance.process()

    # ——— your local subclass remains exactly as before ———
    class LocalGSheetsEtl(SpatialEtl):
        def __init__(self, config_dict):
            super().__init__(config_dict)

        def extract(self):
            print("extracting addresses from google form spreadsheet")
            r = requests.get(
                "https://docs.google.com/spreadsheets/d/…/pubhtml"
            )
            r.encoding = "utf-8"
            with open(r"C:\Users\paint\Downloads\addresses.csv", "w") as output_file:
                output_file.write(r.text)

        def transform(self):
            super().transform()

        def load(self):
            arcpy.env.workspace = f"{self.config_dict.get('proj_dir')}WestNileOutbreak.gdb"
            arcpy.env.overwriteOutput = True
            arcpy.management.XYTableToPoint(
                r"C:\Users\paint\Downloads\addresses.csv",
                "avoid_points", "X", "Y"
            )
            print(arcpy.GetCount_management("avoid_points"))

        def process(self):
            self.extract()
            self.transform()
            self.load()
    # (end subclass)

def main():
    # load your YAML, make it global so etl() can see it
    global config_dict
    config_dict = setup()
    print(config_dict)
    etl()

if __name__ == '__main__':
    main()
