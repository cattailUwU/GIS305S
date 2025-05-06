import arcpy
import requests
import csv
import yaml

# — load your config once at top —
with open('config/wnvoutbreak.yaml') as f:
    config_dict = yaml.load(f, Loader=yaml.FullLoader)

def extract():
    print("extracting addresses from google spreadsheet")
    r = requests.get(config_dict['remote_url'])
    r.encoding = "utf-8"
    data = r.text
    out_path = f"{config_dict['proj_dir']}addresses.csv"
    with open(out_path, "w") as output_file:
        output_file.write(data)

def transform():
    print("Add City, State")
    in_path  = f"{config_dict['proj_dir']}addresses.csv"
    out_path = f"{config_dict['proj_dir']}new_addresses.csv"

    with open(out_path, "w") as tf:
        tf.write("X,Y,Type\n")
        with open(in_path, "r") as pf:
            for row in csv.DictReader(pf):
                address = row["Street Address"] + " Boulder CO"
                print(address)
                geo_url = (
                    "https://geocoding.geo.census.gov/geocoder/"
                    f"locations/onelineaddress?address={address}"
                    "&benchmark=2020&format=json"
                )
                coords = requests.get(geo_url).json()['result']['addressMatches'][0]['coordinates']
                tf.write(f"{coords['x']},{coords['y']},Residential\n")

def load():
    arcpy.env.workspace       = f"{config_dict['proj_dir']}WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True
    in_table = f"{config_dict['proj_dir']}new_addresses.csv"
    arcpy.management.XYTableToPoint(in_table, "avoid_points", "X", "Y")
    print(arcpy.GetCount_management("avoid_points"))

if __name__ == "__main__":
    extract()
    transform()
    load()