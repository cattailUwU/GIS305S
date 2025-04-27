from GSheetsEtls import GSheetsEtls

if __name__ == "__main__":
    etl_instance = GSheetsEtls("https://foo_bar.com", "C:Users", "GSheets", "C:/Users/my.gdb")

    etl_instance.process()