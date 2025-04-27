from GSheetsEtls import GSheetsEtls

if __name__ == "__main__":
    etl_instance = GSheetsEtls("https://foo_bar.com", "C:Users", "GSheets", r"C:\Users\paint\Documents\ArcGIS\Projects\BodelMuilder\BodelMuilder.gdb")

    etl_instance.process()