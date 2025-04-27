# Run_GSheetsEtl.py

from GSheetsEtls import GSheetsEtls

if __name__ == "__main__":
    etl_instance = GSheetsEtls(
        "https://foo_bar.com",       # fixed URL
        r"C:\Users",                # raw-string for Windows path
        "GSheets",
        r"C:\Users\paint\Documents\ArcGIS\Projects\BodelMuilder\BodelMuilder.gdb"          # full path to your geodatabase
    )
    etl_instance.process()
