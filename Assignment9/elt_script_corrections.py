import arcpy
import requests
import csv
from urllib.parse import urlencode


def extract():
    print("Calling your mother I mean Extract Function...")
    url = ("https://docs.google.com/spreadsheets/d/e/2PACX-1vTDjitOlmILea7koCORJkq6QrUcwBJM7K3vy4guXB0mU_nWR6wsPn136bpH6ykoUxyYMW7wTwkzE37l/pub?output=csv")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CSV: {e}")
        return False
    data = response.text
    with open(r"C:\Users\paint\Downloads\addresses.csv", "w", encoding="utf-8") as output_file:
        output_file.write(data)
    return True


def transform():
    print("Add City, State and geocode addresses")
    input_path = r"C:\Users\paint\Downloads\addresses.csv"
    output_path = r"C:\Users\paint\Downloads\new_addresses.csv"

    with open(output_path, "w", newline='', encoding="utf-8") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(["X", "Y", "Type"])

        with open(input_path, "r", encoding="utf-8") as in_f:
            reader = csv.DictReader(in_f)
            for row in reader:
                raw = row.get("Street Address", "").strip()
                address = f"{raw}, Boulder, CO"
                print(f"Geocoding: {address}")

                params = {
                    "address": address,
                    "benchmark": "2020",
                    "format": "json"
                }
                try:
                    r = requests.get(
                        "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress",
                        params=params
                    )
                    r.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Request error for {address}: {e}")
                    continue

                resp = r.json()
                matches = resp.get("result", {}).get("addressMatches", [])
                if not matches:
                    print(f"No match for {address}, skipping...")
                    continue

                coords = matches[0].get('coordinates', {})
                x = coords.get('x')
                y = coords.get('y')
                writer.writerow([x, y, "Residential"]);


def load():
    arcpy.env.workspace = r"C:\Users\paint\Documents\ArcGIS\Projects\WestNileOutbreak\WestNileOutbreak.gdb"
    arcpy.env.overwriteOutput = True

    in_table = r"C:\Users\paint\Downloads\new_addresses.csv"
    out_fc = "avoid_points"
    x_field = "X"
    y_field = "Y"

    arcpy.management.XYTableToPoint(
        in_table, out_fc, x_field, y_field
    )
    result = arcpy.GetCount_management(out_fc)
    count = int(result.getOutput(0))
    print(f"Loaded {count} points.")


if __name__ == "__main__":
    if extract():
        transform()
        load()
    else:
        print("Extraction failed, aborting.")