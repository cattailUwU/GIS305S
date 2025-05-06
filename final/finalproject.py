# finalproject.py

import arcpy
import yaml
import logging
import os
from GSheetsEtl import GSheetsEtl

def setup():

    try:
        logging.debug("ENTER setup()")
        with open('config/wnvoutbreak.yaml') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)

        logging.basicConfig(
            filename=f"{config_dict.get('proj_dir')}wnv.log",
            filemode="w",
            level=logging.DEBUG
        )
        logging.debug("EXIT  setup()")
        return config_dict

    except Exception as e:
        logging.error(f"[setup] Failed: {e}")
        raise


def main():

    try:
        logging.debug("ENTER main()")
        config = setup()
        logging.info("Starting West Nile Virus Final Project")


        etl = GSheetsEtl(config)
        etl.process()


        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(26950)
        # Try to load the project file from config; only fall back to CURRENT if you're
        # actually running inside ArcGIS Pro as a script tool.
        aprx_file = config.get('aprx_path')
        if aprx_file and os.path.exists(aprx_file):
            aprx = arcpy.mp.ArcGISProject(aprx_file)
            logging.info(f"Loaded APRX from {aprx_file}")
        else:
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            logging.info("Loaded APRX from CURRENT")

        m    = aprx.listMaps()[0]
        logging.info("Spatial reference set to EPSG:26950")


        final_layer = m.listLayers("final_analysis")[0]
        sym         = final_layer.symbology
        sym.updateRenderer("SimpleRenderer")

        sym.renderer.symbol.symbolLayers[0].color = {'RGB': [255, 0,   0, 128]}  # red 50%
        sym.renderer.symbol.symbolLayers[1].color = {'RGB': [  0, 0,   0, 255]}  # black
        final_layer.symbology = sym
        logging.info("Applied simple renderer to 'final_analysis'")


        gdb             = config.get('proj_dir') + "WestNileOutbreak.gdb"
        boulder_fc      = os.path.join(gdb, "Boulder_addresses")
        final_fc        = os.path.join(gdb, "final_analysis")
        target_fc       = os.path.join(gdb, "Target_addresses")

        arcpy.analysis.SpatialJoin(
            in_features=boulder_fc,
            join_features=final_fc,
            out_feature_class=target_fc,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_COMMON"
        )
        logging.info("Created 'Target_addresses' via spatial join")


        target_lyr = m.listLayers("Target_addresses")[0]
        target_lyr.definitionQuery = "Join_Count = 1"
        logging.info("Applied definition query to 'Target_addresses'")

        # Save the project so changes persist
        aprx.save()
        logging.debug("EXIT  main()")

    except Exception as e:
        logging.error(f"[main] Failed: {e}")
        raise


if __name__ == "__main__":
    main()
